# DeepSeek4Free
You can read more about the features at this links (source repositories):
[github.com/xtekky/deepseek4free](https://github.com/xtekky/deepseek4free) <br>
[github.com/Doremii109/deepseek4free-fix](https://github.com/Doremii109/deepseek4free-fix) <br>

I just updated the repository so that the functionality works as an MCP server. As of March 28, 2026.

I use it with "qwen code"

```json
{
  "mcpServers": {
    "deepseek-brain": {
      "command": "python",
      "args": [
        "C:\\Users\\ringill\\repo\\deepseek4free\\deepseek_mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\Users\\ringill\\repo\\deepseek4free"
      }
    }
  }
}
```