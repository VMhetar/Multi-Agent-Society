import os
import asyncio
import httpx
import logging
from mcp.server.fastmcp import FastMCP

url = "https://openrouter.ai/api/v1/chat/completions"

api_key = os.getenv("OPENROUTER_API_KEY")

mcp = FastMCP('Agent-Society')

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

system_prompt ="""
You are an expert AI assistant designed to help users with a variety of tasks.
"""
@mcp.tool()
async def llm_call(system_prompt: str) -> str:
    payload = {
        "model": "openrouter/openchat-7b",
        "messages": [
            {"role": "system", "content": system_prompt},
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        data = response.json()
        return data['choices'][0]['message']['content']