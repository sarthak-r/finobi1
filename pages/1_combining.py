import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Function to calculate retirement balance at each year
def calculate_retirement_balance(current_age, super_bal, annual_contribution, retirement_age, roi, inflation_rate, income_replacement_ratio, life_expectancy):
    years = np.arange(current_age, life_expectancy + 1)
    balance = np.zeros(len(years))
    balance[0] = super_bal
    annual_expenses = super_bal * (income_replacement_ratio / 100)
    for i in range(1, len(years)):
        balance[i] = (balance[i - 1] * (1 + roi / 100) + annual_contribution) / (1 + inflation_rate / 100)
        if i >= retirement_age - current_age:
            balance[i] -= annual_expenses
    return years, balance

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
st.title("Financial Planning Tool")

# Retirement planning inputs
st.sidebar.subheader("Retirement Planning Inputs")
current_age = st.sidebar.slider("Current age", 20, 80, 30)
super_bal = st.sidebar.slider("Current super balance", 1, 1000000, 250000)
annual_contribution = st.sidebar.slider("Annual contribution to super", 0, 50000, 10000)
retirement_age = st.sidebar.slider("Retirement age", current_age + 1, 80, 60)
roi = st.sidebar.slider("Return percentage", 0, 25, 4)
inflation_rate_retirement = st.sidebar.slider("Inflation rate", 0, 10, 2)
income_replacement_ratio = st.sidebar.slider("Income replacement ratio (%)", 50, 150, 70)
life_expectancy = st.sidebar.slider("Life expectancy", 80, 100, 85)

# Asset liability management inputs
st.sidebar.subheader("Asset Liability Management Inputs")
initial_assets = st.sidebar.slider("Initial assets", 0, 1000000, 250000)
annual_contributions = st.sidebar.slider("Annual contributions to assets", 0, 50000, 10000)
annual_expenses = st.sidebar.slider("Annual expenses/liabilities", 0, 50000, 10000)
asset_roi = st.sidebar.slider("Asset return percentage", 0, 25, 4)
liability_roi = st.sidebar.slider("Liability return percentage", 0, 25, 2)
inflation_rate_asset_liability = st.sidebar.slider("Inflation rate", 0, 10, 2)

# Calculate retirement balance
years_retirement, retirement_balance = calculate_retirement_balance(current_age, super_bal, annual_contribution, retirement_age, roi, inflation_rate_retirement, income_replacement_ratio, life_expectancy)

# Calculate asset and liability balances
years_asset_liability, asset_balance, liability_balance = calculate_asset_liability_balances(current_age, initial_assets, annual_contributions, annual_expenses, asset_roi, liability_roi, inflation_rate_asset_liability, life_expectancy)

# Combine dataframes
df_retirement = pd.DataFrame({"Year": years_retirement, "Retirement Balance": retirement_balance})
df_asset_liability = pd.DataFrame({"Year": years_asset_liability, "Asset Balance": asset_balance, "Liability Balance": liability_balance})

# Plot retirement balance
st.subheader("Retirement Balance")
chart_retirement = alt.Chart(df_retirement).mark_line(color='blue').encode(
    x='Year:O',
    y='Retirement Balance:Q',
    tooltip=['Year', alt.Tooltip('Retirement Balance', format='.2f')]
).properties(
    width=700,
    height=400
)
st.altair_chart(chart_retirement)

# Plot asset and liability balances
st.subheader("Asset and Liability Balances")
chart_asset_liability = alt.Chart(df_asset_liability).mark_bar().encode(
    x='Year:O',
    y=alt.Y('value:Q', stack=None),
    color='variable:N',
    tooltip=['Year', 'value']
).transform_fold(
    ['Asset Balance', 'Liability Balance'],
    as_=['variable', 'value']
).properties(
    width=700,
    height=400
)
st.altair_chart(chart_asset_liability)
