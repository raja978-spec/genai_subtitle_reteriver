import whisper
import streamlit as st
import tempfile

def converter():
    model = whisper.load_model("small")
    
    def transcribe_audio(file_path):
        result = model.transcribe(file_path, task="translate")  # Translates to English
        return result["text"]
    
    audio_file = st.file_uploader("Upload a 2-minute audio clip", type=["wav", "mp3", "ogg", "mpeg"])
    
    
    if audio_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_file.read())  # Write file content
            temp_audio_path = temp_audio.name  # Get the temp file path
            st.audio(temp_audio_path)
            
            with st.spinner('Converting audio to text file..'):
                transcription = transcribe_audio(temp_audio_path)
                st.success("Transcription:")
                st.write(transcription)
                return transcription

