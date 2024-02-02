import streamlit as st
import psycopg2
import os


db_params = {
    'dbname': 'plant_disease',
    'user': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'password': "Jerry@126"
}

# Streamlit app layout

# Function to connect to PostgreSQL and fetch data
def fetch_data():
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Example query
        cursor.execute("SELECT plant_name FROM agriculture_plant")
        data = cursor.fetchall()

        return data

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        if connection:
            connection.close()

# Function to create subfolder and save images
def save_images(class_name, images):
    # Create a new directory for the class
    new_dir_path = os.path.join('support_plants', class_name)
    os.makedirs(new_dir_path, exist_ok=True)

    # Save each image in the new directory
    for i, image in enumerate(images):
        image_path = os.path.join(new_dir_path, f"image{i + 1}.{image.type.split('/')[1]}")
        with open(image_path, 'wb') as f:
            f.write(image.getbuffer())

def add_new_plant():
    st.header('Add New Plant to Database')
    st.header('', divider='rainbow')
    # User input for class name (no spaces allowed)
    class_name = st.text_input("Enter New Class Name:")

    # Dropdown menu for disease type
    disease_types = [
        "no disease", "bacterial", "black spot", "blight", "canker", "cercospora", "cordana", "curl",
    "dot", "greening", "measles", "mite", "mosaic", "mummification", "pestalotiopsis",
    "powdery mildew", "rot", "rust", "scab", "scorch", "septoria", "sigatoka", "target"
    ]
    selected_disease_type = st.selectbox("Choose Disease Type (select 'no disease' for healthy plant)", disease_types)

    # File uploader for class support images (exactly 5 images required)
    uploaded_images = st.file_uploader("Upload 5 Class Support Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    # Button to add the entry
    if st.button("Confirm"):
        if class_name and len(uploaded_images) == 5:
            try:
                # Save images to the new subfolder
                save_images(class_name, uploaded_images)

                connection = psycopg2.connect(**db_params)
                cursor = connection.cursor()

                # Insert the new class, images, and disease type into the database
                cursor.execute(
                    "INSERT INTO agriculture_plant (plant_name, disease_type, image_one, image_two, image_three, image_four, image_five) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (class_name, selected_disease_type, uploaded_images[0].read(), uploaded_images[1].read(),
                    uploaded_images[2].read(), uploaded_images[3].read(), uploaded_images[4].read())
                )

                connection.commit()
                st.success(f"Added: Class {class_name} with disease type {selected_disease_type} and 5 images to the database and saved images to the folder")

            except Exception as e:
                st.error(f"Error: {e}")

            finally:
                if connection:
                    connection.close()

        else:
            if not class_name:
                st.warning("Please provide a Class Name.")
            if len(uploaded_images) != 5:
                st.warning("Please upload exactly 5 images.")

    # Display the current list of plant names, including the new one
    st.header("Plant Classes:")
    plant_names = fetch_data()

    # Use st.empty() to create a placeholder for the dynamic list
    plant_names_placeholder = st.empty()

    # Continuously update the list without refreshing the entire page
    while True:
        plant_names = fetch_data()
        plant_names_list = [name[0] for name in plant_names]
        plant_names_text = "\n".join(plant_names_list)
        plant_names_placeholder.text(plant_names_text)