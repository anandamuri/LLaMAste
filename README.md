# LLM News Chatbot

An LLM-powered news chatbot built with Python and Streamlit, designed to summarize recent headlines. This tool uses the gnews library to fetch the latest google news articles and trafilatura with playwright to extract full article content. Summarization uses a local LLaMA 3 model via ollama, prompt engineered to produce concise summaries. Users can interact through a Streamlit interface with dark/light mode, which supports chat history for follow-up questions. 

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

https://github.com/user-attachments/assets/fab5d452-6bfe-4f32-a08c-c59113ed198b

<img width="1512" height="489" alt="1 5" src="https://github.com/user-attachments/assets/e15197ca-9b52-4ff0-83da-d5132dbe5bb9" />
<img width="1509" height="574" alt="2" src="https://github.com/user-attachments/assets/a9732889-2d90-423c-a67f-c109bc057d94" />
<img width="1511" height="462" alt="3" src="https://github.com/user-attachments/assets/785ccf66-c999-48f9-87d9-786e2d020675" />
<img width="1512" height="461" alt="4" src="https://github.com/user-attachments/assets/56793a1c-dbe6-451e-9b25-8fbd1228682f" />
<img width="1511" height="820" alt="light" src="https://github.com/user-attachments/assets/240aac97-2d97-4271-9ff8-8559381b7507" />
<img width="1512" height="818" alt="dark" src="https://github.com/user-attachments/assets/2a983e7e-ee93-4030-b58e-a0de888fe6f2" />
