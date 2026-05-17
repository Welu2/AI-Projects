import streamlit as st
import time

st.title("⏳ AI Platform Rate Limiter")
st.write("Prevent users from spamming our infrastructure resources.")

# 1. Initialize a counter in the app memory to track click times
if "request_history" not in st.session_state:
    st.session_state.request_history = []

# 2. Strict Platform Rules (You will tweak these!)
MAX_REQUESTS = 3          # Maximum number of allowed clicks
TIME_WINDOW = 10          # Time window in seconds

if st.button("Call Heavy AI Model 🚀"):
    current_time = time.time()
    
    # Clean up history: remove clicks that happened a long time ago
    st.session_state.request_history = [
        t for t in st.session_state.request_history if current_time - t < TIME_WINDOW
    ]
    
    # 3. Check if the user has exceeded their limits
    if len(st.session_state.request_history) >= MAX_REQUESTS:
        st.error("🚨 Rate Limit Exceeded! You are making requests too fast.")
        st.warning(f"Please wait a few seconds before trying again. Rule: Max {MAX_REQUESTS} requests per {TIME_WINDOW}s.")
    else:
        # Record the current click time
        st.session_state.request_history.append(current_time)
        st.success(f"✅ Request Processed! (Requests used: {len(st.session_state.request_history)}/{MAX_REQUESTS})")
