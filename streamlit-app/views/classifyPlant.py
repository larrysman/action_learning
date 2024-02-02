import streamlit as st
import psycopg2
import os
import torch
import numpy as np
from PIL import Image
import torchvision
import torch.nn as nn
import torch.nn.functional as F
from io import BytesIO
import requests


# Define the Image2Vector model architecture
class Image2Vector(nn.Module):
    def __init__(self):
        super(Image2Vector, self).__init__()
        self.input_block = nn.Sequential(nn.Conv2d(3, 64, 3, padding=1),
                                         nn.BatchNorm2d(64),
                                         nn.ReLU(),
                                         nn.MaxPool2d(2))
        self.conv_block = nn.Sequential(nn.Conv2d(64, 64, 3, padding=1),
                                        nn.BatchNorm2d(64),
                                        nn.ReLU(),
                                        nn.MaxPool2d(2))
    
    def forward(self, x):
        x = self.input_block(x)
        x = self.conv_block(x)
        x = self.conv_block(x)
        x = self.conv_block(x)
        out = x.view(x.size(0), -1)
        return out

# Define the ProtoNet model architecture
class ProtoNet(nn.Module):
    def __init__(self):
        super(ProtoNet, self).__init__()
        self.encoder = Image2Vector()

    def forward(self, support, queries, k_shot, n_way):
        n_queries = queries.shape[0]
        x = torch.cat([support, queries], 0)
        z = self.encoder(x)
        z_dim = z.size(-1)

        protos = z[:n_way * k_shot].view(n_way, k_shot, z_dim).mean(1)
        query_z = z[n_way * k_shot:]

        distances = self.euclidean_dist(query_z, protos)
        softmax_probs = F.softmax(-distances, dim=1)
        _, y_hat = softmax_probs.max(1)

        return y_hat, softmax_probs[torch.arange(n_queries), y_hat]        

    @staticmethod
    def euclidean_dist(x, y):
        n = x.size(0)
        m = y.size(0)
        d = x.size(1)
        x = x.unsqueeze(1).expand(n, m, d)
        y = y.unsqueeze(0).expand(n, m, d)
        return torch.pow(x - y, 2).sum(2)

# Function to load the trained model
def load_model(model_path):
    model = ProtoNet()
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model

# Function to process images in a directory
def process_images_in_directory(directory):
    images = []
    labels = []
    label_names = [name for name in os.listdir(directory) if name != '.DS_Store']
    
    for label in label_names:
        label_path = os.path.join(directory, label)
        for img_name in os.listdir(label_path):
            if img_name != '.DS_Store':
                img_path = os.path.join(label_path, img_name)
                image = Image.open(img_path).convert('RGB')
                image = image.resize((50, 50))
                image = np.array(image)
                image = np.transpose(image, (2, 0, 1)) / 255
                images.append(image)
                labels.append(label)
    
    return np.array(images), np.array(labels), label_names

# Prepare the support set
def prepare_support_set(support_dir):
    X_support, y_support, label_names = process_images_in_directory(support_dir)
    k_shot = len(y_support) // len(label_names)
    n_way = len(label_names)
    support = torch.from_numpy(X_support).float()
    return support, k_shot, n_way, label_names

# Database connection parameters
db_params = {
    'dbname': 'plant_disease',
    'user': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

# Function to query the disease type from the database
def get_disease_type(plant_name):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        query = "SELECT disease_type FROM agriculture_plant WHERE plant_name = %s"
        cursor.execute(query, (plant_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        st.error(f"Database Error: {e}")
    finally:
        if connection:
            connection.close()

# Function to make API call with a keyword
def get_pest_disease_list_by_keyword(api_key, keyword):
    url = f"https://perenual.com/api/pest-disease-list?key={api_key}&q={keyword}"
    response = requests.get(url)
    return response.json()

# Function to display solution
def display_solutions(data):
    if 'data' in data and len(data['data']) > 0:
        solutions = data['data'][0].get('solution', [])
        for solution in solutions:
            st.subheader(solution.get('subtitle', ''))
            st.write(solution.get('description', ''))
    else:
        st.write("No solutions found for this keyword.")

def classify_plant():
    
    col1, col2 = st.columns([15,2])
    with col1:
        st.header('Classify Plant Image')
       
        
    st.header('', divider='rainbow')
    
    
    model = load_model('./model/protonet.pt')
    support, k_shot, n_way, label_names = prepare_support_set('./support_plants')
    
    st.header("Upload Plant Images")

    uploaded_files = st.file_uploader("Upload Plant Images", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'], label_visibility='hidden')

    if st.button('Classify Images'):
        if uploaded_files:
            query_images = []
            for uploaded_file in uploaded_files:
                image = Image.open(uploaded_file).convert('RGB')
                image = image.resize((50, 50))
                image = np.array(image)
                image = np.transpose(image, (2, 0, 1)) / 255
                query_images.append(image)

            queries = torch.from_numpy(np.array(query_images)).float()
            preds, confidences = model(support, queries, k_shot, n_way)

            api_key = 'sk-Aq2J65bb4b07e2d943983'  # API key

            for i, uploaded_file in enumerate(uploaded_files):
                predicted_label = label_names[preds[i]]
                confidence = confidences[i].item() * 100  # Convert to percentage
                caption = f'Predicted: {predicted_label} - Confidence: {confidence:.2f}%'
                st.image(uploaded_file, caption=caption, use_column_width=True)
                
                # Query the database for the disease type
                disease_type = get_disease_type(predicted_label)
                
                #save past prediction
                connection = psycopg2.connect(**db_params)
                cursor = connection.cursor()

                cursor.execute(
                    "INSERT INTO saved_prediction (image_file, prediction,confidence, disease_type, predicted_time) "
                    "VALUES (%s, %s, %s, %s, NOW())",
                    (uploaded_file.read(), predicted_label, confidence, disease_type)
                )
                connection.commit()

                
                if disease_type:
                    st.write(f"Disease Type: {disease_type}")
                    # Get solutions from the API
                    st.header(f"Solution for Disease Type:")
                    data = get_pest_disease_list_by_keyword(api_key, disease_type)
                    display_solutions(data)
                    
                else:
                    st.write("No disease type found for this plant class in the database.")
                    
                    
        else:
            st.error("Please upload at least one image for classification.")