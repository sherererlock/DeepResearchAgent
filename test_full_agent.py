from tool_utils import format_messages
from langchain_core.messages import HumanMessage
from full_agent import agent
import asyncio

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import json

from dotenv import load_dotenv
load_dotenv()

console = Console()

async def test_full_agent():
    print("🚀 Starting MCP Agent...")
    print("Note: First run might be slow as it installs MCP servers via npx.")
    
    initial_message = HumanMessage(content=f"移动端GPU架构详解")
    # Print initial request
    format_messages([initial_message])
    
    async for output in agent.astream(
        {"researcher_messages": [initial_message]}, 
        stream_mode="updates"
    ):
        for node_name, node_content in output.items():
            # console.print(f"[bold blue]Step: {node_name}[/bold blue]")
            if "researcher_messages" in node_content:
                format_messages(node_content["researcher_messages"])
            
            if "compressed_research" in node_content:
                console.print(Panel(node_content["compressed_research"], title="📊 Final Research Report", border_style="magenta"))

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_full_agent())