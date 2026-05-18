import streamlit as st
# 1. Import your custom backend functions directly from your engine file!
from engine import compute_server_load, get_system_greeting

st.title("🧩 Modular Infrastructure Hub")
st.write("This application splits its backend logic from its visual presentation.")

# 2. Use the greeting function from engine.py
operator_name = st.text_input("Enter Operator Name:", "Alpha")
greeting = get_system_greeting(operator_name)
st.success(greeting)

# 3. Use the calculation function from engine.py
st.subheader("Resource Diagnostics")
users = st.slider("Simulate Active Users on Cluster:", min_value=1, max_value=100, value=20)

with st.spinner("Calculating infrastructure load..."):
    # Run the imported calculation logic
    estimated_load = compute_server_load(users)
    st.metric(label="Estimated CPU Infrastructure Load", value=f"{estimated_load}%")
