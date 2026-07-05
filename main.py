from fastapi import BackgroundTasks, Depends, FastAPI
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

from fastapi import FastAPI
from crewai import Agent, Task, Crew, LLM

app = FastAPI()

# Explicit LLM object pointing at your local Ollama server
ollama_llm = LLM(
    model="ollama/llama3.1:8b",
)

# Define agent — llm goes here, not "model"

# Define task


# Define crew — no llm/chat_llm/manager_llm needed for a simple sequential crew


def run_crew(q:str):
    agent1 = Agent(
        role="Lead Competitve Intelligence Researcher",
        goal="Uncover pricing changes, feature releases, and positioning shifts for {q}",
        backstory="You are a Lead Competitive Intelligensce Researcher with 8+ years tracking B2B SaaS markets. You read pricing page copy diffs to detect tier restructuring; you interpret job posting language as a leading indicator of roadmap investment; and you triangulate feature intent from changelog fragments before they become public narratives.You label every finding with a confidence tier: [CONFIRMED] - directly sourced and dated [INFERRED] - derived from indirect signals, reasoning shown [SIGNAL] - early/weak indicator, not yet actionable.",
        llm=ollama_llm,
        allow_delegation=False,
        verbose=True,
    )

    agent2 = Agent(
        role="Senior Strategic Product Analyst",
        goal=""
    )

    task1 = Task(
        description="It receives the competitor company {q}, search for recent signals {q} pricing, changelog, new features announcement or release notes 2026.",
        expected_output="Get recent signals {q} pricing, changelog, new features announcement or release notes 2026.",
        agent=agent1,
    )

    task2 = Task(
        description="It receives the context from task1 and scrape and extract from web.",
        expected_output="Pricing page (label tier names, prices, seat limits) - Changelog or blog (last 3 entries only) - Homepage hero copy (capture exact headline + subtext) ",
        agent=agent1,
        context=[task1]
    )

    task3 = Task(
        description="Produce a Markdown report with sections: ## Pricing signals ## Feature release signals ## Positioning / messaging signals ## Recommended actions Label every finding [CONFIRMED], [INFERRED], or [SIGNAL]. Include source URL and date for every item. ",
        expected_output="A clean Markdown report with four sections. Every finding labeled by confidence tier. At least one recommended action per section. No raw HTML. No filler text. Facts and implications only.",
        agent=agent1,
        context=[task1,task2]
    )

    crew = Crew(
        agents=[agent1],
        tasks=[task1,task2,task3],
        memory=False,
        verbose=True,
    )
    result = crew.kickoff(inputs={"q": q})
    return result

@app.post("/run-crew")
async def send_crew_result(background_tasks: BackgroundTasks, q:str|None):
    background_tasks.add_task(run_crew,q)
    return {"message": "Crew result sent"}
    
@app.get("/")
def read_root():
    return {"Hello World from multi-agents-collaboration-framework"}

# @app.post("/send-notification/{email}")
# async def send_notification(
#     email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
# ):
#     message = f"message to {email}\n"
#     background_tasks.add_task(write_log, message)
#     return {"message": "Message sent"}

# @app.post("/items/")
# async def create_item(item: item):
#     item_dict = item.model_dump()
#     if item.tax is not none:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict

# @app.post("/agent_result")
# async def read_root(data: str):
#     return {"received":data}


# def write_log(message: str):
#     with open("log.txt", mode="a") as log:
#         log.write(message)


# def get_query(background_tasks: BackgroundTasks, q: str | None = None):
#     if q:
#         message = f"found query: {q}\n"
#         background_tasks.add_task(write_log, message)
#     return q


# @app.post("/send-notification/{email}")
# async def send_notification(
#     email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
# ):
#     message = f"message to {email}\n"
#     background_tasks.add_task(write_log, message)
#     return {"message": "Message sent"}
