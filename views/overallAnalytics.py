import streamlit as st

def overall_analytics():
    col1, col2 = st.columns([15,2])
    with col1:
        st.header('Overall Analytics')
    with col2:
        logout = st.button('Logout', type="primary")
    st.header('', divider='rainbow')