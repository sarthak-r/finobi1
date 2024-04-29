import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Function to calculate cashflows for each year
def calculate_cashflows(current_age, retirement_age, initial_super_bal, initial_asset_balances, 
                        annual_super_contribution, annual_asset_contributions, annual_expenses, 
                        asset_rois, liability_roi, inflation_rate, life_expectancy):
    years = np.arange(current_age, life_expectancy + 1)
    super_balance = np.zeros(len(years))
    asset_balances = {asset: np.zeros(len(years)) for asset in initial_asset_balances.keys()}
    liability_balance = np.zeros(len(years))
    
    # Set initial balances
    super_balance[0] = initial_super_bal
    for asset, balance in initial_asset_balances.items():
        asset_balances[asset][0] = balance
    
    for i in range(1, len(years)):
        # Calculate super contributions and returns
        super_contribution = annual_super_contribution
        super_balance[i] = super_balance[i-1] * (1 + asset_rois["Superannuation"] / 100) + super_contribution
        
        # Calculate asset contributions and returns
        for asset, balance in asset_balances.items():
            asset_contribution = annual_asset_contributions[asset]
            asset_balances[asset][i] = balance[i-1] * (1 + asset_rois[asset] / 100) + asset_contribution
        
        # Calculate liabilities
        liability_balance[i] = liability_balance[i-1] * (1 + liability_roi / 100) / (1 + inflation_rate / 100) + annual_expenses["Liabilities"]
        
    return years, super_balance, asset_balances, liability_balance

# Streamlit app
st.title("Enhanced Cashflow Modeling")

# Financial inputs
current_age = st.slider("Current age", 20, 80, 30)
retirement_age = st.slider("Retirement age", current_age + 1, 80, 60)
initial_super_bal = st.slider("Initial superannuation balance", 1, 1000000, 250000)
initial_asset_balances = {
    "Home": st.slider("Initial home balance", 0, 1000000, 100000),
    "Property": st.slider("Initial property balance", 0, 1000000, 150000),
    "Stocks": st.slider("Initial stocks balance", 0, 1000000, 200000),
    "Bonds": st.slider("Initial bonds balance", 0, 1000000, 100000)
}
annual_super_contribution = st.slider("Annual contribution to superannuation", 0, 50000, 10000)
annual_asset_contributions = {
    "Home": st.slider("Annual contribution to home", 0, 50000, 5000),
    "Property": st.slider("Annual contribution to property", 0, 50000, 5000),
    "Stocks": st.slider("Annual contribution to stocks", 0, 50000, 5000),
    "Bonds": st.slider("Annual contribution to bonds", 0, 50000, 5000)
}
annual_expenses = {
    "Living Expenses": st.slider("Annual living expenses", 0, 50000, 20000),
    "Healthcare": st.slider("Annual healthcare expenses", 0, 50000, 10000),
    "Leisure": st.slider("Annual leisure expenses", 0, 50000, 5000),
    "Liabilities": st.slider("Annual liabilities", 0, 50000, 5000)
}
asset_rois = {
    "Superannuation": st.slider("Superannuation return percentage", 0, 25, 4),
    "Home": st.slider("Home return percentage", 0, 25, 3),
    "Property": st.slider("Property return percentage", 0, 25, 5),
    "Stocks": st.slider("Stocks return percentage", 0, 25, 7),
    "Bonds": st.slider("Bonds return percentage", 0, 25, 2)
}
liability_roi = st.slider("Liability return percentage", 0, 25, 2)
inflation_rate = st.slider("Inflation rate", 0, 10, 2)
life_expectancy = st.slider("Life expectancy", 80, 100, 85)

# Calculate cashflows
years, super_balance, asset_balances, liability_balance = calculate_cashflows(current_age, retirement_age, 
                                                                             initial_super_bal, initial_asset_balances, 
                                                                             annual_super_contribution, 
                                                                             annual_asset_contributions, 
                                                                             annual_expenses, asset_rois, 
                                                                             liability_roi, inflation_rate, 
                                                                             life_expectancy)

# Create dataframe for visualization
df = pd.DataFrame({
    "Year": years,
    "Superannuation Balance": super_balance,
    **asset_balances,
    "Liability Balance": liability_balance
})

# Melt dataframe for visualization
df_melted = df.melt("Year", var_name="Category", value_name="Balance")

# Plot grouped bar chart
bar_chart = alt.Chart(df_melted).mark_bar().encode(
    x=alt.X("Year:O", axis=alt.Axis(title="Year")),
    y=alt.Y("Balance:Q", axis=alt.Axis(title="Balance ($)", format="$,.0f")),
    color=alt.Color("Category:N", legend=alt.Legend(title="Category"), scale=alt.Scale(scheme="dark2")),
    column=alt.Column("Category:N", title=None)
).properties(
    width=150,
    height=400,
    title="Enhanced Cashflow Model"
)

st.altair_chart(bar_chart)
