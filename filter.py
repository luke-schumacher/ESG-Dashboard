import pandas as pd
import random

# Load the dataset
data = pd.read_csv('ESG-Dashboard/data/filtered_ESGdataset_complete.csv')

# Define possible categories
categories = ['Economic', 'Social', 'Governance']

# Function to randomly assign a category to each country
def assign_random_category(country_code):
    # You can use the first letter of the country code or just randomly assign
    random.seed(abs(hash(country_code)) % (2**32))  # Seed for reproducibility
    return f"{random.choice(categories)} {country_code[:3].upper()}"  # First 3 letters of country code for consistency

# Apply the random category assignment based on the country code
data['Category'] = data['Country Code'].apply(assign_random_category)

# Drop the old 'Country Name' and 'Country Code' columns
data = data.drop(['Country Name', 'Country Code'], axis=1)

# Define the mapping for shortening indicator names
indicator_shortening = {
    "Adjusted savings: natural resources depletion (% of GNI)": "Nat. Res. Depletion (% of GNI)",
    "Children in employment, total (% of children ages 7-14)": "Children Employment (%)",
    "CO2 emissions (metric tons per capita)": "CO2 Emissions (t/cap)",
    "Energy imports, net (% of energy use)": "Energy Imports (% of energy use)",
    "Energy intensity level of primary energy (MJ/$2017 PPP GDP)": "Energy Intensity (MJ/$ GDP)",
    "Energy use (kg of oil equivalent per capita)": "Energy Use (kg oil/cap)",
    "Fossil fuel energy consumption (% of total)": "Fossil Fuel Consumption (%)",
    "GDP growth (annual %)": "GDP Growth (%)",
    "GHG net emissions/removals by LUCF (Mt of CO2 equivalent)": "GHG Net Emissions (Mt CO2)",
    "Labor force participation rate, total (% of total population ages 15-64)": "Labor Force Participation (%)",
    "Literacy rate, adult total (% of people ages 15 and above)": "Literacy Rate (%)",
    "Methane emissions (metric tons of CO2 equivalent per capita)": "Methane Emissions (t CO2/cap)",
    "Nitrous oxide emissions (metric tons of CO2 equivalent per capita)": "Nitrous Oxide Emissions (t CO2/cap)",
    "Population ages 65 and above (% of total population)": "Population 65+ (%)",
    "Ratio of female to male labor force participation rate (%)": "Female to Male Labor Force (%)",
    "Renewable electricity output (% of total electricity output)": "Renewable Electricity (%)",
    "Renewable energy consumption (% of total final energy consumption)": "Renewable Energy Consumption (%)",
    "Unmet need for contraception (% of married women ages 15-49)": "Unmet Contraception Need (%)"
}

# Rename the indicators using the shortening mapping
data = data.rename(columns=indicator_shortening)

# Save the modified DataFrame to a new CSV file
data.to_csv('modified_data_random_categories.csv', index=False)

print("Data has been processed and saved to 'modified_data_random_categories.csv'.")
