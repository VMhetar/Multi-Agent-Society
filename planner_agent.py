import asyncio
import os
import requests
import logging
from llm_call import llm_call
from mcp.server.fastmcp import FastMCP

mcp = FastMCP('Planner-Agent')

@mcp.tool()
def plan_agent_task(task_description:str) -> str|None:
    """
    Plans a sequence of steps to accomplish a given task.
    task_description: A brief description of the task to be accomplished.
    Returns a detailed plan outllining the steps needed to complete the task.
    """
    system_prompt = f"""
    You are an expert planner AI assistant. Your job is to plan out a sequence of steps for a new research.
    Given the task description {task_description}, create a detailed plan outlining the steps needed to complete the task of research.
    """
    try:
        plan = asyncio.run(llm_call(system_prompt))
        return plan
    except Exception as e:
        logging.error(f"Error in plan_agent_task: {e}")
        return None