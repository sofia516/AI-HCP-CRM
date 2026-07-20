from app.agents.ai_agent import llm

response = llm.invoke("Say hello in one sentence.")

print(response.content)