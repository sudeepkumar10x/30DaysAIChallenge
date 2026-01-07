# Import python packages
import streamlit as st
import json
import time
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import ai_complete
# from snowflake.cortex import Complete

# Get the current credentials
session = get_active_session()

st.title(":material/cached: Caching your App")

@st.cache_data
def call_cortex_llm(prompt_text):
    model = "claude-3-5-sonnet"
    df = session.range(1).select(
        ai_complete(model=model, prompt=prompt_text).alias("response")
    )
    
    # Get and parse response
    response_raw = df.collect()[0][0]
    response_json = json.loads(response_raw)
    return response_json

prompt = st.text_input("Enter your prompt", "Why is the sky blue?")

if st.button("Submit"):
    start_time = time.time()
    response = call_cortex_llm(prompt)
    end_time = time.time()
    
    st.success(f"*Call took {end_time - start_time:.2f} seconds*")
    st.write(response)

# Footer
st.divider()
st.caption("Day 4: Caching your App | 30 Days of AI")