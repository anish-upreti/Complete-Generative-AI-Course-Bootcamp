import streamlit as st             
from pathlib import Path            # helpful for working with file paths in a cross-platform way.
from langchain.agents import create_sql_agent    # used to create an agent that can process SQL queries based on natural language input.
from langchain.sql_database import SQLDatabase   # This class helps interface with SQL databases. It requires a SQLAlchemy engine for connection.
from langchain.agents.agent_types import AgentType  
from langchain.callbacks import StreamlitCallbackHandler  # A callback handler to update the Streamlit UI as the agent processes queries.
from langchain.agents.agent_toolkits import SQLDatabaseToolkit  # integrates the database with LangChain’s agent
from sqlalchemy import create_engine   # creates a connection to your SQL database
import sqlite3
from langchain_groq import ChatGroq   #class from langchain_groq that represents a language model to process Natural language input


st.set_page_config(page_title = "Chat with SQL DB using Langchain", page_icon = "🦜")
st.title("🦜 LangChain: Chat with SQL DB")

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

radio_opt = ["Use sqlite3 database", "Connect to your MySQL database"]
selected_opt = st.sidebar.radio(label ="Choose the DB which you want to chat with:", options = radio_opt)

if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("Enter MySQL host:")
    mysql_username = st.sidebar.text_input("Enter MySQL username:")
    mysql_password = st.sidebar.text_input("Enter MySQL password:", type="password")
    mysql_database = st.sidebar.text_input("Enter MySQL database:")
else:
    db_uri = LOCALDB

api_key  = st.sidebar.text_input("Enter your Groq API key", type = "password")

if not db_uri:
    st.info("Please enter the database information and uri")

if not api_key:
    st.info("Please add the groq api key")

##LLM
llm = ChatGroq(groq_api_key = api_key, model_name = "Llama3-8b-8192", streaming=True)

## connecting with database
@st.cache_resource(ttl="3h")    # caches the database connection for 3 hours
def configure_db(db_uri, mysql_host=None,mysql_username=None, mysql_password=None,mysql_database=None):
    if db_uri == LOCALDB:
        db_filepath = (Path(__file__).parent/"student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{db_filepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator = creator))
    elif db_uri == MYSQL:
        if not (mysql_database and mysql_host and mysql_password and mysql_username):
            st.error("Please provide all necessary MySQL details.")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_username}:{mysql_password}@{mysql_host}/{mysql_database}"))

if db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host,mysql_username, mysql_password, mysql_database)

if db_uri == LOCALDB:
    db = configure_db(db_uri)

# toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm = llm,
    toolkit = toolkit,
    verbose = True,  # Enables logging for debugging or tracking the agent’s actions.
    agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION # The agent is a "zero-shot" agent, which means it can handle queries even if it hasn't been trained on specific tasks. It will try to react to user input based on a description and perform actions (like querying the database).
)

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content":"How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder = "Ask anything from the database:")

if user_query:
    st.session_state.messages.append({"role":"user", "content":user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        response=agent.run(user_query,callbacks=[streamlit_callback])
        st.session_state.messages.append({"role":"assistant","content":response})
        st.write(response)

