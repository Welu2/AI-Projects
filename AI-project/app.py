import streamlit as st
import random

st.title("🔌 Infrastructure Circuit Breaker")
st.write("Simulate a primary system crash and watch the app automatically switch to a fallback system.")

# 1. Platform Admin Switch to simulate a live server crash
st.sidebar.header("🛠️ Infrastructure Control Room")
simulate_server_outage = st.sidebar.toggle("Simulate Primary Cloud Server Crash", value=False)

# 2. Main Application Logic Function
def process_ai_request():
    if simulate_server_outage:
        # This simulates a broken connection to a premium server
        raise ConnectionError("Could not reach premium cluster node.")
    else:
        return "✨ Premium Response: Processing data using ultra-fast Premium infrastructure!"

# 3. Interactive User Execution Block
if st.button("Execute AI Task"):
    try:
        with st.spinner("Contacting primary infrastructure..."):
            # Attempt to run the primary system
            response = process_ai_request()
            st.success(response)
            st.info("Status: Operating on Primary Cloud Node.")
            
    except ConnectionError as error:
        # 4. Graceful Degradation: The fallback kicks in automatically
        st.warning(f"🚨 Primary system failure caught: {error}")
        st.error("🔄 Circuit Breaker Tripped! Diverting traffic to Backup Node...")
        
        # Fallback operation
        st.info("📉 Fallback Active: Running on slower, offline local cache.")
        st.success("🤖 Backup Response: Running task with reduced performance, but application stayed online!")
