import streamlit as st

def supported_diseases():
    col1, col2 = st.columns([15,2])
    with col1:
        st.header('Supported Diseases')
    with col2:
        logout = st.button('Logout', type="primary")
    st.header('', divider='rainbow')