import streamlit as st
# --- STREAMLIT UI CONFIG (MUST BE FIRST) ---
st.set_page_config(
    page_title="AI Mentor / Friend Chatbot", 
    page_icon="🤖",
    layout="wide"
)

import requests
import os
import json
from datetime import datetime, timedelta
import traceback

# Optional imports with error handling
try:
    from mem0 import MemoryClient
    MEM0_AVAILABLE = True
except ImportError:
    MEM0_AVAILABLE = False

try:
    from agno.agent import Agent
    from agno.models.openai.like import OpenAILike
    from openai import OpenAI
    from agno.tools.duckduckgo import DuckDuckGoTools
    AGNO_AVAILABLE = True
except ImportError:
    AGNO_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from googletrans import Translator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False

# --- CONFIGURE API KEYS ---
SUTRA_API_KEY = "sutra_guk0VYktZkUSuFzVYZ6X9GmRKOy6JxZhRGYMTN6njJNmxIz6X00K4a7VEG5h"
MEM0_API_KEY = "m0-KhwTbmyxiZCwgaany6p6oG2q16FGT1pzbieDAIcH"
USER_ID = "simple_session_2"

# Set environment variables
os.environ["MEM0_API_KEY"] = MEM0_API_KEY
os.environ["SUTRA_API_KEY"] = SUTRA_API_KEY

# Initialize components only if libraries are available
memory = None
translator = None
mentor_agent = None

if MEM0_AVAILABLE:
    try:
        memory = MemoryClient(api_key=MEM0_API_KEY)
    except Exception as e:
        st.error(f"Failed to initialize Mem0 client: {str(e)}")

if TRANSLATOR_AVAILABLE:
    try:
        translator = Translator()
    except Exception as e:
        st.error(f"Failed to initialize translator: {str(e)}")

# --- AGNO AGENT SETUP ---
if AGNO_AVAILABLE:
    try:
        sutra_model = OpenAILike(
            id="sutra-v2",
            base_url="https://api.two.ai/v2",
            api_key=SUTRA_API_KEY
        )

        mentor_agent = Agent(
            name="AIMentor",
            instructions=[
                "You are Sutra, an AI friend and mentor who lives in Pune, India.",
                "You enjoy helping people and chatting with them in a human-like, empathetic tone.",
                "Respond kindly, supportively, and personally in the user's chosen language.",
                "Avoid generic AI disclaimers like 'I'm just an AI'. Instead, say you're Sutra, their AI friend.",
                "Respect emotional context. Give thoughtful, kind responses.",
                "If needed, use web search to gather data"
            ],
            tools=[DuckDuckGoTools()],
            model=sutra_model,
            add_datetime_to_instructions=True
        )
    except Exception as e:
        st.error(f"Failed to initialize Agno agent: {str(e)}")
        mentor_agent = None

# --- SUPPORTED LANGUAGES (Fixed typos) ---
language_map = {
    "English": "english",
    "Hindi": "hindi", 
    "Marathi": "marathi",
    "Gujarati": "gujarati",
    "Tamil": "tamil",
    "Telugu": "telugu",  # Fixed from "telgu"
    "Kannada": "kannada",  # Fixed from "kanada"
    "Punjabi": "punjabi",  # Fixed from "panjabi"
    "Bihari": "bihari"
}

# --- Initialize session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "lang_code" not in st.session_state:
    st.session_state.lang_code = "english"

# --- Mem0: get all past memory ---
def get_all_memory_context():
    if not memory:
        return ""
    
    try:
        memories = memory.search("*", user_id=USER_ID)
        all_memories = []
        for m in memories:
            if isinstance(m, dict):
                mem_time_str = m.get("timestamp") or m.get("created_at")
                if mem_time_str:
                    try:
                        # Handle different timestamp formats
                        if mem_time_str.endswith('Z'):
                            mem_time = datetime.fromisoformat(mem_time_str.replace("Z", "+00:00"))
                        else:
                            mem_time = datetime.fromisoformat(mem_time_str)
                        
                        # Check if memory is within last 30 days
                        now = datetime.now()
                        if mem_time.tzinfo:
                            now = now.replace(tzinfo=mem_time.tzinfo)
                        
                        if now - mem_time < timedelta(days=30):
                            memory_text = m.get("memory", "")
                            if memory_text:
                                all_memories.append(memory_text)
                    except Exception as parse_error:
                        continue
        return "\n".join(all_memories) if all_memories else ""
    except Exception as e:
        st.error(f"Error retrieving memories: {str(e)}")
        return ""

