import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Set page config with a custom title and icon
st.set_page_config(page_title="Data Quality Analytics Dashboard", page_icon="🌎", layout="wide")

# Display the main dashboard title using markdown for custom font size
st.markdown("## 📈 CRM CONTACT Data Quality Analytics Dashboard", unsafe_allow_html=True)

# Custom CSS for styling
custom_css = """
<style>
    /* General font styling to ensure uniformity with increased size */
    html, body, [class*="st-"] {
        font-family: "Arial", sans-serif;
        font-size: 30px; /* Increase base font size */
    }

   /* This specific targeting might need adjustment based on actual DOM structure */
    label[for*="Select a Property"] {
        font-size: 30px !important;
        font-weight: bold !important;
    }
    
    /* Style adjustments for the select box options */
    .stSelectbox > div > div > select {
        font-size: 20px !important;
    }

    /* Style adjustments for file uploader for consistency */
    .stFileUploader {
        margin-bottom: 20px;
    }
    /* Style adjustments for the content text */
    
    .stText {
        font-size: 30px; /* Increase font size for better visibility */
        color: black; /* Ensure text color is black */
    }

    /* Enhancements for comments and data type information with bigger fonts */
    .info-box {
        border: 2px solid #ced4da;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: #f8f9fa;
    }

    .info-title {
        font-weight: bold;
        margin-bottom: 5px;
        font-size: 22px; /* Larger font size for titles */
    }

    /* Style adjustments for text area */
    .stTextArea > div > div > textarea {
        font-size: 18px; /* Increase font size in text area */
        color: black !important; /* Ensure text color is black */
        border-color: #ced4da; /* Visible border color */
    }
    /* Style adjustments for the bordered text box */
     /* Style adjustments for the bordered text box */
    .bordered-text-box {
        border: 2px solid #ced4da;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
        font-size: 18px; /* Increased font size for content */
        color: black; /* Ensure text color is black */
        white-space: pre-wrap; /* Ensure that line breaks and white spaces are preserved */
    }
    .stMarkdown > p {
        font-size: 30px; /* Increase font size for the title */
        color: black; /* Make title text color black */
    }
    /* Adding general font styling */
    html, body, [class*="st-"] {
        font-family: "Arial", sans-serif;
        font-size: 30px; /* Adjust base font size for uniformity */
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# File uploader for CSV input
uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

if uploaded_file is not None:
    # Load and display data
    df = pd.read_csv(uploaded_file)
    # selected_attribute = st.selectbox('Select a Property:', df['Attribute'].unique(), index=0, format_func=lambda x: f"🔹 {x}")
    # selected_attribute = st.selectbox('Select a Property:', df['Attribute'].unique())
    selected_attribute = st.selectbox('Select a Property:',options=df['Attribute'].unique())
    # Display the selected value
    st.write('You selected:', selected_attribute)
       # selected_attribute = st.selectbox('Select a Property:', df['Attribute'].unique())
    # selected_attribute = st.selectbox(st.text('Select a Property:)',  df['Attribute'].unique()))

    if selected_attribute:
        # Creating gauge charts within columns
        gauge_columns = st.columns(3)
        attribute_data = df[df['Attribute'] == selected_attribute].iloc[0]

        valid_counts = attribute_data['Valid Length Counts']
        invalid_counts = attribute_data['Invalid Length Counts']
        null_counts = attribute_data['NULL Count']

        max_values = {
            'Valid Length Counts': max(df['Valid Length Counts']) * 1.1,
            'Invalid Length Counts': max(df['Invalid Length Counts'], default=10) * 1.1,
            'NULL Count': max(df['NULL Count']) * 1.1
        }

        gauges = ['Valid Length Counts', 'Invalid Length Counts', 'NULL Count']
        count_values = [valid_counts, invalid_counts, null_counts]
        colors = ["green", "red", "orange"]

        for i, gauge_column in enumerate(gauge_columns):
            with gauge_column:
                gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=count_values[i],
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': gauges[i], 'font': {'size': 22}},
                    gauge={
                        'axis': {'range': [None, max_values[gauges[i]]], 'tickwidth': 1, 'tickcolor': "darkblue", 'tickfont': {'size': 18}},
                        'bar': {'color': colors[i]},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [0, max_values[gauges[i]] / 2], 'color': 'lightgray'},
                            {'range': [max_values[gauges[i]] / 2, max_values[gauges[i]]], 'color': 'gray'}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': count_values[i]
                        }
                    }
                ))
                gauge.update_layout(paper_bgcolor="white", font={'size': 18, 'color': "darkblue"})
                st.plotly_chart(gauge, use_container_width=True)

        # Display additional attribute details with larger fonts
        details = [
            ('Comment', attribute_data['Comment']),
            ('MIS Property DataType', attribute_data['Mis_Type']),
            ('Hact Property DataType', attribute_data['Hact_Type'])
        ]

        for title, detail in details:
            st.markdown(f'<div class="info-box"><div class="info-title">{title}:</div><div style="font-size: 18px;">{detail}</div></div>', unsafe_allow_html=True)
        
        # Title for the text area
        st.markdown("#### Attributes not present in CRM.Contact but in Hact Data-Standards", unsafe_allow_html=True)
        # Attributes not present in CRM.Contact but in Hact Data-Standards
        unique_attributes = df['Attributes not present in CRM.Contact'].dropna().unique()
        constant_attributes = "<div class=\"bordered-text-box\">" + "<br>".join(unique_attributes) + "</div>"
        st.markdown(constant_attributes, unsafe_allow_html=True)

        # Title for the text area
        st.markdown("#### Data Extraction Source", unsafe_allow_html=True)
        # Attributes not present in CRM.Contact but in Hact Data-Standards
        unique_attributesA = df['Extraction_source'].dropna().unique()
        constant_attributesA = "<div class=\"bordered-text-box\">" + "<br>".join(unique_attributesA) + "</div>"
        st.markdown(constant_attributesA, unsafe_allow_html=True)
