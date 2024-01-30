import streamlit as st
from streamlit_option_menu import option_menu
from views import classifyPlant, history, supportedDiseases, overallAnalytics

st.set_page_config(layout="wide")

with st.sidebar:
    selected = option_menu( 
        menu_title = None,
        options = ["Classify New Plant", "History", "Supported Diseases", "Overall Analytics"],
        default_index = 0,
        # orientation = "horizontal"
    )
    
if selected == "Classify New Plant":
    classifyPlant.classify_plant()
if selected == "History":
    history.history()
if selected == "Supported Diseases":
    supportedDiseases.supported_diseases()
if selected == "Overall Analytics":
    overallAnalytics.overall_analytics()
    
        

