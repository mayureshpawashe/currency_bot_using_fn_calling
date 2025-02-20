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
    "USD": {"EUR": 0.85, "INR": 82.5, "GBP": 0.75, "CAD": 1.34, "AUD": 1.50, "JPY": 150.2},
    "EUR": {"USD": 1.18, "INR": 96.8, "GBP": 0.88, "CAD": 1.57, "AUD": 1.76, "JPY": 176.4},
    "INR": {"USD": 0.012, "EUR": 0.010, "GBP": 0.009, "CAD": 0.016, "AUD": 0.018, "JPY": 1.84},
    "GBP": {"USD": 1.33, "EUR": 1.14, "INR": 110.5, "CAD": 1.79, "AUD": 2.02, "JPY": 201.6},
    "CAD": {"USD": 0.75, "EUR": 0.64, "INR": 61.2, "GBP": 0.56, "AUD": 1.13, "JPY": 113.4},
    "AUD": {"USD": 0.67, "EUR": 0.57, "INR": 55.3, "GBP": 0.50, "CAD": 0.88, "JPY": 100.2},
    "JPY": {"USD": 0.0067, "EUR": 0.0057, "INR": 0.54, "GBP": 0.005, "CAD": 0.0088, "AUD": 0.01},
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
from_currency = st.selectbox("From Currency:", ["USD", "EUR", "INR", "GBP", "CAD", "AUD", "JPY"])
to_currency = st.selectbox("To Currency:", ["USD", "EUR", "INR", "GBP", "CAD", "AUD", "JPY"])

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
