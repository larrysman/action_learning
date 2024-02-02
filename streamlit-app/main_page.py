import streamlit as st
from streamlit_modal import Modal
from streamlit_option_menu import option_menu
from views import pitchDeck, addNewPlant, classifyPlant, history, overallAnalytics


#st.set_page_config(layout="wide")

# signup_modal = Modal(
#     "SignUp", 
#     key="-signup_modal",
    
#     # Optional
#     padding=20,    # default value
#     max_width=744  # default value
# )

# signin_modal = Modal(
#     "SignIn", 
#     key="demo-signin_modal",
    
#     # Optional
#     padding=20,    # default value
#     max_width=744  # default value
# )

def main_page():
    # st.set_page_config(layout="centered")
    # if signin_modal.is_open():
    #     with signin_modal.container():
    #         st.header('', divider='rainbow')
    #         email = st.text_input("Email Id")
    #         password = st.text_input("Password", type="password")
            
    #         login_data = {
    #             "email" : email,
    #             "password" : password
    #         }

    #         if st.button("Login", type="primary"):
    #             if email == "demo" and password == "helloworld":
    #                 signin_modal.close()
    #             else:
    #                 st.error("Invalid Username or Password")
    #         st.header('', divider='rainbow')
            
    #         st.button("Create an Account", type="primary")

    with st.sidebar:
        selected = option_menu( 
            menu_title = None,
            options = ["Pitch Deck", "Classify Plant", "Add New Plant", "History", "Overall Analytics"],
            default_index = 0,
            # orientation = "horizontal"
        )
        
    # if selected == "Main":
    if selected == "Pitch Deck":
        pitchDeck.pitch_deck()    
    if selected == "Classify Plant":
        classifyPlant.classify_plant()
    if selected == "History":
        history.history()
    if selected == "Add New Plant":
        addNewPlant.add_new_plant()
    if selected == "Overall Analytics":
        overallAnalytics.overall_analytics()
    
    # signin_modal.open() 
        
    

if __name__ == "__main__":
    main_page()
    
        

