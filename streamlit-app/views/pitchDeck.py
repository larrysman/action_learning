import streamlit as st


# Function to display a particular slide
def show_slide(slide_number):
    if slide_number == 1:
        st.image('pitch_deck/Slide1.jpg', width=1400)
    elif slide_number == 2:
        st.image('pitch_deck/Slide2.jpg', width=1400)
    elif slide_number == 3:
        st.image('pitch_deck/Slide3.jpg', width=1400)
    elif slide_number == 4:
        st.image('pitch_deck/Slide4.jpg', width=1400)
    elif slide_number == 5:
        st.image('pitch_deck/Slide5.jpg', width=1400)
    elif slide_number == 6:
        st.image('pitch_deck/Slide6.jpg', width=1400)
    elif slide_number == 7:
        st.image('pitch_deck/Slide7.jpg', width=1400)
    elif slide_number == 8:
        st.image('pitch_deck/Slide8.jpg', width=1400)
    elif slide_number == 9:
        st.image('pitch_deck/Slide9.jpg', width=1400)

# Streamlit app main function
def pitch_deck():
    st.title("Always Green Pitch Deck")

    # Session state to keep track of slide number
    if 'slide_number' not in st.session_state:
        st.session_state.slide_number = 1

    # Display the current slide
    show_slide(st.session_state.slide_number)

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Previous'):
            if st.session_state.slide_number > 1:
                st.session_state.slide_number -= 1
    with col2:
        if st.button('Next'):
            if st.session_state.slide_number < 9:
                st.session_state.slide_number += 1

if __name__ == "__main__":
    pitch_deck()