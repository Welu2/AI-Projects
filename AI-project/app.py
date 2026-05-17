import streamlit as st
import yaml

# 1. Open and safely read the external configuration file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

settings = config["platform_settings"]

# 2. Dynamically build the dashboard using the file settings
st.title(f"📊 {settings['app_name']}")
st.write("This control panel reads its structural boundaries from an external YAML file.")

st.subheader("Active System Properties")
st.metric(label="Max Allowed Generation Tokens", value=settings["max_tokens"])
st.metric(label="API Connection Timeout", value=f"{settings['api_timeout_seconds']} seconds")

# 3. Check and display system maintenance status
if settings["maintenance_mode"]:
    st.error("🚨 SYSTEM STATUS: OFFLINE FOR MAINTENANCE. Please check back later.")
else:
    st.success("✅ SYSTEM STATUS: ONLINE & HEALTHY. Core infrastructure clusters active.")
