from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
import streamlit as st

def get_response(user_query, chat_history):


    llm = ChatOllama(model='mistral')



    template = '''
        Welcome to the ChatBot from Ollama Mistral
        Answer the following questions considering the history of the conversations:
        Chat History: {chat_history}
        User Question: {user_question}
    '''

    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | llm | StrOutputParser()

    return chain.stream({
        "chat_history":chat_history,
        "user_question":user_query
    })

st.set_page_config(page_title="Streamlit Ollama Chatbot")
st.title('Ollama Mistral ChatBot')

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [AIMessage(content="I am a ChatBot created from Ollama Mistral. How can I help you?")]

for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

user_query = st.chat_input("Enter your message")

if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("Human"):
        st.markdown(user_query)
    with st.chat_message("AI"):
        response = st.write_stream(get_response(user_query,st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(content=response))        