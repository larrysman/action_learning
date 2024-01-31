import streamlit as st
from streamlit_modal import Modal
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
import requests

st.set_page_config(layout="wide")

signup_modal = Modal(
    "SignUp", 
    key="-signup_modal",
    
    # Optional
    padding=20,    # default value
    max_width=744  # default value
)

signin_modal = Modal(
    "SignIn", 
    key="demo-signin_modal",
    
    # Optional
    padding=20,    # default value
    max_width=744  # default value
)


def home_page():
    col1, col2 = st.columns([15,2])
    with col1:
        st.header('Disease Identification in Agriculture')
    with col2:
        col1, col2 = st.columns([1,1])
        with col1:
            signin = st.button('SignIn')
        with col2:
            signup = st.button('SignUp', type="primary")
        
    st.header('', divider='rainbow')
    
    if signin:
        signin_modal.open()
    if signin_modal.is_open():
        with signin_modal.container():
            email = st.text_input("Email Id")
            password = st.text_input("Password", type="password")
            
            login_data = {
                "email" : email,
                "password" : password
            }

            if st.button("Login"):
                if email == "demo" and password == "password":
                    signin_modal.close()
                else:
                    st.error("Invalid Username or Password")
    if signup:
        signup_modal.open()
    if signup_modal.is_open():
        with signup_modal.container():
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email Id")
            password = st.text_input("Password", type="password")
            hashed_pswrd = stauth.Hasher([password]).generate()
            
            user_data = {
                "first_name" : first_name,
                "last_name" : last_name,
                "email" : email,
                "password" : hashed_pswrd[0]
            }

            if st.button("Sign Up"):
                save_user = requests.post("http://127.0.0.1:8000/signup", json=user_data) 
                st.success(save_user.text)
                signup_modal.close()

            
    st.header("Introduction")
    st.write("With the global population on the rise and the increasing demand for food, sustainable agricultural practices are more crucial than ever. The application of few-shot learning in detecting plant diseases is a novel approach that addresses the twin challenges of limited data availability and the need for high accuracy in disease identification. This application is a response to the pressing demand for innovative solutions that can ensure crop health, reduce losses, and contribute to overall food security.")
    

def login_page():
    st.title("Sign In")
    email = st.text_input("Email Id")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email == "demo" and password == "password":
            st.success("Login Successful!")
        else:
            st.error("Invalid Username or Password")

def signup_page():
    st.title("Sign Up")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email Id")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        # Implement user registration logic here (e.g., store in a database)
        st.success("Account created successfully!")
    
def main():
    home_page()

if __name__ == "__main__":
    main()
