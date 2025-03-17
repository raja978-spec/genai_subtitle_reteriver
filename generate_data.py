import sqlite3
import zipfile
import io
import pandas as pd
import os

con = sqlite3.connect('eng_subtitles_database.db')

df = pd.read_sql_query('SELECT * FROM zipfiles', con)


def decode_method(binary_data):
    with io.BytesIO(binary_data) as f:
        with zipfile.ZipFile(f, 'r') as zip_file:
            subtitle_content = zip_file.read(zip_file.namelist()[0])
    
    return subtitle_content.decode('latin-1')

extracted_subtitles = df['content'].apply(decode_method)
no_of_knowledge_base_data = df['content'].shape
no_of_available_knowledge_base_data = os.listdir(os.path.join('dataset'))

def generated_subtitle(start_range, end_range):
    df['file_content'] = extracted_subtitles
    file_no =start_range
    print('Content to be expand',df['file_content'][start_range:end_range])
    for data in df['file_content'][start_range:end_range]:
        with open(f'dataset/subtitle_{file_no}.srt','w', encoding='utf-8') as file:
            file.write(data)
        print(f'file {file_no} written....')
        file_no += 1
    return 1
