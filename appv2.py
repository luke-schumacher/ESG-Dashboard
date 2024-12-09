import streamlit as st
import pandas as pd
import plotly.express as px

# Read CSV from local directory
df = pd.read_csv("data/filtered_ESGdataset_complete1.csv")

# Remove irrelevant columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
year_columns = df.columns[4:]  # Assuming years start from the 5th column

# Set Streamlit page configuration
st.set_page_config(
    page_title="Real-Time ESG Dashboard",
    page_icon="🌍",
    layout="wide"
)

# Add custom styling
st.markdown("""
    <style>
    .stTitle { text-align: center; font-size: 2.5rem; font-weight: bold; color: #e0e6f0; }
    </style>
""", unsafe_allow_html=True)

# Dashboard title
st.markdown('<div class="stTitle">ESG Dashboard</div>', unsafe_allow_html=True)


# Function to render each category section
def render_category_section(category_name, col, color_sequence):
    with col:
        st.markdown(f"## {category_name}")

        # Country and indicator filters
        country_filter = st.selectbox(f"Select Country for {category_name}", pd.unique(df['Country Name']), key=f"{category_name}_country")
        indicator_filter = st.selectbox(f"Select Metric for {category_name}", pd.unique(df['Indicator Name']), key=f"{category_name}_indicator")

        # Filter data based on user selection
        filtered_df = df[(df['Country Name'] == country_filter) & (df['Indicator Name'] == indicator_filter)]

        # Reshape data for visualization
        filtered_df_melted = filtered_df.melt(
            id_vars=['Country Name', 'Indicator Name', 'Indicator Code'],
            value_vars=year_columns, var_name='Year', value_name='Value'
        )
        filtered_df_melted['Year'] = pd.to_numeric(filtered_df_melted['Year'], errors='coerce')
        filtered_df_melted.dropna(subset=['Year', 'Value'], inplace=True)

        # Line plot for the selected indicator
        fig = px.line(
            data_frame=filtered_df_melted, x='Year', y='Value',
            title=f"{indicator_filter} Over Years ({category_name})",
            color_discrete_sequence=color_sequence
        )
        st.plotly_chart(fig, use_container_width=True, key=f"{category_name}_line_chart")

        # Bar plot for the same data
        fig2 = px.bar(
            data_frame=filtered_df_melted, x='Year', y='Value',
            title=f"{indicator_filter} Bar Chart ({category_name})",
            color_discrete_sequence=color_sequence
        )
        st.plotly_chart(fig2, use_container_width=True, key=f"{category_name}_bar_chart")

        return filtered_df_melted  # Return data for table and JSON export


# Layout with three columns for the categories
col1, col2, col3 = st.columns(3)

# Render each category with distinct colors and collect filtered data
economic_data = render_category_section("Economic", col1, color_sequence=px.colors.qualitative.Plotly)  # Default Plotly colors
social_data = render_category_section("Social", col2, color_sequence=px.colors.qualitative.Bold)         # Bold colors for Social
governance_data = render_category_section("Governance", col3, color_sequence=['#FF5733', '#33FF57', '#3357FF']) # Safe colors for Governance

# Combine filtered data for display and export
combined_data = pd.concat([economic_data, social_data, governance_data])

# Table visualization at the bottom
st.markdown("## Combined Data")
st.dataframe(combined_data)

# Button to download data as JSON
st.download_button(
    label="Download Data as JSON",
    data=combined_data.to_json(orient="records", lines=True),
    file_name="esg_data.json",
    mime="application/json"
)
