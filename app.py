from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from datetime import date
from langchain_core.tools import tool
import requests
import json
from enum import Enum
from datetime import datetime
from langchain_core.messages import HumanMessage, SystemMessage

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/chat", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    response = handle_new_query(msg)
    return response

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

class TimeOption(Enum):
    OPTION_1 = "today"
    OPTION_2 = "single date"
    OPTION_3 = "multi date"

@tool
def weather(location, time: TimeOption, start_date : date, end_date : date):
    """Getting Latitude and longitude from the location name"""
    loc_url = "https://geocode.maps.co/search"
    loc_params = {
        "q": location,
        "api_key" : "66c5dcd041c61814137721udx5d6895"
    }

    response = requests.get(loc_url, loc_params)
    data = response.json()
    weather_url = "https://api.open-meteo.com/v1/forecast"
    if time == TimeOption.OPTION_1:
        start_date = datetime.now().date()
        end_date = datetime.now().date()
        weather_params = {
            "latitude": data[0]["lat"],
            "longitude": data[0]["lon"],
            "daily": "temperature_2m_max,temperature_2m_min",
            "timezone": "auto",
            "forecast_days": 1
        }
    if time == TimeOption.OPTION_2 or time == TimeOption.OPTION_3:
        weather_params = {
            "latitude": data[0]["lat"],
            "longitude": data[0]["lon"],
            "daily": "temperature_2m_max,temperature_2m_min",
            "timezone": "auto",
            "start_date": start_date,
            "end_date": end_date
        }
    response = requests.get(weather_url, weather_params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Convert the response to a Python dictionary
        return data
    else:
        return f"Error: {response.status_code}"

@tool
def movies():
    """Fetches a list of upcoming movies from the Movies Database API."""
    url = "https://moviesdatabase.p.rapidapi.com/titles/x/upcoming"
    headers = {
        'x-rapidapi-host': 'moviesdatabase.p.rapidapi.com',
        'x-rapidapi-key': '32dcbded87msh801c6a12c151b95p17014cjsnf8dbefa2a26f'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

tools = [weather, movies]

llm_with_tools = llm.bind_tools(tools)

# Initialize an empty list to store the conversation
conversation_history = []

# Function to summarize the conversation history
def summarize_conversation(history):
    # Simple example using an LLM to summarize
    summary_query = "Summarize the following conversation: " + "\n".join([msg.content for msg in history])
    summary = llm_with_tools.invoke([HumanMessage(summary_query)])
    return [SystemMessage(summary.content)]

# Function to handle a new query and update the conversation history
def handle_new_query(query):
    global conversation_history
    #just these 2 existing here solves out date issue
    metadata = datetime.now().date()
    system_message = SystemMessage(f"If relevant, use {metadata} as the current date.")
    # Add the new query to the conversation history
    conversation_history.append(HumanMessage(query))
    # conversation_history.append(system_message)

    # Invoke the LLM with the conversation history
    ai_msg = llm_with_tools.invoke(conversation_history)

    # Append the AI's response to the conversation history
    conversation_history.append(ai_msg)

    # If there are any tool calls, handle them and append the results to the conversation history
    for tool_call in ai_msg.tool_calls:
        selected_tool = {"weather": weather, "movies": movies}[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        conversation_history.append(tool_msg)

    # Summarize the conversation if it gets too long
    if len(conversation_history) > 5:  # Arbitrary length before summarizing
        conversation_history = summarize_conversation(conversation_history)

    # Return the AI's response (you can also return the updated conversation history if needed)
    return ai_msg.content

if __name__ == '__main__':
    app.run()