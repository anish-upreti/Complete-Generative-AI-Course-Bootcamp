## import libraries and modules
import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler  # streams the internal steps of an LLM agent or chain directly into your Streamlit app UI, so you can visualize what’s happening behind the scenes.


# Streamlit app
st.set_page_config(page_title="Math problem solver and data search assistant.", page_icon="🧮")
st.title(" 🧮 Math problem solver using Google Gemma 2")

# get the groq api key
groq_api_key = st.sidebar.text_input(label="Groq API key",type="password")

if not groq_api_key.strip():  # for more robust checking by elimination leading/trailing white spaces, we use strip() 
    st.info("Please add your groq api key.")
    st.stop()

# llm model using groq api
llm = ChatGroq(model = "Gemma2-9b-It", groq_api_key=groq_api_key)

# initialize tools
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the Internet to find the vatious information on the topics mentioned"
)

# initialize math tool
math_chain = LLMMathChain.from_llm(llm=llm)
calculator = Tool(
    name = "Calculator",
    func=math_chain.run,
    description="A tools for answering math related questions. Only input mathematical expression that needs to be provided"
)

# create prompt and prompt template

prompt = """
You are a helpful AI assistant that solves math problems in a detailed, step-by-step way.
Break down your reasoning clearly and display the solution in bullet points.

Question:{question}
Answer:
"""

prompt_template = PromptTemplate(input_variables=["question"], template=prompt)

# combine all tools into chain
chain = LLMChain(llm=llm, prompt=prompt_template)

reasoning_tool = Tool(
    name = "Reasoning tool",
    func=chain.run,
    description="A tool for answering logic-based and reasoning questions."
)

# initialize agents
assistant_agent = initialize_agent(
    tools = [wikipedia_tool, calculator, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,        # verbose Controls how much debug info is printed in the console
    handle_parsing_errors=True   #If the LLM’s response doesn’t follow the expected format, this lets LangChain recover gracefully.

)

# Initialize chat history in session state (only on first load)
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role":"assistant", "content": "Hello , I'm a Math chatbot who can help with math questions."}
    ]

# Display all previous messages from the chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# start the interaction
question = st.text_area("Enter your question:")

if st.button("find my answer"):
    if question:
        with st.spinner("Generating response........"):
            st.session_state.messages.append({"role":"user", "content":question})
            st.chat_message("user").write(question)

            # Callback handler to stream agent thoughts (tool use, reasoning)
            st_callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)

            # Run the agent with the full conversation history as input
            response = assistant_agent.run(st.session_state.messages, callbacks=[st_callback])

            # Add assistant's response to the chat history
            st.session_state.messages.append({"role":"assistant", "content":response})
            st.write("### Response:")
            st.success(response)

    else:
        st.warning("Please enter the question.")
