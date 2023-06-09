import csv
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import plotly.express as px

# Function to convert uploaded CSV file to DataFrame
def read_csv(csv_file):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)
        return df
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Function to download CSV file
def download_csv(csv_data):
    # Create a unique filename for the temporary CSV file
    temp_file = "temp_file.csv"

    # Download link for the CSV file
    href = f'<a href="data:file/csv;base64,{base64.b64encode(csv_data.encode()).decode()}" download="{temp_file}">Download CSV file</a>'
    st.markdown(href, unsafe_allow_html=True)

# Function to perform data analysis
def perform_data_analysis(table_data):
    # Display the table
    st.table(table_data)

    # Convert the table data to a DataFrame
    data = pd.DataFrame(table_data)

    # Show the distribution of predicted functional effects
    functional_effects = data["Predicted functional effect"].value_counts()
    st.subheader("Functional Effect Distribution")
    fig = px.pie(names=functional_effects.index, values=functional_effects.values)
    st.plotly_chart(fig)

    # Count the number of occurrences for each mutation type
    mutation_counts = data["Type of mutation - DNA"].value_counts()
    st.subheader("Mutation Type Counts")
    st.bar_chart(mutation_counts)

    # Display the top 10 most frequent amino acid changes
    top_amino_acid_changes = data["Amino acid change"].value_counts().head(10)
    st.subheader("Top 10 Amino Acid Changes")
    st.table(top_amino_acid_changes)

    # Filter data based on a specific mutation type
    selected_mutation_type = st.selectbox("Select a Mutation Type", data["Type of mutation - DNA"].unique())
    filtered_data = data[data["Type of mutation - DNA"] == selected_mutation_type]
    st.subheader(f"Filtered Data - Mutation Type: {selected_mutation_type}")
    st.table(filtered_data)

    # Show summary statistics of nucleotide change positions
    nucleotide_positions = data["contig position (GRCh38.p7)"]
    nucleotide_positions = pd.to_numeric(nucleotide_positions, errors='coerce')
    nucleotide_positions = nucleotide_positions.dropna().astype(int)

    st.subheader('Nucleotide Positions')
    st.line_chart(nucleotide_positions)

    # Plot histogram of nucleotide change positions
    st.subheader("Histogram - Nucleotide Change Positions")
    fig, ax = plt.subplots() 
    plt.hist(nucleotide_positions, bins=20)   
    st.pyplot(fig)

    # Additional data analysis and plots for other columns
    # ...

    # Display additional information
    st.sidebar.header("Additional Information")
    st.sidebar.write("This Streamlit app performs data analysis on the provided table. You can explore different aspects of the data using the interactive widgets.")

def main():
    st.title("Data Analysis of CLN08 Mutations")
    st.sidebar.title("Data Analysis")
    st.sidebar.write("Below is the Data of CLN8 mutation diagnosis of 43 patients taken from https://www.ucl.ac.uk/ncl-disease/ncl-resource-gateway-batten-disease")
    st.sidebar.write("Below is Link to example files used (excel and csv files) - https://drive.google.com/drive/folders/1sN7aabvBnrooZcg38aeNp-NpfJwRmmQC?usp=sharing")

    st.set_option('deprecation.showPyplotGlobalUse', False)

    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file:
        # Read CSV data into DataFrame
        table_data = read_csv(uploaded_file)
        if table_data is not None:
            perform_data_analysis(table_data)

    st.sidebar.write("This Streamlit app allows you to upload a CSV file containing data about CLN08 mutations. Once uploaded, it performs data analysis and provides interactive visualizations.")

if __name__ == "__main__":
    main()
