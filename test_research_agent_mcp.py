
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import json

console = Console()

from dotenv import load_dotenv
load_dotenv()

import research_agent_mcp
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, filter_messages

from langchain_core.messages import HumanMessage

research_brief = """I want to identify and evaluate the coffee shops in San Francisco that are considered the best based specifically  
on coffee quality. My research should focus on analyzing and comparing coffee shops within the San Francisco area, 
using coffee quality as the primary criterion. I am open regarding methods of assessing coffee quality (e.g.,      
expert reviews, customer ratings, specialty coffee certifications), and there are no constraints on ambiance,      
location, wifi, or food options unless they directly impact perceived coffee quality. Please prioritize primary    
sources such as the official websites of coffee shops, reputable third-party coffee review organizations (like     
Coffee Review or Specialty Coffee Association), and prominent review aggregators like Google or Yelp where direct  
customer feedback about coffee quality can be found. The study should result in a well-supported list or ranking of
the top coffee shops in San Francisco, emphasizing their coffee quality according to the latest available data as  
of July 2025."""

from tool_utils import format_messages

async def test_mcp_agent():
    print("🚀 Starting MCP Agent...")
    print("Note: First run might be slow as it installs MCP servers via npx.")
    
    initial_message = HumanMessage(content=f"{research_brief}.")
    # Print initial request
    format_messages([initial_message])
    
    async for output in research_agent_mcp.agent_mcp.astream(
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
    asyncio.run(test_mcp_agent())
