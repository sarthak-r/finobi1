import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Function to calculate cashflows for each year
def calculate_cashflows(current_age, retirement_age, initial_super_bal, initial_asset_bal, 
                        annual_super_contribution, annual_asset_contribution, annual_expenses, 
                        super_roi, asset_roi, liability_roi, inflation_rate, life_expectancy):
    years = np.arange(current_age, life_expectancy + 1)
    super_balance = np.zeros(len(years))
    asset_balance = np.zeros(len(years))
    liability_balance = np.zeros(len(years))
    
    # Set initial balances
    super_balance[0] = initial_super_bal
    asset_balance[0] = initial_asset_bal
    
    for i in range(1, len(years)):
        # Calculate super contributions and returns
        super_contribution = annual_super_contribution
        super_balance[i] = super_balance[i-1] * (1 + super_roi / 100) + super_contribution
        
        # Calculate asset contributions and returns
        asset_contribution = annual_asset_contribution
        asset_balance[i] = asset_balance[i-1] * (1 + asset_roi / 100) + asset_contribution
        
        # Calculate liabilities
        liability_balance[i] = liability_balance[i-1] * (1 + liability_roi / 100) / (1 + inflation_rate / 100) + annual_expenses
        
    return years, super_balance, asset_balance, liability_balance

# Streamlit app
st.title("Comprehensive Cashflow Modeling")

# Financial inputs
current_age = st.slider("Current age", 20, 80, 30)
retirement_age = st.slider("Retirement age", current_age + 1, 80, 60)
initial_super_bal = st.slider("Initial superannuation balance", 1, 1000000, 250000)
initial_asset_bal = st.slider("Initial asset balance", 0, 1000000, 100000)
annual_super_contribution = st.slider("Annual contribution to superannuation", 0, 50000, 10000)
annual_asset_contribution = st.slider("Annual contribution to assets", 0, 50000, 10000)
annual_expenses = st.slider("Annual expenses/liabilities", 0, 50000, 10000)
super_roi = st.slider("Superannuation return percentage", 0, 25, 4)
asset_roi = st.slider("Asset return percentage", 0, 25, 6)
liability_roi = st.slider("Liability return percentage", 0, 25, 2)
inflation_rate = st.slider("Inflation rate", 0, 10, 2)
life_expectancy = st.slider("Life expectancy", 80, 100, 85)

# Calculate cashflows
years, super_balance, asset_balance, liability_balance = calculate_cashflows(current_age, retirement_age, 
                                                                             initial_super_bal, initial_asset_bal, 
                                                                             annual_super_contribution, 
                                                                             annual_asset_contribution, 
                                                                             annual_expenses, super_roi, 
                                                                             asset_roi, liability_roi, 
                                                                             inflation_rate, life_expectancy)

# Create dataframe for visualization
df = pd.DataFrame({
    "Year": years,
    "Superannuation Balance": super_balance,
    "Asset Balance": asset_balance,
    "Liability Balance": liability_balance
})

# Melt dataframe for visualization
df_melted = df.melt("Year", var_name="Category", value_name="Balance")

# Plot stacked bar chart
bar_chart = alt.Chart(df_melted).mark_bar().encode(
    x=alt.X("Year:O", axis=alt.Axis(title="Year")),
    y=alt.Y("Balance:Q", stack="normalize", axis=alt.Axis(title="Balance")),
    color=alt.Color("Category:N", legend=alt.Legend(title="Category"), scale=alt.Scale(scheme="dark2")),
    tooltip=["Year", "Balance", "Category"]
).properties(
    width=700,
    height=400,
    title="Comprehensive Cashflow Model"
)

st.altair_chart(bar_chart)
