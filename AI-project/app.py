import os
import streamlit as st
from dotenv import load_dotenv

# 1. Load hidden configurations from the .env file
load_dotenv()

st.title("🔐 Secure AI Vault App")

# 2. Safely extract the secret key without typing it out in code
secret_key = os.getenv("MY_SECRET_AI_KEY")

if st.button("Check Infrastructure Security"):
    if secret_key:
        st.success("🔒 System Secure: Environment variable loaded successfully!")
        st.info(f"Retrieved Key: {secret_key}")
    else:
        st.error("🚨 System Vulnerable: Secret key missing or exposed!")
