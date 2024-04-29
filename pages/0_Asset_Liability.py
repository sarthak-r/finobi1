import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Function to calculate asset and liability balances at each year
def calculate_asset_liability_balances(current_age, initial_assets, annual_contributions, annual_expenses, asset_roi, liability_roi, inflation_rate, life_expectancy):
    years = np.arange(current_age, life_expectancy + 1)
    asset_balance = np.zeros(len(years))
    liability_balance = np.zeros(len(years))
    asset_balance[0] = initial_assets
    for i in range(1, len(years)):
        asset_balance[i] = (asset_balance[i - 1] * (1 + asset_roi / 100) + annual_contributions) / (1 + inflation_rate / 100)
        liability_balance[i] = liability_balance[i - 1] * (1 + liability_roi / 100) / (1 + inflation_rate / 100) + annual_expenses
    return years, asset_balance, liability_balance

# Streamlit app
st.title("Asset Liability Cashflow Model")

current_age = st.slider("Current age", 20, 80, 30)
initial_assets = st.slider("Initial assets", 0, 1000000, 250000)
annual_contributions = st.slider("Annual contributions to assets", 0, 50000, 10000)
annual_expenses = st.slider("Annual expenses/liabilities", 0, 50000, 10000)
asset_roi = st.slider("Asset return percentage", 0, 25, 4)
liability_roi = st.slider("Liability return percentage", 0, 25, 2)
inflation_rate = st.slider("Inflation rate", 0, 10, 2)
life_expectancy = st.slider("Life expectancy", 80, 100, 85)

years, asset_balance, liability_balance = calculate_asset_liability_balances(current_age, initial_assets, annual_contributions, annual_expenses, asset_roi, liability_roi, inflation_rate, life_expectancy)
df = pd.DataFrame({"Year": years, "Asset Balance": asset_balance, "Liability Balance": liability_balance})

st.write("### Asset Liability Cashflow Model")

# Stacked bar chart for asset and liability balances with tooltips
tooltip=['Asset Balance', 'Liability Balance']
chart = alt.Chart(df).mark_bar().encode(
    x='Year:O',
    y=alt.Y('value:Q', stack=None),
    color='variable:N',
    tooltip=tooltip
).transform_fold(
    ['Asset Balance', 'Liability Balance'],
    as_=['variable', 'value']
).properties(
    width=700,
    height=400
)

st.altair_chart(chart, use_container_width=True)
