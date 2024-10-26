import streamlit as st
import numpy as np 
import pandas as pd  
import time 
import plotly.express as px  
import plotly.graph_objects as go  

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
        # Add a loading spinner to enhance user feedback during data update
        with st.spinner("Updating data..."):
            time.sleep(1)

        # Create three columns for KPIs
        kpi1, kpi2, kpi3 = st.columns(3)

        # Fill in those three columns with respective metrics or KPIs
        kpi1.metric(label="Avg Adjusted Savings (%)", value=round(avg_savings, 2), delta=round(avg_savings - 10, 2))
        kpi2.metric(label="Total Natural Resources Depletion", value=int(total_depletion), delta=-10 + int(total_depletion))
        
        # Add conditional coloring for KPI 3 to indicate increase or decrease
        latest_value = df['2022'].values[0]
        delta_value = round(latest_value / 100) * 100
        delta_direction = "+" if latest_value > 1000 else "-"
        delta_color = "green" if latest_value > 1000 else "red"
        
        kpi3.metric(
            label="Latest Year Data (2022)",
            value=f"{latest_value:,.2f}",
            delta=f"{delta_direction}{delta_value}",
            delta_color=delta_color
        )

        # Create two columns for charts
        fig_col1, fig_col2 = st.columns(2)

        with fig_col1:
            st.markdown("### Adjusted Savings Over Years")
            # Enhanced Line Chart with smoother visuals
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['Indicator Code'],
                y=df['Adjusted Savings'],
                mode='lines+markers',
                line=dict(color='royalblue', width=2),
                marker=dict(size=5, color='royalblue')
            ))
            fig.update_layout(
                title="Adjusted Savings Over Years",
                xaxis_title="Year",
                yaxis_title="Adjusted Savings",
                template="plotly_dark"
            )
            st.write(fig)

        with fig_col2:
            st.markdown("### Natural Resources Depletion")
            # Enhanced Bar Chart
            fig2 = px.bar(
                data_frame=df, x='Country Name', y='Natural Resources Depletion',
                title="Natural Resources Depletion",
                color='Natural Resources Depletion',
                color_continuous_scale='sunset'
            )
            fig2.update_layout(
                xaxis_title="Country",
                yaxis_title="Depletion",
                template="plotly_dark"
            )
            st.write(fig2)

        st.markdown("### Detailed Data View")
        st.dataframe(df.style.format("{:.2f}").background_gradient(cmap='viridis', axis=0))
        
        time.sleep(1)
