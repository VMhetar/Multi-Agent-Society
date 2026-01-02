import logging
from typing import Dict, Any, Optional

from llm_call import llm_call
from schemas import RESEARCH_PLAN_SCHEMA 
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Planner-Agent")


@mcp.resource(uri="planner/schema")
def schema_agent_task() -> Dict[str, Any]:
    """
    Exposes the research planning schema.
    """
    return RESEARCH_PLAN_SCHEMA   


@mcp.tool()
async def plan_agent_task(task_description: str) -> Optional[Dict[str, Any]]:
    """
    Generates a structured research plan that strictly follows RESEARCH_PLAN_SCHEMA.
    """

    system_prompt = f"""
You are a research planner AI.

You MUST return ONLY valid JSON.
Do NOT include explanations, markdown, or commentary.

The output MUST strictly follow this schema:
{RESEARCH_PLAN_SCHEMA}

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
