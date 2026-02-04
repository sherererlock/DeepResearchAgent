# Load environment variables and set up auto-reload
from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
thread = {"configurable": {"thread_id": "1"}}


from .src.research_agent_scope import scope_research

result = scope_research.invoke(
    {"messages": [HumanMessage(content="我想要研究汽车")]}, 
    config=thread
)

for message in result["messages"]:
    message.pretty_print()
