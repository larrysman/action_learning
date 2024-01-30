import streamlit as st

def classify_plant():
    col1, col2 = st.columns([10,4])
    with col1:
        st.header('Classify New Plant')
    with col2:
        logout = st.button('Logout', type="primary")
       
        
    st.header('', divider='rainbow')
    
    st.header("Upload Image")
    
    img_file = st.file_uploader("Upload Your Image", type=["img","jpg","png"], accept_multiple_files=False, label_visibility="hidden")