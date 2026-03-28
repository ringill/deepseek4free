"""
DeepSeek MCP Server - Exposes DeepSeek R1 as a tool for Qwen Code

This server allows Qwen Code to use DeepSeek as an external reasoning engine
via the MCP (Model Context Protocol).
"""

from mcp.server.fastmcp import FastMCP
from dsk.api import DeepSeekAPI
import os
import time

# Initialize MCP server
mcp = FastMCP("DeepSeek-Brain")

# Initialize DeepSeek API
# Make sure DEEPSEEK_AUTH_TOKEN is set in .env file
auth_token = os.getenv("DEEPSEEK_AUTH_TOKEN")
if not auth_token:
    raise ValueError("DEEPSEEK_AUTH_TOKEN environment variable is not set")

api = DeepSeekAPI(auth_token)

# Track active chat sessions
active_sessions = {}


@mcp.tool()
async def ask_deepseek_reasoner(prompt: str, use_thinking: bool = True, use_search: bool = False) -> str:
    """
    Ask DeepSeek R1 for deep analysis and reasoning.
    
    Use this tool when you need:
    - Complex problem solving
    - Deep code analysis
    - Algorithm design
    - Mathematical reasoning
    - Research and analysis
    
    Args:
        prompt: The question or task to analyze
        use_thinking: Enable step-by-step reasoning (default: True)
        use_search: Enable web search for up-to-date info (default: False)
    
    Returns:
        DeepSeek's response as a string
    """
    chat_id = api.create_chat_session()
    session_key = f"session_{int(time.time())}"
    active_sessions[session_key] = chat_id
    
    try:
        response = ""
        for chunk in api.chat_completion(
            chat_id, 
            prompt, 
            thinking_enabled=use_thinking,
            search_enabled=use_search
        ):
            if chunk['type'] == 'text':
                response += chunk['content']
        
        # Clean up session after getting response
        api.delete_chat_session(chat_id)
        del active_sessions[session_key]
        
        return response
        
    except Exception as e:
        # Clean up on error
        if chat_id:
            try:
                api.delete_chat_session(chat_id)
            except:
                pass
        if session_key in active_sessions:
            del active_sessions[session_key]
        raise Exception(f"DeepSeek API error: {str(e)}")


@mcp.tool()
async def analyze_code_with_deepseek(code: str, task_description: str = "") -> str:
    """
    Ask DeepSeek to analyze code and provide insights.
    
    Args:
        code: The code to analyze
        task_description: Optional description of what the code should do
    
    Returns:
        Analysis including improvements, bugs, and optimizations
    """
    prompt = f"Analyze this code and provide detailed feedback"
    if task_description:
        prompt += f" for: {task_description}"
    
    prompt += f"\n\nCode:\n```python\n{code}\n```"
    
    chat_id = api.create_chat_session()
    
    try:
        response = ""
        for chunk in api.chat_completion(chat_id, prompt, thinking_enabled=True):
            if chunk['type'] == 'text':
                response += chunk['content']
        
        api.delete_chat_session(chat_id)
        return response
        
    except Exception as e:
        if chat_id:
            try:
                api.delete_chat_session(chat_id)
            except:
                pass
        raise Exception(f"DeepSeek API error: {str(e)}")


if __name__ == "__main__":
    mcp.run()
