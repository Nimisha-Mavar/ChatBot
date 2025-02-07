import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"  # Enables LangSmith tracing

# Initialize OpenAI Model with Streaming Enabled
model = ChatOpenAI(model="gpt-4o", streaming=True,max_completion_tokens=1000)

# Streamlit UI
st.title("🤖 Chatbot 🤖")
st.write("Ask me anything!")

# Store chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    # Add user input to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat UI
    with st.chat_message("user"):
        st.markdown(prompt)

    # Define prompt template
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a knowledgeable and friendly AI assistant."),
        ("user", "{question}")
    ])

    # Create chain
    chain = prompt_template | model | StrOutputParser()

    # Display assistant response
    with st.chat_message("assistant"):
        response_container = st.empty()  # Placeholder for streaming text
        full_response = ""

        # Stream response as it is generated
        for chunk in chain.stream({"question": prompt}):
            full_response += chunk
            response_container.markdown(full_response)  # Update response in real-time

    # Save assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
