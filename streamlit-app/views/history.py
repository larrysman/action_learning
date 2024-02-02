import streamlit as st
import psycopg2
from PIL import Image
import io


db_params = {
    'dbname': 'plant_disease',
    'user': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

def fetch_data():
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        cursor.execute("SELECT image_file, prediction, confidence, disease_type, predicted_time FROM saved_prediction ORDER BY predicted_time DESC")
        data = cursor.fetchall()

        return data

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        if connection:
            connection.close()

def convert_binary_to_image(binary_data):
    if binary_data:
        return Image.open(io.BytesIO(binary_data))
    return None

rows_per_page = 5

def history():
    st.header('Prediction History')
    st.header('', divider='rainbow')
    
    past_prediction = fetch_data()

    for i in range(len(past_prediction)):
        row = list(past_prediction[i])
        row[0] = convert_binary_to_image(row[0])
        row[2] = round(row[2], 2)
        past_prediction[i] = row

    total_rows = len(past_prediction)
    total_pages = total_rows // rows_per_page + (total_rows % rows_per_page > 0)

    # Initialize current_page in session state if it doesn't exist
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 0

    current_page = st.session_state['current_page']

    start_idx = current_page * rows_per_page
    end_idx = min(start_idx + rows_per_page, total_rows)

    # Display rows for the current page
    for row in past_prediction[start_idx:end_idx]:
        cols = st.columns([1, 3])
        with cols[0]:
            st.image(row[0], width=100)
        with cols[1]:
            st.write(f"Classification: {row[1]}")
            st.write(f"Confidence: {row[2]}%")
            st.write(f"Type: {row[3]}")
            st.write(f"Timestamp: {row[4]}")
        st.header('', divider='rainbow')

    # Pagination buttons
    if total_pages > 1:
        col1, col2 = st.columns(2)
        with col1:
            if current_page > 0:
                prev = st.button("Previous Page")
                if prev:
                    st.session_state.current_page -= 1
                    st.experimental_rerun()

        with col2:
            if current_page + 1 < total_pages:
                next = st.button("Next Page")
                if next:
                    st.session_state.current_page += 1
                    st.experimental_rerun()

if __name__ == "__main__":
    history()
