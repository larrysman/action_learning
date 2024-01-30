import streamlit as st

def history():
    col1, col2 = st.columns([15,2])
    with col1:
        st.header('History')
    with col2:
        logout = st.button('Logout', type="primary")
        
    st.header('', divider='rainbow')