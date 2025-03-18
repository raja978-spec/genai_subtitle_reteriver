import streamlit as st
import re
from audio_file_to_transcription_converter import converter

st.set_page_config(page_title="Movie Search Engine", page_icon="🎬", layout="centered")

st.title("🎥 Movie Search Engine - Upload Audio Query")

if "load_new_data_to_model" not in st.session_state:
    st.session_state.load_new_data_to_model = False
if "train_btn_name" not in st.session_state:
    st.session_state.train_btn_name = "Train Model With New Data"
if "spinner_message" not in st.session_state:
    st.session_state.spinner_message = "Retrieving movie info with this subtitle..."

def switch_model_train_mode():
    if st.session_state.load_new_data_to_model:
        st.session_state.load_new_data_to_model = False
        st.session_state.train_btn_name = "Train Model With New Data"
    else:
        st.session_state.load_new_data_to_model = True
        st.session_state.train_btn_name = "Train Model With Existing Data"

train_btn = st.button(st.session_state.train_btn_name, on_click=switch_model_train_mode)

def format_movie_info(ai_response):
    # Extract movie name, timestamp, and subtitle
    pattern = r"Movie Name: (.*?)\nTime stamp: (.*?)\nSubtitle: (.*)"
    match = re.search(pattern, ai_response, re.DOTALL)

    if match:
        movie_name = match.group(1)
        timestamp = match.group(2).strip()
        subtitle = match.group(3).strip()

        # Default styling for timestamp
        timestamp_display = (
            f"⏰ **Time Stamp:** `{timestamp}`"
            if "not found" not in timestamp.lower() else
            "⏰ **Time Stamp:** ❌ `Not Available`"
        )

        # Corrected Streamlit Markdown with HTML/CSS
        st.markdown(
            f"""
            <div style="background-color: #1e293b; padding: 20px; border-radius: 12px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3); color: #f3f4f6;">
                <h2 style="color: #10b981;">🎬 Movie Name:</h2>
                <h4 style="color: #f97316; margin-top: -10px;">{movie_name}</h4>
                <h4 style="color: #facc15;">{timestamp_display}</h4>
                <h4 style="color: #60a5fa; margin-bottom: 5px;">💬 Subtitle:</h4>
                <blockquote style="font-size: 1.2em; background: #334155; color: #f3f4f6; padding: 10px; border-radius: 8px;">
                    {subtitle}
                </blockquote>
            </div>
            """,
            unsafe_allow_html=True
        )

def get_response_from_model(user_prompt, load_new_data_to_model_db):
    from generate_data import generated_subtitle, no_of_knowledge_base_data, no_of_available_knowledge_base_data
    start_range = len(no_of_available_knowledge_base_data) + 1
    end_range = len(no_of_available_knowledge_base_data) + 3

    if start_range != no_of_knowledge_base_data[0] and load_new_data_to_model_db:
        generated_subtitle(start_range, end_range)

    from gemini_emdeddings_subtitle_finder import subtitle_finder
    ai_response = subtitle_finder(user_prompt, load_new_data_to_model_db)
    return ai_response

user_prompt = converter()

if user_prompt:
    is_load_new_data_to_model = st.session_state.load_new_data_to_model
    if is_load_new_data_to_model:
        st.session_state.spinner_message = "Model Takes Time To Learn From Expanded Data. Please Wait..."

    with st.spinner(st.session_state.spinner_message):
        ai_response = get_response_from_model(user_prompt, is_load_new_data_to_model)
        format_movie_info(ai_response)
