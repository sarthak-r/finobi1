import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Function to calculate cashflows for each year
def calculate_cashflows(current_age, retirement_age, initial_super_bal, initial_asset_balances, 
                        annual_super_contribution, annual_asset_contributions, initial_expenses, 
                        annual_expenses, asset_rois, liability_roi, inflation_rate, life_expectancy):
    """Calculate cashflows for each year based on user inputs."""
    years = np.arange(current_age, life_expectancy + 1)
    super_balance = np.zeros(len(years))
    total_assets = np.zeros(len(years))
    liabilities = np.zeros(len(years))
    net_worth = np.zeros(len(years))
    
    # Set initial balances
    super_balance[0] = initial_super_bal
    total_assets[0] = initial_super_bal + sum(initial_asset_balances.values())
    liabilities[0] = initial_expenses["Liabilities"]  # Initial liabilities
    
    for i in range(1, len(years)):
        # Calculate super contributions and returns
        if years[i] <= retirement_age:
            super_contribution = annual_super_contribution
        else:
            super_contribution = 0
        super_balance[i] = super_balance[i-1] * (1 + asset_rois["Superannuation"] / 100) + super_contribution
        
        # Calculate total asset contributions and returns
        total_asset_contribution = sum(annual_asset_contributions.values())
        total_assets[i] = total_assets[i-1] * (1 + sum(asset_rois.values()) / 100) + total_asset_contribution
        
        # Calculate liabilities
        annual_liability_payment = annual_expenses["Liabilities"]
        liabilities[i] = liabilities[i-1] * (1 + liability_roi / 100) / (1 + inflation_rate / 100) - annual_liability_payment
        
        # Calculate net worth
        net_worth[i] = total_assets[i] - liabilities[i]
        
    return years, super_balance, total_assets, liabilities, net_worth

# Streamlit app
def main():
    """Main function to run the Streamlit app."""
    st.title("Comprehensive Cashflow Modeling")

    # Financial inputs
    st.header("Financial Inputs")
    current_age = st.slider("Current age", 20, 80, 30)
    retirement_age = st.slider("Retirement age", current_age + 1, 80, 60)
    
    st.subheader("Superannuation")
    initial_super_bal = st.slider("Initial balance", 1, 1000000, 250000)
    annual_super_contribution = st.slider("Annual contribution", 0, 50000, 10000)
    
    st.subheader("Assets")
    initial_asset_balances = {
        "Home": st.slider("Initial home balance", 0, 1000000, 100000),
        "Property": st.slider("Initial property balance", 0, 1000000, 150000),
        "Stocks": st.slider("Initial stocks balance", 0, 1000000, 200000),
        "Bonds": st.slider("Initial bonds balance", 0, 1000000, 100000)
    }
    annual_asset_contributions = {
        "Home": st.slider("Annual contribution to home", 0, 50000, 5000),
        "Property": st.slider("Annual contribution to property", 0, 50000, 5000),
        "Stocks": st.slider("Annual contribution to stocks", 0, 50000, 5000),
        "Bonds": st.slider("Annual contribution to bonds", 0, 50000, 5000)
    }
    
    st.subheader("Liabilities")
    initial_expenses = {
        "Liabilities": st.slider("Initial balance", 0, 1000000, 50000)
    }
    annual_expenses = {
        "Liabilities": st.slider("Annual payment", 0, 50000, 5000)
    }
    
    st.subheader("Returns and Rates")
    asset_rois = {
        "Superannuation": st.slider("Superannuation return percentage", 0, 25, 4),
        "Home": st.slider("Home return percentage", 0, 25, 3),
        "Property": st.slider("Property return percentage", 0, 25, 5),
        "Stocks": st.slider("Stocks return percentage", 0, 25, 7),
        "Bonds": st.slider("Bonds return percentage", 0, 25, 2)
    }
    liability_roi = st.slider("Liability return percentage", 0, 25, 2)
    inflation_rate = st.slider("Inflation rate", 0, 10, 2)
    
    st.subheader("Life Expectancy")
    life_expectancy = st.slider("Life expectancy", 80, 100, 85)

    # Calculate cashflows
    years, super_balance, total_assets, liabilities, net_worth = calculate_cashflows(current_age, retirement_age, 
                                                                                     initial_super_bal, initial_asset_balances, 
                                                                                     annual_super_contribution, 
                                                                                     annual_asset_contributions, 
                                                                                     initial_expenses,
                                                                                     annual_expenses, asset_rois, 
                                                                                     liability_roi, inflation_rate, 
                                                                                     life_expectancy)

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
    chart_super = alt.Chart(df_super).mark_line().encode(
        x='Year',
        y=alt.Y('Superannuation Balance', axis=alt.Axis(title="Superannuation Balance ($)", format="$,.0f")),
        color=alt.value("blue")
    ).properties(
        width=700,
        height=200,
        title="Superannuation Balance"
    )

    chart_assets = alt.Chart(df_assets).mark_line().encode(
        x='Year',
        y=alt.Y('Total Assets', axis=alt.Axis(title="Total Assets ($)", format="$,.0f")),
        color=alt.value("green")
    ).properties(
        width=700,
        height=200,
        title="Total Assets"
    )

    chart_liabilities = alt.Chart(df_liabilities).mark_line().encode(
        x='Year',
        y=alt.Y('Liabilities', axis=alt.Axis(title="Liabilities ($)", format="$,.0f")),
        color=alt.value("red")
    ).properties(
        width=700,
        height=200,
        title="Liabilities"
    )

    chart_net_worth = alt.Chart(df_net_worth).mark_line().encode(
        x='Year',
        y=alt.Y('Net Worth', axis=alt.Axis(title="Net Worth ($)", format="$,.0f")),
        color=alt.value("purple")
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
