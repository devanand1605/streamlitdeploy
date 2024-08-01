import streamlit as st
import json

# Function to load data from JSON file
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Load data
data = load_data('data.json')

# Streamlit application
st.title('ID Lookup Application')

# Input textbox for ID
id_input = st.text_input('Enter ID:')

if st.button('Submit'):
    # Search for the ID in the JSON data
    user_data = next((item for item in data if item["id"] == id_input), None)

    if user_data:
        st.write(f"Name: {user_data['name']}")
        st.write(f"Email: {user_data['email']}")
    else:
        st.write("ID not found. Please enter a valid ID.")
