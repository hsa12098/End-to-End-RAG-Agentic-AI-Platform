# from fastapi import FastAPI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_groq import ChatGroq
# from langserve import add_routes
# import uvicorn
# import os
# from langchain_community.llms import Ollama
# from dotenv import load_dotenv

# load_dotenv()

# os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

# app=FastAPI(
#     title="Langchain Server",
#     version="1.0",
#     decsription="A simple API Server"

# )

# add_routes(
#     app,
#     ChatGroq(model="llama-3.1-8b-instant"),
#     path="/groq"
# )
# model=ChatGroq(model="llama-3.1-8b-instant")
# ##ollama llama2
# llm=Ollama(model="llama2")

# prompt1=ChatPromptTemplate.from_template("Write me an essay about {topic} with 100 words")
# prompt2=ChatPromptTemplate.from_template("Write me an poem about {topic} for a 5 years child with 100 words")

# add_routes(
#     app,
#     prompt1|model,
#     path="/essay"


# )

# add_routes(
#     app,
#     prompt2|llm,
#     path="/poem"


# )


# if __name__=="__main__":
#     uvicorn.run(app,host="localhost",port=8000)

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import InMemoryChatMessageHistory

# Load environment variables (like GROQ_API_KEY)
load_dotenv()

# Set GROQ_API_KEY from environment variables
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

app = FastAPI(
    title="LangChain Server with Memory",
    version="1.0",
    description="A simple API Server with conversational memory."
)

# --- 1. Initialize Models and Chains ---
# Groq Chat Model (used for essay)
groq_model = ChatGroq(model="llama-3.1-8b-instant")
# Ollama LLM (used for poem)
ollama_llm = Ollama(model="llama2")

# Prompts
prompt1 = ChatPromptTemplate.from_template(
    "You are an essay writer. Write me an essay about {topic} with 100 words. "
    "Use the history to continue the conversation. History: {history}"
)
prompt2 = ChatPromptTemplate.from_template(
    "You are a children's poet. Write me a poem about {topic} for a 5 year old with 100 words. "
    "Use the history to continue the conversation. History: {history}"
)

# --- 2. Define Session Store for Memory ---
# In-memory store for demonstration purposes. Key is the session_id.
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Retrieves or creates an InMemoryChatMessageHistory for a given session ID."""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# --- 3. Create Chains with History ---

# Essay Chain (Groq)
essay_chain = prompt1 | groq_model

essay_with_history = RunnableWithMessageHistory(
    essay_chain,
    get_session_history,
    input_messages_key="topic", # This is the variable the prompt expects
    history_messages_key="history" # This is the key we use for history in the prompt
)

# Poem Chain (Ollama)
poem_chain = prompt2 | ollama_llm

poem_with_history = RunnableWithMessageHistory(
    poem_chain,
    get_session_history,
    input_messages_key="topic", # This is the variable the prompt expects
    history_messages_key="history" # This is the key we use for history in the prompt
)

# --- 4. Add Routes ---
add_routes(app, groq_model, path="/groq_raw") 

# Add routes for the chains wrapped with memory
add_routes(
    app,
    essay_with_history,
    path="/essay"
)

add_routes(
    app,
    poem_with_history,
    path="/poem"
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)