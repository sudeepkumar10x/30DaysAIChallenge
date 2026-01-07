# Import python packages
import streamlit as st
import json
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import ai_complete


# Get the current credentials
session = get_active_session()

## DAY 1 ####

# Query and display Snowflake version
version = session.sql("SELECT CURRENT_VERSION()").collect()[0][0]

# Show results
st.success(f"Successfully connected! Snowflake Version: {version}")

# Footer
st.divider()
st.caption("Day 2: Hello, Cortex! | 30 Days of AI")