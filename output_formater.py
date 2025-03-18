import re
from typing import List, Tuple

def format_output(data: List[Tuple[object, float]]) -> str:
    for item in data:
        doc, _ = item
        movie_info = doc.metadata['source']

        # Extract movie name and year
        start = movie_info.find('\\') + 1
        end = movie_info.rfind('.eng')
        movie_name_year = movie_info[start:end].replace('.', ' ').title()

        # Extract timestamp from page_content
        page_content = doc.page_content.strip()
        timestamp_match = re.search(r"(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})", page_content)
        timestamp = timestamp_match.group(1) if timestamp_match else "Timestamp not found"

        # Extract subtitle, removing the timestamp
        subtitle = re.sub(r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", "", page_content).strip()

        return f"Movie Name: {movie_name_year}\nTime stamp: {timestamp}\nSubtitle: {subtitle}"

