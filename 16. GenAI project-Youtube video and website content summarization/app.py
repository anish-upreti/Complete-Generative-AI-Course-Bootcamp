## import necessary libraries and modules
import validators, streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader


# Streamlit app
st.set_page_config(page_title="Langchain: Text summarization from Youtube and Websites", page_icon="🦜")
st.title("🦜 Summarize Text from YT and Websites")
st.subheader("URL of youtube or website to summarize")

# Get Groq api key and url
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key",value="", type="password")

generic_url = st.text_input("URL",label_visibility="collapsed")

# llm model using Groq API
llm = ChatGroq(groq_api_key=groq_api_key, model="Llama3-8b-8192")

# generating prompt template and prompt for the chain
prompt_template = """
Give a summary of the following content:
Content:{text}
"""

prompt = PromptTemplate(input_variables=["text"], template=prompt_template)



if st.button("Summarize the content"):
    # validate inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide both: groq api key and the url")   # for displaying error message in streamlit web app
    
    elif not validators.url(generic_url):
        st.error("Please provide a valid url: a YT video url or website url")

    else:
        try:
            with st.spinner("Processing....."):      # display the temporary waiting message during a execution
                # loading the website or YT video data
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(urls=[generic_url], ssl_verify=False,
                                                   headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                    ##  here used headers for mimicking real browser’s User-Agent to avoid getting blocked or receiving simplified content from some sites.
                
                docs = loader.load()

                # chain for summarization
                chain = load_summarize_chain(llm=llm, chain_type="stuff", prompt=prompt)
                summary = chain.run(docs)

                st.success(summary)

        except Exception as e:
            st.exception(f"Exception:{e}")
