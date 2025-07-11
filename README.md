# LLM News Chatbot

An AI-powered news chatbot built with Python, leveraging Google News scraping and LLM summarization.
This tool uses the gnews library to scrape current news articles and employs LLaMA 3 via Ollama to generate summaries. It uses prompt engineering to format outputs effectively and maintain clarity. A Streamlit interface enables users to search for topics and interact with the chatbot.

## Run Instructions

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Activate Virtual Environment
   ```
   source venv/bin/activate
   ```

2. Start Ollama:
   ```
   ollama run llama3
   ```

3. Run the app:
   ```
   streamlit run app.py
   ```

Demo:
