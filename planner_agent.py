import os
import requests
import logging

from mcp.server.fastmcp import FastMCP

mcp = FastMCP('Planner-Agent')

@mcp.tool()
def plan_agent_task(task_description:str) -> str|None:
    """
    Plans a sequence of steps to accomplish a given task.
    task_description: A brief description of the task to be accomplished.
    Returns a detailed plan outllining the steps needed to complete the task.
    """

    