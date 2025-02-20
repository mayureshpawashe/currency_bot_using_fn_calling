import os
import streamlit as st
from dotenv import load_dotenv
import groq

# Load API Key from .env file
load_dotenv()
key = os.getenv("GROQ_API_KEY")

if not key:
    st.error("API key not found. Please set it in the .env file.")
    st.stop()

# Initialize Groq API client
client = groq.Client(api_key=key)

# Function to perform currency conversion
def convert_currency(amount, from_currency, to_currency):
    exchange_rates = {
        "USD": {"EUR": 0.85, "INR": 82.5},
        "EUR": {"USD": 1.18, "INR": 96.8},
        "INR": {"USD": 0.012, "EUR": 0.010},
    }

    rate = exchange_rates.get(from_currency, {}).get(to_currency, None)

    if rate:
        converted_amount = round(amount * rate, 2)
        return f"{amount} {from_currency} is {converted_amount} {to_currency} at rate {rate}"
    else:
        return "Exchange rate not available"

# Streamlit UI
st.title("💱 Currency Converter")
st.write("Convert between different currencies.")

amount = st.number_input("Enter Amount:", min_value=0.01, step=0.01, format="%.2f")
from_currency = st.selectbox("From Currency:", ["USD", "EUR", "INR"])
to_currency = st.selectbox("To Currency:", ["USD", "EUR", "INR"])

if st.button("Convert"):
    # Ask Groq for confirmation on conversion (but call function manually)
    user_input = f"Convert {amount} {from_currency} to {to_currency}"

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": user_input}]
    )

    # Convert currency manually
    result = convert_currency(amount, from_currency, to_currency)
    st.success(result)
