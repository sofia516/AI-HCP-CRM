from typing import Literal

from pydantic import BaseModel
from langgraph.graph import StateGraph, END

from app.agents.state import AgentState
from app.agents.ai_agent import llm
from app.agents.prompts import SYSTEM_PROMPT
from app.database.database import SessionLocal

from app.tools.log_tool import log_interaction
from app.tools.edit_tool import edit_interaction
from app.tools.search_tool import search_interactions
from app.tools.summary_tool import summarize_interactions
from app.tools.followup_tool import recommend_followup

from app.models.interaction import Interaction


# -------------------------------------------------
# Structured Output Models
# -------------------------------------------------

class RouteDecision(BaseModel):
    tool_name: Literal[
        "log",
        "edit",
        "search",
        "summary",
        "followup",
        "chat",
    ]


class LogInteractionData(BaseModel):
    hcp_id: int
    interaction_type: str
    notes: str


class EditInteractionData(BaseModel):
    interaction_id: int
    interaction_type: str
    notes: str


class SearchInteractionData(BaseModel):
    keyword: str


class SummaryRequestData(BaseModel):
    hcp_id: int

class FollowupRequestData(BaseModel):
    hcp_id: int    

# -------------------------------------------------
# Router Node
# -------------------------------------------------

def router_node(state: AgentState):
    """
    Determines which CRM tool should handle the user's request.
    """

    router_llm = llm.with_structured_output(RouteDecision)

    try:
        result = router_llm.invoke(
            f"""
You are an intent router for an AI-first Healthcare CRM.

Classify the user's request into exactly one category:

- log: Create or record a new HCP interaction.
- edit: Modify an existing interaction.
- search: Find or view previous interactions.
- summary: Summarize a meeting or interaction.
- followup: Recommend a next action or follow-up.
- chat: General conversation that does not require a CRM tool.

User request:
{state["user_query"]}
"""
        )

        state["tool_name"] = result.tool_name

    except Exception:
        state["tool_name"] = "chat"

    return state


# -------------------------------------------------
# Log Interaction Node
# -------------------------------------------------

def log_node(state: AgentState):
    """
    Extracts interaction information and saves
    the interaction to PostgreSQL.
    """

    extractor = llm.with_structured_output(LogInteractionData)

    try:
        data = extractor.invoke(
            f"""
Extract interaction details from the following Healthcare CRM request.

Required information:

- hcp_id: Numeric ID of the Healthcare Professional.
- interaction_type: For example Visit, Call, Email, or Meeting.
- notes: Concise details about the interaction.

User request:
{state["user_query"]}
"""
        )

        db = SessionLocal()

        try:
            result = log_interaction(
                db=db,
                hcp_id=data.hcp_id,
                interaction_type=data.interaction_type,
                notes=data.notes,
            )

            state["tool_output"] = result
            state["final_response"] = result["message"]

        finally:
            db.close()

    except Exception as error:
        state["final_response"] = (
            f"Unable to log interaction: {str(error)}"
        )

    return state


# -------------------------------------------------
# Edit Interaction Node
# -------------------------------------------------

def edit_node(state: AgentState):
    """
    Extracts update information and modifies
    an existing interaction in PostgreSQL.
    """

    extractor = llm.with_structured_output(EditInteractionData)

    try:
        data = extractor.invoke(
            f"""
Extract the information required to edit an existing
Healthcare CRM interaction.

Required information:

- interaction_id: Numeric ID of the interaction to update.
- interaction_type: The new interaction type.
- notes: The updated interaction notes.

User request:
{state["user_query"]}
"""
        )

        db = SessionLocal()

        try:
            result = edit_interaction(
                db=db,
                interaction_id=data.interaction_id,
                interaction_type=data.interaction_type,
                notes=data.notes,
            )

            state["tool_output"] = result
            state["final_response"] = result["message"]

        finally:
            db.close()

    except Exception as error:
        state["final_response"] = (
            f"Unable to edit interaction: {str(error)}"
        )

    return state


# -------------------------------------------------
# Search Interaction Node
# -------------------------------------------------

def search_node(state: AgentState):
    """
    Extracts a keyword and searches interactions
    stored in PostgreSQL.
    """

    extractor = llm.with_structured_output(SearchInteractionData)

    try:
        data = extractor.invoke(
            f"""
Extract the most useful keyword for searching CRM interactions.

The keyword can represent:
- a medical topic
- an interaction type
- a word or phrase in interaction notes

Examples:

"Find interactions about hypertension"
Keyword: hypertension

"Search for Visit interactions"
Keyword: Visit

User request:
{state["user_query"]}
"""
        )

        db = SessionLocal()

        try:
            interactions = search_interactions(
                db=db,
                keyword=data.keyword,
            )

            if not interactions:
                state["tool_output"] = []
                state["final_response"] = (
                    f"No interactions found for '{data.keyword}'."
                )
                return state

            results = []

            for interaction in interactions:
                results.append(
                    {
                        "id": interaction.id,
                        "hcp_id": interaction.hcp_id,
                        "interaction_type": interaction.interaction_type,
                        "notes": interaction.notes,
                        "created_at": (
                            interaction.created_at.isoformat()
                            if interaction.created_at
                            else None
                        ),
                    }
                )

            state["tool_output"] = results

            formatted_results = "\n\n".join(
                [
                    (
                        f"Interaction ID: {item['id']}\n"
                        f"HCP ID: {item['hcp_id']}\n"
                        f"Type: {item['interaction_type']}\n"
                        f"Notes: {item['notes']}"
                    )
                    for item in results
                ]
            )

            state["final_response"] = (
                f"Found {len(results)} interaction(s):\n\n"
                f"{formatted_results}"
            )

        finally:
            db.close()

    except Exception as error:
        state["final_response"] = (
            f"Unable to search interactions: {str(error)}"
        )

    return state

