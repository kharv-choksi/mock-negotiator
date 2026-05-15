import streamlit as st
from anthropic import Anthropic

# --- PAGE SETUP ---
st.set_page_config(page_title="Mock Negotiator", page_icon="🤝")
st.title("🤝 The Mock Negotiator")
st.markdown("Practice your PM salary negotiations and stakeholder pushback.")

# --- SIDEBAR & AUTH ---
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Anthropic API Key:", type="password")
    st.markdown("[Get an API key here](https://console.anthropic.com/)")
    
    st.divider()
    
    # NEW: Feedback Button in the sidebar
    st.header("Feedback")
    st.write("Done negotiating? Get your score.")
    get_feedback = st.button("🏁 End Negotiation & Get Feedback", type="primary")

# --- MVP SCOPE: THE SCENARIO & PERSONA ---
st.subheader("Context")
col1, col2 = st.columns(2)

with col1:
    persona = st.selectbox(
        "Who are you talking to?",
        ["The Stingy Big Tech Recruiter", "The Stubborn Engineering Lead", "The Skeptical VP of Product"]
    )

with col2:
    scenario = st.text_area(
        "What is the situation?", 
        "I have a $110k offer but want $120k + a sign-on bonus. The recruiter says budgets are locked."
    )

st.divider()

# --- CHAT INTERFACE STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat if context changes
if st.button("Reset Conversation"):
    st.session_state.messages = []
    st.rerun()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- NEW: THE FEEDBACK ENGINE ---
if get_feedback:
    if not api_key:
        st.sidebar.error("⚠️ API Key required.")
    elif len(st.session_state.messages) < 2:
        st.sidebar.warning("⚠️ Have a conversation first before asking for feedback!")
    else:
        with st.spinner("Analyzing your negotiation tactics..."):
            client = Anthropic(api_key=api_key)
            
            # We create a new system prompt telling Claude to act as a coach, not the opponent
            coach_prompt = f"""
            You are an expert negotiation coach for Product Managers. 
            Review the chat history where the user was negotiating with a '{persona}' about this scenario: '{scenario}'.
            
            Provide the following format EXACTLY:
            ### Final Score: [Insert Score out of 100]
            
            **What you did well:**
            - [Bullet 1]
            - [Bullet 2]
            
            **Areas for improvement:**
            - [Bullet 1]
            - [Bullet 2]
            
            Keep it concise, actionable, and brutally honest.
            """
            
            # We append a hidden system request to the existing chat history to trigger the evaluation
            eval_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            eval_messages.append({"role": "user", "content": "The negotiation is over. Please evaluate my performance based on your instructions."})
            
            response = client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=400,
                system=coach_prompt,
                messages=eval_messages
            )
            
            # Display the feedback beautifully in the main UI
            st.divider()
            st.success("Analysis Complete!")
            st.markdown(response.content[0].text)

# --- THE CHAT ENGINE ---
if prompt := st.chat_input("Make your pitch..."):
    if not api_key:
        st.warning("⚠️ Please enter your Anthropic API key in the sidebar to start negotiating.")
        st.stop()

    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # System prompt to enforce the persona
    system_prompt = f"""
    You are playing the role of '{persona}'. 
    The specific scenario is: '{scenario}'. 
    
    Rules for you:
    1. Be highly realistic and push back appropriately. 
    2. Do NOT be overly helpful. Make the user work for it.
    3. Keep your responses concise, like a real Slack message or verbal conversation.
    4. Never break character.
    """

    client = Anthropic(api_key=api_key)

    # Call Claude and stream the response
    with st.chat_message("assistant"):
        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=300,
            system=system_prompt,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )
        response = message.content[0].text
        st.markdown(response)

    # Append AI message
    st.session_state.messages.append({"role": "assistant", "content": response})