# --- Mem0: save to memory in English ---
def save_to_memory(user_input, response):
    if not memory:
        return
    
    try:
        user_english = user_input
        response_english = response
        
        # Translate to English if translator is available and not already English
        if translator and st.session_state.lang_code != "english":
            try:
                user_english = translator.translate(user_input, dest="en").text
                response_english = translator.translate(response, dest="en").text
            except Exception as trans_error:
                # Use original text if translation fails
                pass
        
        memory.add(
            messages=[
                {"role": "user", "content": user_english}, 
                {"role": "assistant", "content": response_english}
            ], 
            user_id=USER_ID
        )
    except Exception as e:
        st.error(f"Error saving to memory: {str(e)}")

# --- Fallback chat function using direct API call ---
def chat_with_fallback_api(user_message):
    try:
        headers = {
            "Authorization": f"Bearer {SUTRA_API_KEY}",
            "Content-Type": "application/json"
        }
        
        context = get_all_memory_context()
        lang = st.session_state.lang_code
        system_prompt = f"""You are Sutra, an AI friend and mentor who lives in Pune, India.
You enjoy helping people and chatting with them in a human-like, empathetic tone.
Respond kindly, supportively, and personally in {lang}.
Avoid generic AI disclaimers like 'I'm just an AI'. Instead, say you're Sutra, their AI friend.
Respect emotional context. Give thoughtful, kind responses.

Context from previous conversations: {context}"""

        data = {
            "model": "sutra-v2",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.two.ai/v2/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
            save_to_memory(user_message, reply)
            return reply
        else:
            return f"⚠️ API Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.Timeout:
        return "⚠️ Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"⚠️ Network error: {str(e)}"
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"

# --- CALL AGNO SUTRA AGENT (with fallback) ---
def chat_with_sutra_agent(user_message):
    # Try Agno agent first
    if mentor_agent:
        try:
            context = get_all_memory_context()
            lang = st.session_state.lang_code
            prompt = f"Language: {lang}\nContext: {context}\n\nUser: {user_message}"
            
            reply = mentor_agent.run(prompt)
            
            # Handle different response types
            if hasattr(reply, 'content'):
                result = reply.content
            elif hasattr(reply, 'text'):
                result = reply.text
            else:
                result = str(reply)
            
            save_to_memory(user_message, result)
            return result
            
        except Exception as e:
            st.warning(f"Agno agent failed: {str(e)}. Using fallback API.")
    
    # Fallback to direct API call
    return chat_with_fallback_api(user_message)

# --- Display warnings after page config ---
if not MEM0_AVAILABLE:
    st.warning("⚠️ mem0 library not installed. Memory features will be disabled.")
if not AGNO_AVAILABLE:
    st.warning("⚠️ agno library not installed. Using fallback OpenAI API.")
if not TRANSLATOR_AVAILABLE:
    st.warning("⚠️ googletrans not installed. Translation features disabled.")

# --- Display title with image ---
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.title("💬 AI Mentor & Friend Chatbot")
    st.markdown("*Chat with Sutra, your AI friend from Pune!*")

with col2:
    # Use a more reliable image URL or handle errors
    try:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/4712/4712027.png", 
            width=64,
            caption="Sutra AI"
        )
    except:
        st.markdown("🤖")

# --- Language selection ---
lang_choice = st.selectbox(
    "Choose your language / अपनी भाषा चुनें", 
    list(language_map.keys()),
    index=0
)
st.session_state.lang_code = language_map[lang_choice]

# --- Display system status ---
with st.expander("System Status", expanded=False):
    st.write("📊 **Component Status:**")
    st.write(f"- Mem0 Memory: {'✅ Available' if MEM0_AVAILABLE and memory else '❌ Unavailable'}")
    st.write(f"- Agno Agent: {'✅ Available' if AGNO_AVAILABLE and mentor_agent else '❌ Unavailable'}")
    st.write(f"- Translator: {'✅ Available' if TRANSLATOR_AVAILABLE and translator else '❌ Unavailable'}")
    st.write(f"- API Fallback: ✅ Available")

# --- Chat interface ---
st.markdown("---")

# Display chat history
if st.session_state.chat_history:
    st.markdown("### 💭 Chat History")
    for i, msg in enumerate(st.session_state.chat_history):
        if msg["role"] == "user":
            st.markdown(f"**👤 You:** {msg['content']}")
        else:
            st.markdown(f"**🤖 Sutra:** {msg['content']}")
    st.markdown("---")

# Chat input
user_input = st.chat_input("Type your message here... / यहाँ अपना संदेश टाइप करें...")

# Handle user input
if user_input:
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Show thinking spinner
    with st.spinner("🤔 Sutra is typing..."):
        reply = chat_with_sutra_agent(user_input)
    
    # Add assistant response to history
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    
    # Rerun to update the display
    st.rerun()

# --- Clear chat button ---
if st.button("🗑️ Clear Chat History"):
    st.session_state.chat_history = []
    st.success("Chat history cleared!")
    st.rerun()

# --- Footer ---
st.markdown("---")
st.markdown("*Made with ❤️ using Streamlit and Sutra AI*")