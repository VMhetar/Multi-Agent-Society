from typing import Dict, Any

RESEARCH_STEP_SCHEMA: Dict[str, Any] = {
    "step_number": int,
    "step_description": str,
    "success_criteria": str,
    "depends_on": list
}
