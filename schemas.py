from typing import Dict, Any

RESEARCH_PLAN_SCHEMA: Dict[str, Any] = {
    "res_id": int,
    "res_name": str,
    "res_description": str,

    "res_steps": [
        {
            "step_number": int,
            "step_description": str,
            "success_criteria": str,
            "depends_on": list
        }
    ],

    "res_uncertainties": [
        {
            "unknown": str,
            "impact": str,
            "mitigation": str
        }
    ]
}
