import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage,AIMessage
import google.generativeai as genai
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("ChatBot 🤖")

#Get Response Function with Openai
def Get_Response(query,chat_history):
    prompt="""
    You are a helpful assistant, Aswer the following question considering the chat history.
    chat_history:{chat_history}
    User_question:{query}
    """
    # Set up the model
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    
    st.write("here")
    # Pass the combined prompt to the model
    response = model.generate_content([{
        "content": prompt
    }])
    
    return response["text"]
    

#Chat History
if "Chat_History" not in st.session_state:
    st.session_state.Chat_History=[]

#Coverstation
for message in st.session_state.Chat_History:
    if isinstance(message,HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

#User Query
User_Query=st.chat_input("Your Msg....")
if User_Query is not None and User_Query!="":
    st.session_state.Chat_History.append(HumanMessage(User_Query))
    
    with st.chat_message("Human"):
        st.markdown(User_Query)
        
    with st.chat_message("AI"):
        Response=Get_Response(User_Query,st.session_state.Chat_History)
        st.markdown(Response)
    
    st.session_state.Chat_History.append(AIMessage(Response))