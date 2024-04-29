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
    current_age = st.slider("Current age", 20, 80, 30)
    retirement_age = st.slider("Retirement age", current_age + 1, 80, 60)
    initial_super_bal = st.number_input("Initial superannuation balance", min_value=1, max_value=1000000, value=250000)
    
    st.subheader("Initial Asset Balances")
    initial_asset_balances = {
        "Home": st.number_input("Initial home balance", min_value=0, max_value=1000000, value=100000),
        "Property": st.number_input("Initial property balance", min_value=0, max_value=1000000, value=150000),
        "Stocks": st.number_input("Initial stocks balance", min_value=0, max_value=1000000, value=200000),
        "Bonds": st.number_input("Initial bonds balance", min_value=0, max_value=1000000, value=100000)
    }
    
    st.subheader("Annual Contributions to Assets")
    annual_asset_contributions = {
        "Home": st.number_input("Annual contribution to home", min_value=0, max_value=50000, value=5000),
        "Property": st.number_input("Annual contribution to property", min_value=0, max_value=50000, value=5000),
        "Stocks": st.number_input("Annual contribution to stocks", min_value=0, max_value=50000, value=5000),
        "Bonds": st.number_input("Annual contribution to bonds", min_value=0, max_value=50000, value=5000)
    }
    
    st.subheader("Expenses")
    initial_expenses = {
        "Liabilities": st.number_input("Initial liabilities balance", min_value=0, max_value=1000000, value=50000)
    }
    annual_expenses = {
        "Liabilities": st.number_input("Annual liabilities payment", min_value=0, max_value=50000, value=5000)
    }
    
    st.subheader("Asset Returns (%)")
    asset_rois = {
        "Superannuation": st.number_input("Superannuation return percentage", min_value=0, max_value=25, value=4),
        "Home": st.number_input("Home return percentage", min_value=0, max_value=25, value=3),
        "Property": st.number_input("Property return percentage", min_value=0, max_value=25, value=5),
        "Stocks": st.number_input("Stocks return percentage", min_value=0, max_value=25, value=7),
        "Bonds": st.number_input("Bonds return percentage", min_value=0, max_value=25, value=2)
    }
    
    st.subheader("Liability Returns (%)")
    liability_roi = st.number_input("Liability return percentage", min_value=0, max_value=25, value=2)
    
    st.subheader("Inflation Rate (%)")
    inflation_rate = st.number_input("Inflation rate", min_value=0, max_value=10, value=2)
    
    st.subheader("Life Expectancy")
    life_expectancy = st.number_input("Life expectancy", min_value=80, max_value=100, value=85)

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
