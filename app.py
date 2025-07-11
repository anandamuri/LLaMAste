
import streamlit as st
from gnews import GNews
import ollama
import trafilatura
from playwright.sync_api import sync_playwright
import re

# --- Configuration ---
st.set_page_config(page_title="LLaMAste News", page_icon="🦙")
st.title("LLaMAste News Chatbot")

# --- Themes ---
mode = st.radio("Choose mode:", ["Dark", "Light"], horizontal=True)
bg, fg, caret = ("#111", "#fff", "#fff") if mode == "Dark" else ("#fff", "#111", "#111")
you_color = "#ff9500"  # orange (adjust as you like)
llamaste_color = "#2081e2"  # blue


# --- Styles ---
st.markdown(
    """
    <style>
        .stApp {
            background-color: %(bg)s;
            color: %(fg)s;
        }
        div[data-testid="stMarkdownContainer"] *, .stTextInput > div > input, .stTextArea textarea, .stTextInput input {
            color: %(fg)s !important;
        }
        .stTextInput > div > input, .stTextArea textarea, .stTextInput input {
            background-color: %(bg)s !important;
            border-color: #555;
            caret-color: %(caret)s !important;
        }

        /* Button styles */
        button[kind="primary"] {
            background-color: %(bg)s !important;
            color: %(fg)s !important;
            border: 2px solid #222 !important;
        }
        button[kind="primary"]:hover, button[kind="primary"]:focus {
            background-color: %(fg)s !important;
            color: %(bg)s !important;
            border: 2px solid #555 !important;
        }

        .stButton>button {
            background-color: %(bg)s !important;
            color: %(fg)s !important;
            border: 2px solid #222 !important;
        }
        .stButton>button:hover, .stButton>button:focus {
            background-color: %(bg)s !important;
            color: %(bg)s !important;
            border: 2px solid #555 !important;
        }
        
        /* Hide the 'Press Enter to apply' helper */
        span[aria-live="polite"] {
            display: none !important;
        }

        div[data-testid="stMarkdownContainer"] .you-label {
            color: #ff9500 !important;
            font-weight: bold;
        }
        div[data-testid="stMarkdownContainer"] .llamaste-label {
            color: #2081e2 !important;
            font-weight: bold;
        }

    </style>
    """ % {"bg": bg, "fg": fg, "caret": caret, "you_color": you_color, "llamaste_color": llamaste_color},
    unsafe_allow_html=True
)

# --- Get Articles ---
def fetch_article_text(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_load_state('networkidle')
            html = page.content()
            browser.close()
        return trafilatura.extract(html)
    except Exception:
        return None

# --- Usable Articles ---
def get_good_articles(query, num=5):
    google_news = GNews()
    search = google_news.get_news(query)
    articles = []
    for result in search:
        text = fetch_article_text(result['url'])
        if text and len(text) > 100:
            articles.append({'title': result['title'], 'url': result['url'], 'text': text})
            if len(articles) == num:
                break
    return articles

def clean_markdown_formatting(text):
    text = re.sub(r'(\d)(\*)([^\s])', r'\1 \2\3', text)
    text = re.sub(r'\*([^\*]+)\*([A-Za-z])', r'*\1* \2', text)
    return text

def format_bullet_points(text):
    lines = text.split('\n')
    formatted = []
    for line in lines:
        line = line.strip()
        if line.startswith('•'):
            line = '- ' + line[1:].strip()
        elif line.startswith('-'):
            line = '- ' + line[1:].strip()
        formatted.append(line)
    return '\n'.join(formatted)

# --- State Setup ---
if 'msgs' not in st.session_state:
    st.session_state['msgs'] = []

# --- Topic Input ---
query = st.text_input("Name any topic to learn about:", key="main_query")
search_button = st.button("Search and Summarize", key="search_button")

# --- Initial ---
if search_button and query:
    st.session_state['msgs'] = []
    with st.spinner(f"Searching and parsing up to 5 articles for '{query}'..."):
        articles = get_good_articles(query, num=5)

    if not articles:
        st.warning("No articles with enough text found. Try another topic.")
    else:
        links = "\n".join([f"- [{a['title']}]({a['url']})" for a in articles])
        st.info("Summarizing these articles:\n" + links)

        all_texts = "\n\n".join([f"Article {i+1}: {a['title']}\n{a['text']}" for i, a in enumerate(articles)])
        system_prompt = "You are an expert news summarizer. Summarize the following news articles and ONLY return a 5 bullet point summary."

        st.session_state['msgs'] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Summarize the topic: {query}"}
        ]
        st.session_state['article_data'] = all_texts

        with st.spinner("Summarizing with LLaMAste..."):
            response = ""
            stream = ollama.chat(
                model='llamaste',
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": all_texts}
                ],
                stream=True
            )
            for chunk in stream:
                response += chunk['message']['content']

        st.session_state['msgs'].append({"role": "assistant", "content": response})
        st.markdown("### Combined Summary")

# --- Chat UI ---
if st.session_state['msgs']:
    st.markdown("---")
    st.markdown("#### Chat about the news")
    for msg in st.session_state['msgs']:
        if msg['role'] == 'user':
            st.markdown(f"<span class='you-label'>You:</span> {msg['content']}", unsafe_allow_html=True)

        elif msg['role'] == 'assistant':
            cleaned = clean_markdown_formatting(msg['content'])
            formatted = format_bullet_points(cleaned)
            st.markdown(f"<span class='llamaste-label'>LLaMAste:</span>\n\n{formatted}", unsafe_allow_html=True)

# --- Follow-Ups ---
if st.session_state['msgs'] and st.session_state['msgs'][-1]['role'] == 'assistant':
    followup = st.text_input("Ask a follow-up question (leave blank to end):", key=f"followup_{len(st.session_state['msgs'])}")
    if followup:
        st.session_state['msgs'].append({"role": "user", "content": followup})
        with st.spinner("Answering..."):
            resp = ""
            stream = ollama.chat(
                model='llamaste',
                messages=st.session_state['msgs'],
                stream=True,
            )
            for chunk in stream:
                resp += chunk['message']['content']
        st.session_state['msgs'].append({"role": "assistant", "content": resp})
        st.rerun()
