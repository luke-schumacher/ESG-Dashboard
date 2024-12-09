import streamlit as st  # web development
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import time  # to simulate real-time data, time loop
import plotly.express as px  # interactive charts
import json  # for JSON formatting

# Read CSV from local directory
df = pd.read_csv("data/filtered_ESGdataset_complete1.csv")

# Remove any irrelevant columns (like 'Unnamed: 67') and keep only year columns and other necessary columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
year_columns = df.columns[4:]  # assuming years start from the 5th column onwards

# Set page configuration with a sustainability-related icon
st.set_page_config(
    page_title='Real-Time ESG Dashboard',
    page_icon='🌍',  # Sustainability-related icon
    layout='wide'
)

st.markdown("""
    <style>
    /* Title styling with improved color */
    .stTitle {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-top: -20px;
        margin-bottom: 20px;
        color: #e0e6f0;  /* Light color for better contrast */
    }
    /* Dropdown menu size and hover effect */
    div[data-baseweb="select"] {
        max-width: 60%;
        margin-bottom: 10px; /* Adjust spacing below dropdown */
        transition: all 0.3s ease-in-out;
    }
    div[data-baseweb="select"]:hover {
        transform: scale(1.03);
    }
    </style>
""", unsafe_allow_html=True)

# Dashboard title
st.markdown('<div class="stTitle">ESG Dashboard</div>', unsafe_allow_html=True)

# Top-level filters
st.markdown("### Select Economic, Social or Governance")
country_filter = st.selectbox("", pd.unique(df['Country Name']))
st.markdown("### Select Metric")
indicator_filter = st.selectbox("", pd.unique(df['Indicator Name']))

# The rest of the code remains unchanged


# Single-element container
placeholder = st.empty()

# Filter DataFrame based on selected country and indicator
df = df[(df['Country Name'] == country_filter) & (df['Indicator Name'] == indicator_filter)]

# Reshape data for year-based analysis and remove any non-numeric year columns
df_melted = df.melt(id_vars=['Country Name', 'Indicator Name', 'Indicator Code'], 
                    value_vars=year_columns, var_name='Year', value_name='Value')
df_melted['Year'] = pd.to_numeric(df_melted['Year'], errors='coerce')
df_melted.dropna(subset=['Year', 'Value'], inplace=True)  # remove rows where Year or Value is NaN

# Near real-time / live feed simulation
for seconds in range(200):
    # Simulate new data for visualization
    df_melted['Adjusted Savings'] = df_melted['Value'] + np.random.choice(range(0, 100), size=len(df_melted))
    df_melted['Natural Resources Depletion'] = df_melted['Value'] * np.random.choice(range(1, 5), size=len(df_melted))

    # Calculate KPIs
    avg_value = np.mean(df_melted['Value'])
    total_depletion = np.sum(df_melted['Natural Resources Depletion'])
    latest_value = df_melted[df_melted['Year'] == 2022]['Value'].values[0] if 2022 in df_melted['Year'].values else np.nan
    
    with placeholder.container():
        # KPI columns
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(label=f"Avg {indicator_filter} (%)", value=round(avg_value, 2))
        kpi2.metric(label="Total Natural Resources Depletion", value=int(total_depletion))
        kpi3.metric(label="Latest Year Data (2022)", value=f"{latest_value:,.2f}" if not np.isnan(latest_value) else "N/A")

        # Visualization columns
        fig_col1, fig_col2 = st.columns(2)

        with fig_col1:
            st.markdown(f"### {indicator_filter} Over Years")
            # Line plot for indicator over years
            fig = px.line(data_frame=df_melted, x='Year', y='Value', title=f"{indicator_filter} Over Years")
            st.plotly_chart(fig, use_container_width=True, key=f"line_chart_{seconds}")

        with fig_col2:
            st.markdown("### Natural Resources Depletion")
            # Bar plot for natural resources depletion by year
            fig2 = px.bar(data_frame=df_melted, x='Year', y='Natural Resources Depletion', title='Natural Resources Depletion Over Years')
            st.plotly_chart(fig2, use_container_width=True, key=f"bar_chart_{seconds}")

        # Additional visualizations
        st.markdown("### Additional Analysis")

        # Moving Average Line Chart
        fig3 = px.line(df_melted, x='Year', y=df_melted['Value'].rolling(window=5).mean(), 
                       title=f"{indicator_filter} 5-Year Moving Average")
        st.plotly_chart(fig3, use_container_width=True, key=f"moving_avg_{seconds}")

        # Area Chart for cumulative indicator value
        df_melted['Cumulative Value'] = df_melted['Value'].cumsum()
        fig4 = px.area(df_melted, x='Year', y='Cumulative Value', title=f"Cumulative {indicator_filter} Over Years")
        st.plotly_chart(fig4, use_container_width=True, key=f"cumulative_area_{seconds}")

        # Detailed data table view
        st.markdown("### Detailed Data View")
        st.dataframe(df_melted)
        time.sleep(1)

        # Convert the DataFrame to JSON format
        json_data = df_melted.to_json(orient='records')

        # Add a unique key based on the selected country and indicator
        unique_key = f"json_download_button_{country_filter}_{indicator_filter}_{seconds}"  # Make unique key by appending seconds

        # Add a download button with a unique key
        st.download_button(
            label="Download Data as JSON",
            data=json_data,
            file_name=f"{country_filter}_{indicator_filter}_data.json",
            mime="application/json",
            key=unique_key  # Ensure unique key by including seconds
        )
        # placeholder.empty()
