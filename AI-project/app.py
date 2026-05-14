import logging
import os
import streamlit as st

# 1. Configure the logging system to save messages to a file
logging.basicConfig(
    filename="platform_activity.log",
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

st.title("📊 AI Platform Monitoring App")
st.write("Type a query below. Every single button click is tracked securely.")

user_query = st.text_input("Enter a test query:", "Hello AI Infrastructure!")

# 2. Track user actions and system status
if st.button("Submit Query to Platform"):
    if user_query.strip() == "":
        st.error("Empty input detected.")
        logging.warning("User attempted to submit an empty query.")
    else:
        st.success(f"Query processed: '{user_query}'")
        # Record a successful platform interaction
        logging.info(f"Successfully processed query of length: {len(user_query)}")

# 3. Simulate an unexpected platform error for testing
if st.button("Simulate Infrastructure Error 🚨"):
    st.error("Database connection lost! (Simulated)")
    logging.error("CRITICAL: Failed to connect to backend database cluster.")
