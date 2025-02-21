import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(model_name="mixtral-8x7b-32768", api_key=groq_api_key)

prompt = PromptTemplate.from_template("Translate this text into {language}: {text}")

parser = StrOutputParser()

# Chain Using LangChain LCEL
chain = prompt | model | parser

# Streamlit UI
st.title("AI Translator Using Function-Calling-LCEL")
text = st.text_area("Enter text to translate:")
language = st.selectbox("Select a language:", [
    "French", "Spanish", "German", "Chinese", "Japanese", "Italian",
    "Portuguese", "Russian", "Arabic", "Hindi", "Korean", "Dutch",
    "Turkish", "Thai", "Greek","Marathi"
])

if st.button("Translate"):
    if text and language:
        translation = chain.invoke({"text": text, "language": language})
        st.success(f"**Translated Text:** {translation}")
    else:
        st.warning("Please enter text and select a language before translating.")
