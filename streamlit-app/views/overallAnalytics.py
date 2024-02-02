import streamlit as st
import psycopg2
import matplotlib.pyplot as plt

# Function to fetch disease counts from the database
db_params = {
    'dbname': 'plant_disease',
    'user': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

# Function to fetch disease counts from the database
def fetch_disease_counts():
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        cursor.execute("SELECT disease_type FROM saved_prediction")
        data = cursor.fetchall()

        disease_counts = {}
        for (disease_type,) in data:
            if disease_type in disease_counts:
                disease_counts[disease_type] += 1
            else:
                disease_counts[disease_type] = 1

        return disease_counts

    except Exception as e:
        st.error(f"Error: {e}")
        return {}

    finally:
        if connection:
            connection.close()

# Function to plot disease counts as a horizontal bar chart
def plot_disease_counts(disease_counts):
    fig, ax = plt.subplots()
    disease_types = list(disease_counts.keys())
    counts = list(disease_counts.values())

    ax.barh(disease_types, counts)
    ax.set_ylabel('Disease Types')
    ax.set_xlabel('Counts')
    ax.set_title('Disease Type Counts')
    return fig

# Function to display overall analytics of disease types using Streamlit
def overall_analytics():
    st.title('Overall Analytics of Disease Types')

    disease_counts = fetch_disease_counts()
    if disease_counts:
        fig = plot_disease_counts(disease_counts)
        st.pyplot(fig)
    else:
        st.write('No data available.')

if __name__ == "__main__":
    overall_analytics()