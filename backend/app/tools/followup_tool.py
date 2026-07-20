from app.agents.ai_agent import llm


def recommend_followup(interactions: list):
    """
    Generates an AI-powered follow-up recommendation
    based on previous HCP interactions.
    """

    if not interactions:
        return "No interactions available to generate a follow-up recommendation."

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

Analyze the following interaction history with a Healthcare Professional.

Recommend the most appropriate next follow-up action.

Your response should include:

1. Recommended next action
2. Reason for the recommendation
3. Suggested communication method
4. Suggested timeframe
5. Important points to discuss during the follow-up

Keep the recommendation professional, concise, and based only on the provided interaction history.

Do not provide medical advice or make clinical treatment decisions.

Interaction History:

{interaction_text}
"""

    response = llm.invoke(prompt)

    return response.content