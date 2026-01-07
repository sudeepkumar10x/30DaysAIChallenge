# Import python packages
import streamlit as st
import json
import time
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import ai_complete
# from snowflake.cortex import Complete

# Get the current credentials
session = get_active_session()


# --- App UI ---
st.title(":material/post: LinkedIn Post Generator v2")

# Cached LLM Function
@st.cache_data
def call_cortex_llm(prompt_text):
    """Makes a call to Cortex AI with the given prompt."""
    model = "claude-3-5-sonnet"
    df = session.range(1).select(
        ai_complete(model=model, prompt=prompt_text).alias("response")
    )
    
    # Get and parse response
    response_raw = df.collect()[0][0]
    response_json = json.loads(response_raw)
    return response_json


# Input widgets
content = st.text_input("Content URL:", "https://docs.snowflake.com/en/user-guide/views-semantic/overview")
tone = st.selectbox("Tone:", ["Professional", "Casual", "Funny"])
word_count = st.slider("Approximate word count:", 50, 300, 100)

# Generate button
if st.button("Generate Post"):

    # Initialize the status container
    with st.status("Starting engine..", expanded=True) as status:

        # Step 1: Constuct Prompt
        st.write(":material/psychology:Thinking: Analyzing constraints and tone..")
        prompt=f"""
        You are a Linkedin Copywriter and expert. Generate a linkedin post based on the following:

        Tone: {tone}
        Desired Length : Approxipately {word_count} words
        Use content from this URL: {content}

        Use dash for bullet points.
        Use Arrow-> for important pointers
        Add emoji where is important pointers and Humanize the content.
        Keep the conversational style in the post. 

        Also follow these principles of content creation:
        1. Start with a strong, eye catching, honest hook
        Open with a relatable insight, real experience, or reflective statement that stops scrolling — not hype, not clickbait.
        
        2. Use short, skimmable lines
        Write in crisp sentences and line breaks so the post is easy to read on mobile and feels conversational.
        
        3️. Teach through lived experience, not theory
        Share lessons from real work, mentoring conversations, challenges, or mistakes — avoid textbook explanations.
        
        4️. Focus on clarity, consistency, and direction
        Center posts around reducing confusion, avoiding noise, and helping readers make better learning or career decisions.
        
        5️. End with a soft, human CTA
        Invite reflection or conversation (e.g., “comment AI”, “what resonated?”, “let’s learn together”) — not hard selling.
        
        Always keep CTA in new line.
        
        """

        # Step 2 : Call API
        st.write(":material/flash_on: Generating: contacting Snowflake Cortex..")

        # This is the blocking call that takes time
        response = call_cortex_llm(prompt)

        # Step 3: Updates status to complete
        st.write(":material/check_circle: Post generation completed")
        status.update(label="Post Generated Successfully!", state="complete", expanded=False)
        
    # Display Result
    st.subheader("Generated Post:")
    st.markdown(response)