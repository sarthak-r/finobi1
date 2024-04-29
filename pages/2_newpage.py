import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Function to calculate cashflows for each year
def calculate_cashflows(current_age, retirement_age, initial_super_bal, initial_asset_balances, 
                        annual_super_contribution, annual_assets_roi, initial_liabilities, 
                        annual_expenses, inflation_rate, life_expectancy):
    
    years = np.arange(current_age, life_expectancy + 1)
    super_balance = np.zeros(len(years))
    total_assets = np.zeros(len(years))
    total_liabilities = np.zeros(len(years))
    net_cash = np.zeros(len(years))

    super_balance[0] = initial_super_bal
    total_assets[0] = initial_super_bal + sum(initial_asset_balances.values())
    total_liabilities[0] = sum(initial_liabilities.values())
    
    for i in range(1, len(years)):
        if years[i] <= retirement_age:
            super_contribution = annual_super_contribution
        else:
            super_contribution = 0
            
        super_balance[i] = super_balance[i - 1] * (1 + annual_assets_roi / 100) + super_contribution
        total_assets[i] = total_assets[i - 1]*(1 + annual_assets_roi / 100) - annual_expenses*(1 + inflation_rate / 100)
        
        if total_assets[i] < 0:
            total_liabilities[i] = total_liabilities[i - 1]*(1 + inflation_rate / 100) + total_assets[i]
            total_assets[i] = 0
        else:
            total_liabilities[i] = total_liabilities[i - 1]*(1 + inflation_rate / 100)
            
        net_cash[i] = super_balance[i] + total_assets[i] - total_liabilities[i]
        
    return years, super_balance, total_assets, total_liabilities, net_cash

def main():
    st.title("Comprehensive Cashflow Modelling")
    
    st.header("Financial Inputs")
    current_age = st.slider("Current age", 20, 80, 30)
    retirement_age = st.slider("Retirement age", current_age+1, 100, 65)
    
    st.subheader("Superannuation")
    initial_super_bal = st.slider("Initial balance", 1, 10000000, 25000)
    annual_super_contribution = st.slider("Annual contribution", 0, 5000000, 15000)
    
    st.subheader("Assets")
    initial_asset_balances = {
        "Cash": st.slider("Initial cash balance", 0, 5000000, 10000),
        "Investments": st.slider("Initial investments balance", 0, 5000000, 25000) 
    }
    
    annual_super_roi = st.slider("Annual return on super", 1, 15, 3)
    
    st.subheader("Liabilities")
    initial_liabilities = {
        "Mortgage": st.slider("Mortgage", 0, 2000000, 50000),
        "Loans": st.slider("Loans", 0, 2000000, 10000)
    }
    
    annual_expenses = st.slider("Annual expenses", 0, 200000, 10000)
    
    st.subheader("Rates")
    inflation_rate = st.slider("Inflation rate", 0, 10, 2)
    
    st.subheader("Life Expectancy")
    life_expectancy = st.slider("Life expectancy", 80, 130, 100)
    
    years, super_balance, total_assets, total_liabilities, net_cash = calculate_cashflows(current_age, retirement_age, 
                                                                                         initial_super_bal, 
                                                                                         initial_asset_balances, 
                                                                                         annual_super_contribution, 
                                                                                         annual_super_roi, 
                                                                                         initial_liabilities,
                                                                                         annual_expenses,
                                                                                         inflation_rate, life_expectancy)


# Create dataframe for visualization
    df_super = pd.DataFrame({
        "Year": years,
        "Superannuation Balance": super_balance
    })

    df_assets = pd.DataFrame({
        "Year": years,
        "Total Assets": total_assets
    })

    df_liabilities = pd.DataFrame({
        "Year": years,
        "Liabilities": liabilities
    })

    df_net_worth = pd.DataFrame({
        "Year": years,
        "Net Worth": net_worth
    })

    # Plot charts
    chart_super = alt.Chart(df_super).mark_bar().encode(
        x='Year',
        y=alt.Y('Superannuation Balance', axis=alt.Axis(title="Superannuation Balance ($)", format="$,.0f")),
        tooltip=['Year', alt.Tooltip('Superannuation Balance', format='$,.0f')]
    ).properties(
        width=700,
        height=200,
        title="Superannuation Balance"
    )

    chart_assets = alt.Chart(df_assets).mark_bar().encode(
        x='Year',
        y=alt.Y('Total Assets', axis=alt.Axis(title="Total Assets ($)", format="$,.0f")),
        tooltip=['Year', alt.Tooltip('Total Assets', format='$,.0f')]
    ).properties(
        width=700,
        height=200,
        title="Total Assets"
    )

    chart_liabilities = alt.Chart(df_liabilities).mark_bar().encode(
        x='Year',
        y=alt.Y('Liabilities', axis=alt.Axis(title="Liabilities ($)", format="$,.0f")),
        tooltip=['Year', alt.Tooltip('Liabilities', format='$,.0f')]
    ).properties(
        width=700,
        height=200,
        title="Liabilities"
    )

    chart_net_worth = alt.Chart(df_net_worth).mark_bar().encode(
        x='Year',
        y=alt.Y('Net Worth', axis=alt.Axis(title="Net Worth ($)", format="$,.0f")),
        tooltip=['Year', alt.Tooltip('Net Worth', format='$,.0f')]
    ).properties(
        width=700,
        height=200,
        title="Net Worth"
    )

    st.altair_chart(chart_super)
    st.altair_chart(chart_assets)
    st.altair_chart(chart_liabilities)
    st.altair_chart(chart_net_worth)

# Run the app
if __name__ == "__main__":
    main()