#-------------------------------------------------
# Summary Node
#-------------------------------------------------  

def summary_node(state: AgentState):
    """
    Fetches interactions for an HCP from PostgreSQL
    and generates an AI-powered meeting summary.
    """

    extractor = llm.with_structured_output(SummaryRequestData)

    try:
        data = extractor.invoke(
            f"""
Extract the Healthcare Professional ID from the user's request.

Required field:

- hcp_id: Numeric ID of the Healthcare Professional whose
  interactions should be summarized.

User request:
{state["user_query"]}
"""
        )

        db = SessionLocal()

        try:
            records = (
                db.query(Interaction)
                .filter(Interaction.hcp_id == data.hcp_id)
                .order_by(Interaction.created_at.desc())
                .all()
            )

            if not records:
                state["tool_output"] = []
                state["final_response"] = (
                    f"No interactions found for HCP ID {data.hcp_id}."
                )
                return state

            interactions = []

            for record in records:
                interactions.append(
                    {
                        "id": record.id,
                        "interaction_type": record.interaction_type,
                        "notes": record.notes,
                        "created_at": (
                            record.created_at.isoformat()
                            if record.created_at
                            else None
                        ),
                    }
                )

        finally:
            db.close()

        summary = summarize_interactions(interactions)

        state["tool_output"] = interactions
        state["final_response"] = summary

    except Exception as error:
        state["final_response"] = (
            f"Unable to summarize interactions: {str(error)}"
        )

    return state        


#-------------------------------------------------
# Follow-up Node        
#-------------------------------------------------  

def followup_node(state: AgentState):
    """
    Fetches an HCP's interaction history from PostgreSQL
    and generates an AI-powered follow-up recommendation.
    """

    extractor = llm.with_structured_output(FollowupRequestData)

    try:
        data = extractor.invoke(
            f"""
Extract the Healthcare Professional ID from the user's request.

Required field:

- hcp_id: Numeric ID of the Healthcare Professional for whom
  a follow-up recommendation should be generated.

User request:
{state["user_query"]}
"""
        )

        db = SessionLocal()

        try:
            records = (
                db.query(Interaction)
                .filter(Interaction.hcp_id == data.hcp_id)
                .order_by(Interaction.created_at.desc())
                .all()
            )

            if not records:
                state["tool_output"] = []
                state["final_response"] = (
                    f"No interactions found for HCP ID {data.hcp_id}. "
                    "A follow-up recommendation cannot be generated."
                )
                return state

            interactions = []

            for record in records:
                interactions.append(
                    {
                        "id": record.id,
                        "interaction_type": record.interaction_type,
                        "notes": record.notes,
                        "created_at": (
                            record.created_at.isoformat()
                            if record.created_at
                            else None
                        ),
                    }
                )

        finally:
            db.close()

        recommendation = recommend_followup(interactions)

        state["tool_output"] = interactions
        state["final_response"] = recommendation

    except Exception as error:
        state["final_response"] = (
            f"Unable to generate follow-up recommendation: {str(error)}"
        )

    return state

# -------------------------------------------------
# General Chat Node
# -------------------------------------------------

def chat_node(state: AgentState):
    """
    Handles requests that do not require CRM tool execution.
    """

    try:
        response = llm.invoke(
            [
                ("system", SYSTEM_PROMPT),
                ("human", state["user_query"]),
            ]
        )

        state["final_response"] = response.content

    except Exception as error:
        state["final_response"] = (
            f"Unable to process your request: {str(error)}"
        )

    return state


# -------------------------------------------------
# Conditional Router
# -------------------------------------------------

def route(state: AgentState):
    return state.get("tool_name", "chat")


# -------------------------------------------------
# Build LangGraph
# -------------------------------------------------

builder = StateGraph(AgentState)

# Register nodes
builder.add_node("router", router_node)
builder.add_node("log", log_node)
builder.add_node("edit", edit_node)
builder.add_node("search", search_node)
builder.add_node("summary", summary_node)   
builder.add_node("followup", followup_node)
builder.add_node("chat", chat_node)

# Set entry point
builder.set_entry_point("router")

# Route AI requests
builder.add_conditional_edges(
    "router",
    route,
    {
        "log": "log",
        "edit": "edit",
        "search": "search",

        # Real nodes for these will be added next
        "summary": "summary",
        "followup": "followup",

        "chat": "chat",
    },
)

# End workflow after node execution
builder.add_edge("log", END)
builder.add_edge("edit", END)
builder.add_edge("search", END)
builder.add_edge("summary", END)
builder.add_edge("followup", END)
builder.add_edge("chat", END)

# Compile LangGraph
graph = builder.compile()