
import streamlit as st

st.set_page_config(page_title="AI Subtitle Retriever", page_icon="📚", layout="centered")

st.title("🤖 AI Subtitle Retriever")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "load_new_data_to_model" not in st.session_state:
    st.session_state.load_new_data_to_model = False
if 'train_btn_name' not in st.session_state:
     st.session_state.train_btn_name = "Train Model With New Data"
if 'spinner_message' not in st.session_state:
     st.session_state.spinner_message = "Retrieving..."

def switch_model_train_mode():
     if st.session_state.load_new_data_to_model == True:
         st.session_state.load_new_data_to_model = False
         st.session_state.train_btn_name = 'Train Model With New Data'
     else:
         st.session_state.load_new_data_to_model = True
         st.session_state.train_btn_name = 'Train Model With Existing Data'
    
train_btn = st.button(st.session_state.train_btn_name, on_click=switch_model_train_mode)

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


def get_response_from_model(user_prompt, load_new_data_to_model_db):
      from generate_data import generated_subtitle, no_of_knowledge_base_data, no_of_available_knowledge_base_data
      start_range = len(no_of_available_knowledge_base_data)+1
      end_range = len(no_of_available_knowledge_base_data)+3

      if start_range != no_of_knowledge_base_data[0] and load_new_data_to_model_db: 
           generated_subtitle(start_range, end_range)
           print('Inside.....', start_range, end_range)
      from gemini_ai_subtitle_finder import subtitle_finder
      ai_response = subtitle_finder(user_prompt,load_new_data_to_model_db)
      return ai_response

print(st.session_state.load_new_data_to_model)
user_prompt = st.chat_input('Enter a subtitle line to retrieve')

if user_prompt:
        with st.chat_message('user'):
            st.markdown(user_prompt)
        st.session_state.messages.append({'role':'user','content':user_prompt})

        is_load_new_data_to_model = st.session_state.load_new_data_to_model
        
        if(is_load_new_data_to_model):
             st.session_state.spinner_message = 'Model Takes Time To Learn From Expanded Data Please Wait.'
        
        with st.spinner(st.session_state.spinner_message):
             ai_response = get_response_from_model(user_prompt, is_load_new_data_to_model)
             text_response = ''
             for page,score in ai_response:
                  print(page.page_content)
                  text_response += page.page_content

        with st.chat_message('ai'):
            st.markdown(text_response)
        st.session_state.messages.append({'role':'ai','content':text_response})


    
    
   


