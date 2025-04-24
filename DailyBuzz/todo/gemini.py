import google.generativeai as genai
# from .models import Task
import os
from dotenv import load_dotenv
from datetime import datetime

# Set your Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Or hardcode for now

model = genai.GenerativeModel("gemini-1.5-pro")

def your_model_inference(text):
    today = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""
    You are a helpful assistant for a todo app.
    Today's date is: {today}
    Extract the user's intent, task name, and date/time from the command below.
    Return only valid JSON like this:

    {{
        "intent": "create_task",
        "task": "Go jogging",
        "datetime": "2025-04-23T06:00:00"
    }}

    Command: "{text}"
    """

    response = model.generate_content(prompt)
    
    # Use .text and parse the JSON from the response
    import json, re
    json_str = re.search(r"\{.*\}", response.text, re.DOTALL).group(0)
    return json.loads(json_str)


