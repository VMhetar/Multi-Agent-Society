import logging
from typing import Dict, Optional, List, Any

from llm_call import llm_call
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Planner-Agent")


RESEARCH_SCHEMA: Dict[str, Any] = {
    "res_id": 1,
    "res_name": "Research Name",
    "res_description": "Detailed description of the research task",

    "res_steps": [
        {
            "step_number": 1,
            "step_description": "Atomic, executable research step",
            "success_criteria": "Objective condition to mark step as complete",
            "depends_on": []
        }
    ],

    "res_uncertainties": [
        {
            "unknown": "What data sources are reliable?",
            "impact": "High",
            "mitigation": "Executor evaluates source credibility"
        }
    ]
}


@mcp.resource(uri="planner/schema")
def schema_agent_task() -> Dict[str, Any]:
    """
    Exposes the research planning schema.
    This is a declarative contract used by planner, executor, and debater.
    """
    return RESEARCH_SCHEMA


@mcp.tool()
async def plan_agent_task(task_description: str) -> Optional[Dict[str, Any]]:
    """
    Generates a structured research plan that strictly follows RESEARCH_SCHEMA.
    """

    system_prompt = f"""
You are a research planner AI.

You MUST return ONLY valid JSON.
Do NOT include explanations, markdown, or commentary.

The output MUST strictly follow this schema:
{RESEARCH_SCHEMA}

Task description:
{task_description}

Rules:
- Each step must be atomic and independently executable
- Include clear success_criteria for every step
- Use depends_on to express step dependencies
- Explicitly list uncertainties and assumptions
- Avoid vague verbs (e.g., "analyze deeply", "understand")
"""

    try:
        plan = await llm_call(system_prompt)
        return plan

    except Exception as e:
        logging.error(f"[Planner-Agent] Planning failed: {e}")
        return None
