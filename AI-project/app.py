import streamlit as st

st.title("🛡️ Secure Input Gatekeeper")
st.write("This app simulates an AI gateway that validates text before sending it to a model.")

# 1. User text box
user_input = st.text_input("Enter your prompt for the AI model:")

# 2. The Validation Bouncer Check
if st.button("Process Prompt"):
    # Rule A: Check if it's completely empty
    if len(user_input.strip()) == 0:
        st.error("❌ Request Blocked: You cannot submit an empty prompt.")
        
    # Rule B: Check if the text is too long (protecting server costs)
    elif len(user_input) > 50:
        st.error(f"❌ Request Blocked: Prompt is too long ({len(user_input)} characters). Maximum allowed is 50.")
        st.warning("This keeps our server bills low and prevents system crashes!")
        
    # Rule C: Check for forbidden words (basic safety guardrail)
    elif "hack" in user_input.lower() or "bypass" in user_input.lower():
        st.error("🚨 Security Alert: Malicious keyword detected! Access denied.")
        
    # Success: The input passed all tests
    else:
        st.success("✅ Request Approved! Sending clean data to the AI engine.")
        st.info(f"Verified Prompt: '{user_input}'")
