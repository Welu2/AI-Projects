import streamlit as st
import asyncio
import random
# 1. Import your brand new async background simulation engine
from engine import simulate_heavy_ai_job, load_config

st.set_page_config(page_title="Async Workers Hub", page_icon="⚡")
st.title("⚡ Async Infrastructure Job Worker")
st.write("Keep the dashboard interactive while heavy AI tasks process in the background.")

saved_data = load_config()
st.sidebar.info(f"Operator Session: {saved_data.get('operator', 'Alpha')}")

st.subheader("Execute Background AI Workload")
job_id = f"AI-TASK-{random.randint(1000, 9999)}"

# 2. Trigger the async generator loop safely
if st.button("🚀 Dispatch Non-Blocking AI Job"):
    status_box = st.empty()
    progress_bar = st.progress(0)
    
    # Define an async runner loop inside our button execution
    async def run_pipeline():
        step_count = 5
        current_step = 0
        
        # Stream the async generator values as they yield
        async for status_update in simulate_heavy_ai_job(job_id, steps=step_count):
            status_box.text(status_update)
            if current_step < step_count:
                current_step += 1
                progress_bar.progress(int((current_step / step_count) * 100))
        
        st.balloons()

    # Run the asynchronous function using the modern asyncio framework
    asyncio.run(run_pipeline())

st.divider()
st.caption("Notice how you can still interact with the sidebar or other widgets while the progress bar calculates!")
