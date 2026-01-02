import logging
from typing import Dict, Any, Optional

from schemas import RESEARCH_STEP_SCHEMA
from llm_call import llm_call
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Executor-Agent")

def validate_step(step: Dict[str, Any]) -> Optional[str]:
    """
    Validates that the step conforms to RESEARCH_STEP_SCHEMA.
    Returns error message if invalid, otherwise None.
    """
    for key, expected_type in RESEARCH_STEP_SCHEMA.items():
        if key not in step:
            return f"Missing required field: {key}"
        if not isinstance(step[key], expected_type):
            return f"Invalid type for '{key}': expected {expected_type}"

    return None

@mcp.tool()
async def execute_step(step: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Executes a SINGLE research step.
    This agent does not plan, replan, or reason globally.
    """
    error = validate_step(step)
    if error:
        return {
            "step_number": step.get("step_number", -1),
            "step_status": "failed",
            "step_result": "",
            "notes": f"Schema validation failed: {error}"
        }
    system_prompt = f"""
You are a research executor AI.

You will execute EXACTLY ONE research step.

Step:
{step}

Rules:
- Do NOT invent new steps
- Do NOT modify the step
- If execution is not possible, mark as failed
- Be concrete and evidence-based

Return ONLY valid JSON in this EXACT format:

{{
  "step_number": {step["step_number"]},
  "step_status": "completed" | "failed",
  "step_result": "Concrete result, evidence, or output",
  "notes": "Errors, limitations, or observations"
}}
"""

    try:
        result = await llm_call(system_prompt)
        return result

    except Exception as e:
        logging.error(f"[Executor-Agent] Step execution failed: {e}")
        return {
            "step_number": step.get("step_number", -1),
            "step_status": "failed",
            "step_result": "",
            "notes": f"Execution error: {e}"
        }
