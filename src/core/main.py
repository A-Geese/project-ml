import streamlit as st

# Optional: If integrating with OpenAI
# import openai
# import os
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Set page configuration
st.set_page_config(page_title="Debate Chat Interface", page_icon="💬")

st.title("💬 Debate Chat Interface")

# Inject CSS for styling
st.markdown(
    """
    <style>
    /* Chat container */
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding-right: 15px;
    }

    /* Chat message */
    .chat-message {
        display: flex;
        margin-bottom: 10px;
    }

    /* User message */
    .chat-message.user .message-content {
        margin-left: auto;
        background-color: #DCF8C6; /* Light green bubble */
        color: #000;
    }

    /* Assistant message */
    .chat-message.assistant .message-content {
        margin-right: auto;
        background-color: #FFFFFF; /* White bubble */
        color: #000;
    }

    /* Message content */
    .message-content {
        max-width: 70%;
        padding: 10px;
        border-radius: 15px;
        position: relative;
        word-wrap: break-word;
    }

    /* Optional: Add a background color to the page */
    body {
        background-color: #E5DDD5;
    }

    </style>
    """
)

# Initialize message history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display existing messages
with st.container():
    for message in st.session_state["messages"]:
        role = message["role"]
        content = message["content"]

        message_html = f"""
        <div class="chat-message {role}">
            <div class="message-content">
                {content}
            </div>
        </div>
        """

        st.markdown(message_html, unsafe_allow_html=True)

# User input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...")
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input:
    st.session_state["messages"].append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    # Generate assistant's response
    response = f"You said: {user_input}"

    # Optional: Use OpenAI API for assistant's response
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=st.session_state['messages']
    # ).choices[0].message.content

    st.session_state["messages"].append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    # Rerun the app to display the new messages
    st.rerun()
