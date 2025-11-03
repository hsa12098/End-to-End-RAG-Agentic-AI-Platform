# import requests
# import streamlit as st

# def get_openai_response(input_text):
#     response=requests.post("http://localhost:8000/essay/invoke",
#     json={'input':{'topic':input_text}})

#     return response.json()['output']['content']

# def get_ollama_response(input_text):
#     response=requests.post(
#     "http://localhost:8000/poem/invoke",
#     json={'input':{'topic':input_text}})

#     return response.json()['output']

#     ## streamlit framework

# st.title('Langchain Demo With LLAMA2 API')
# input_text=st.text_input("Write an essay on")
# input_text1=st.text_input("Write a poem on")

# if input_text:
#     st.write(get_openai_response(input_text))

# if input_text1:
#     st.write(get_ollama_response(input_text1))

import requests
import streamlit as st

# Define a fixed session ID for each conversational flow
# These IDs link to the memory streams on the LangServe server (app.py)
ESSAY_SESSION_ID = "essay_chat_session"
POEM_SESSION_ID = "poem_chat_session"

st.set_page_config(layout="wide", page_title="LangChain Memory Demo")

# --- API Interaction Functions ---

def get_essay_response(input_text):
    """Invokes the essay chain with a specific session ID for memory."""
    try:
        response = requests.post(
            "http://localhost:8000/essay/invoke",
            json={
                'input': {'topic': input_text},
                # Pass the session_id in the configurable section for memory
                'config': {'configurable': {'session_id': ESSAY_SESSION_ID}}
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()['output']['content']
    except requests.exceptions.RequestException as e:
        return f"Error connecting to essay server: {e}"


def get_poem_response(input_text):
    """Invokes the poem chain with a specific session ID for memory."""
    try:
        response = requests.post(
            "http://localhost:8000/poem/invoke",
            json={
                'input': {'topic': input_text},
                # Pass the session_id in the configurable section for memory
                'config': {'configurable': {'session_id': POEM_SESSION_ID}}
            },
            timeout=60 
        )
        response.raise_for_status()
        # Ollama output structure is usually just a string
        return response.json()['output']
    except requests.exceptions.RequestException as e:
        return f"Error connecting to poem server: {e}"

# --- Page Definitions ---

def essay_page():
    """Renders the Essay Writer interface."""
    st.header('✍️ Essay Writer (Groq Model)')
    st.markdown("Ask for an essay, then ask a follow-up about the previous essay's topic to test memory.")

    # Initialize essay history in session state
    if 'essay_history' not in st.session_state:
        st.session_state.essay_history = []

    with st.form("essay_form"):
        essay_input = st.text_input(
            "Start/Continue Essay Conversation:",
            placeholder="e.g., 'Write about the benefits of bees', then 'make it longer'"
        )
        submitted = st.form_submit_button("Generate Essay", type="primary")

        if submitted and essay_input:
            with st.spinner("Writing essay..."):
                response = get_essay_response(essay_input)
            
            st.session_state.essay_history.append(
                {"prompt": essay_input, "response": response}
            )

    st.markdown("---")
    st.subheader("Conversation History")
    
    # Display history (newest first)
    for chat in reversed(st.session_state.essay_history):
        # Use a container for the chat box appearance
        with st.container(border=True):
            st.markdown(f"**You:** {chat['prompt']}")
            st.markdown(f"**AI Response:** {chat['response']}")


def poem_page():
    """Renders the Children's Poet interface."""
    st.header('🧸 Children\'s Poet (Ollama Model)')
    st.markdown("Ask for a poem, then ask to change a detail in the same conversation to test memory.")

    # Initialize poem history in session state
    if 'poem_history' not in st.session_state:
        st.session_state.poem_history = []

    with st.form("poem_form"):
        poem_input = st.text_input(
            "Start/Continue Poem Conversation:",
            placeholder="e.g., 'A cat with blue shoes', then 'Change the cat to a dog'"
        )
        submitted = st.form_submit_button("Generate Poem", type="primary")

        if submitted and poem_input:
            with st.spinner("Writing poem..."):
                response = get_poem_response(poem_input)
            
            st.session_state.poem_history.append(
                {"prompt": poem_input, "response": response}
            )

    st.markdown("---")
    st.subheader("Conversation History")

    # Display history (newest first)
    for chat in reversed(st.session_state.poem_history):
        # Use a container for the chat box appearance
        with st.container(border=True):
            st.markdown(f"**You:** {chat['prompt']}")
            st.markdown(f"**AI Response:** {chat['response']}")


# --- Main App Logic (Router) ---

# Define the pages and their corresponding functions
PAGES = {
    "Essay Writer": essay_page,
    "Children's Poet": poem_page
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to:", list(PAGES.keys()))

# Call the function associated with the selected page
page = PAGES[selection]
page()