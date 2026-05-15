import streamlit as st
import time

st.title("⚡ High-Speed Platform Caching")
st.write("See how platform engineers use memory tricks to speed up slow AI systems.")

# 1. This function simulates a slow, heavy AI computation
@st.cache_data
def heavy_ai_calculation(user_number):
    # Simulate a 5-second wait time (like a massive AI model thinking)
    time.sleep(5)
    return user_number * 100

number_input = st.number_input("Select a configuration number:", min_value=1, max_value=10)

# 2. Run the calculation and track the time it takes
if st.button("Run Heavy Computation"):
    start_time = time.time()
    
    with st.spinner("Processing heavy calculations..."):
        result = heavy_ai_calculation(number_input)
        
    end_time = time.time()
    duration = end_time - start_time
    
    st.success(f"Output Result: {result}")
    st.info(f"⏱️ Execution Time: {duration:.2f} seconds")
