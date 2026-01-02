import logging
from typing import Dict, Any, Optional

from llm_call import llm_call
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Executor-Agent")

@mcp.tool()
async def execute_step(
    step: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Executes a SINGLE research step.
    This agent does not plan, reason globally, or replan.
    """

    system_prompt = f"""
You are a research executor AI.

You will execute EXACTLY ONE research step.

Step:
{step}

Rules:
- Do not invent extra steps
- Do not modify the step
- If execution is not possible, mark as failed
- Return ONLY valid JSON in the following format:

{{
  "step_number": int,
  "step_status": "completed" | "failed",
  "step_result": "Concrete result or evidence",
  "notes": "Errors, limitations, or observations"
}}
"""

    try:
        result = await llm_call(system_prompt)
        return result

    except Exception as e:
        logging.error(f"[Executor-Agent] Step execution failed: {e}")
        return None
