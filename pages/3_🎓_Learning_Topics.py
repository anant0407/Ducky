import asyncio

import streamlit as st
import helpers.sidebar
import helpers.util
import services.prompts
import services.llm

st.set_page_config(
    page_title="Learning Topics",
    page_icon="🎓",
    layout="wide"
)

st.header("Learning Topics")

helpers.sidebar.show()

learner_level = st.selectbox("I'd like my answer as if I were a:",
                                     ["Toddler", "High School Student", "College Student", "Graduate", "Retiree"])

response_format = st.selectbox("I'd like my answer as a:",
                                       ["set of brief bullet points", "article", "online course syllabus"])

# answer_button_sb = st.button("Tell me", type="primary", key="answer_button_sb")

st.markdown("<br>", unsafe_allow_html=True)

topic = st.text_input("What would you like to learn about?", placeholder="Ask about a coding topic here..")
answer_button = st.button("Answer", type="primary")

# if answer_button or answer_button_sb:
#     advice = st.markdown("### Ducky Teaching...")
#     learning_prompt = services.prompts.learning_prompt(learner_level, response_format, topic)
#     messages = services.llm.create_conversation_starter(services.prompts.system_learning_prompt())
#     messages.append({"role": "user", "content": learning_prompt})
#     asyncio.run(helpers.util.run_conversation(messages, advice))

if answer_button:
    advice = st.markdown("### Ducky Teaching...")
    learning_prompt = services.prompts.learning_prompt(learner_level, response_format, topic)
    messages = services.llm.create_conversation_starter(services.prompts.system_learning_prompt())
    messages.append({"role": "user", "content": learning_prompt})
    asyncio.run(helpers.util.run_conversation(messages, advice))

# Button to reset the page
if st.button("Reset Page"):
    user_code = ""
    error_string = ""
    modification_request = ""
