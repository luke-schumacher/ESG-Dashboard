import streamlit as st  # web development
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import time  # to simulate real-time data, time loop
import plotly.express as px  # interactive charts

# Read CSV from local directory
df = pd.read_csv("data/filtered_ESGdataset_complete.csv")

# Set page configuration
st.set_page_config(
    page_title='Real-Time ESG Dashboard',
    page_icon='✅',
    layout='wide'
)

# Dashboard title
st.title("ESG Dashboard")

# Top-level filters
country_filter = st.selectbox("Select the Country", pd.unique(df['Country Name']))

# Creating a single-element container
placeholder = st.empty()

# DataFrame filter based on selected country
df = df[df['Country Name'] == country_filter]

# Near real-time / live feed simulation
for seconds in range(200):
    # Simulate new data for visualization
    df['Adjusted Savings'] = df['1960'] + np.random.choice(range(0, 100), size=len(df))
    df['Natural Resources Depletion'] = df['1960'] * np.random.choice(range(1, 5), size=len(df))

    # Creating KPIs
    avg_savings = np.mean(df['Adjusted Savings'])
    total_depletion = np.sum(df['Natural Resources Depletion'])

    with placeholder.container():
        # Create three columns for KPIs
        kpi1, kpi2, kpi3 = st.columns(3)

        # Fill in those three columns with respective metrics or KPIs 
        kpi1.metric(label="Avg Adjusted Savings (%)", value=round(avg_savings, 2), delta=round(avg_savings - 10, 2))
        kpi2.metric(label="Total Natural Resources Depletion", value=int(total_depletion), delta=-10 + int(total_depletion))
        kpi3.metric(label="Latest Year Data (2022)", value=f"{df['2022'].values[0]:,.2f}", delta=-round(df['2022'].values[0] / 100) * 100)

        # Create two columns for charts
        fig_col1, fig_col2 = st.columns(2)

        with fig_col1:
            st.markdown("### Adjusted Savings Over Years")
            fig = px.line(data_frame=df, x='Indicator Code', y='Adjusted Savings', title='Adjusted Savings Over Years')
            st.write(fig)

        with fig_col2:
            st.markdown("### Natural Resources Depletion")
            fig2 = px.bar(data_frame=df, x='Country Name', y='Natural Resources Depletion', title='Natural Resources Depletion')
            st.write(fig2)

        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)

    # Clear previous results after displaying
    # placeholder.empty()
