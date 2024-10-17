from datetime import datetime
from typing import List
from wikipedia import summary
from langchain_core.tools import Tool


def get_current_time(*args, **kwargs):
    """Returns the current time in HH:MM AM/PM format
    """
    now = datetime.now()
    return now.strftime("%I:%M %p")


def search_wikipedia(query: str):
    """Get information in wikipedia
    """
    try:
        return summary(query, sentences=2)
    except Exception as e:
        return "I couldn't find any information of that"


def tools_generator() -> List[Tool]:
    return [Tool(name="Time",
                 description="useful when you need to get the current time",
                 func=get_current_time) , 
            Tool(name="Wikipedia", description="useful when you need to get data about people in wikipedia", func=search_wikipedia)]