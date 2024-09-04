# API-ChatBot
 
## Overview

This repository contains a chatbot application built with Flask and LangChain, integrated with OpenAI's GPT-4o-mini model. The chatbot supports user interactions via a web interface and can perform tasks like fetching weather information and retrieving upcoming movie details using APIs.

## Features

- **Interactive Chat Interface**: Users can interact with the chatbot through a web interface.
- **Weather Information**: The chatbot can fetch weather data for a specified location and date range.
- **Movie Information**: The chatbot can retrieve a list of upcoming movies.
- **Conversation History**: The chatbot maintains a conversation history to provide contextually relevant responses.
- **Automatic Conversation Summarization**: When the conversation history becomes lengthy, it is summarized to keep interactions concise.

## Setup

### Prerequisites

- Python 3.x
- Flask
- LangChain
- OpenAI API Key
- API keys for weather and movie services

### Installation

1. **Clone the Repository**
   ```bash
   git clone <[repository-url](https://github.com/samanvay13/API-ChatBot.git)>
   cd <repository-directory>
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**

   Create a `.env` file in the root directory with the following variables:

   ```env
   OPENAI_API_KEY=<your-openai-api-key>
   ```

4. **Run the Application**

   Start the Flask application:

   ```bash
   python app.py
   ```

   The application will be accessible at `http://127.0.0.1:5000/`.

## Usage

### Web Interface

1. Navigate to the root URL of the application (`http://127.0.0.1:5000/`).
2. Type your query into the chat interface and submit it.
3. The chatbot will respond with relevant information, optionally using external tools like weather or movie databases.

### API Tools

The chatbot uses two main tools:

1. **Weather Tool**
   - Fetches weather data based on location and date range.
   - Accepts a location name and a time option (today, single date, or multiple dates).

2. **Movies Tool**
   - Retrieves a list of upcoming movies from the Movies Database API.

### Conversation Management

- **Conversation History**: The chatbot keeps track of the conversation to provide coherent responses based on context.
- **Summarization**: If the conversation history exceeds a certain length, it is automatically summarized to maintain clarity.

## Customization

### Adding More Tools

To add more tools to the chatbot:

1. Define the new tool function.
2. Decorate the function with `@tool`.
3. Add the new tool to the `tools` list.

### Modifying the Chatbot's Behavior

- **Conversation Length**: You can adjust the threshold for conversation summarization by modifying the `if len(conversation_history) > 5` condition in the `handle_new_query` function.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgments

- [LangChain](https://www.langchain.com/)
- [OpenAI](https://www.openai.com/)
- [Flask](https://flask.palletsprojects.com/)

---

Feel free to contribute or modify the project as needed. If you encounter any issues, please open an issue on GitHub.
