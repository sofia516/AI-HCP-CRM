from app.agents.ai_agent import llm


def summarize_interactions(interactions: list):
    """
    Generates an AI summary from a list of interaction records.
    """

    if not interactions:
        return "No interactions available to summarize."

    interaction_text = "\n\n".join(
        [
            (
                f"Interaction ID: {item['id']}\n"
                f"Type: {item['interaction_type']}\n"
                f"Notes: {item['notes']}\n"
                f"Created At: {item['created_at']}"
            )
            for item in interactions
        ]
    )

    prompt = f"""
You are an AI assistant for a Healthcare CRM.

Summarize the following interactions with a Healthcare Professional.

Provide a concise professional summary containing:

1. Main topics discussed
2. Important requests or concerns
3. Key decisions or outcomes
4. Any potential next steps

Interactions:

{interaction_text}
"""

    response = llm.invoke(prompt)

    return response.content