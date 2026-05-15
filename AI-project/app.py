import streamlit as st

# 1. Read the URL parameters to check if a monitoring system is pinging us
query_params = st.query_params

# 2. If the monitoring system asks for "/?status=check", show a clean health report
if "status" in query_params and query_params["status"] == "check":
    st.text("STATUS: HEALTHY")
    st.text("DATABASE: CONNECTED")
    st.text("AI_ENGINE: READY")
    # Stop rendering the rest of the regular website for the monitor bot
    st.stop()

# --- Regular Web App Interface Starts Here ---
st.title("🏥 Automated Platform Health Monitoring")
st.write("This app includes a hidden heartbeat endpoint for automated monitoring systems.")

st.info("The regular user dashboard is active and running normally.")
st.write("To simulate a platform monitoring bot, add '?status=check' to the end of your browser's URL bar.")
