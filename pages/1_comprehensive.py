import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Function to calculate cashflows for each year
def calculate_cashflows(current_age, retirement_age, initial_super_bal, initial_asset_balances, 
                        annual_super_contribution, annual_asset_contributions, initial_expenses, 
                        annual_expenses, monthly_expenses, asset_rois, liability_roi, inflation_rate, life_expectancy):
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
    
    # Calculate monthly liabilities
    monthly_liabilities = initial_expenses["Liabilities"] / 12
    
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
        
        # Calculate monthly income and expenses
        monthly_income = super_contribution / 12
        monthly_expense = monthly_expenses * ((1 + inflation_rate / 100) ** (years[i] - current_age))
        
        # Calculate liabilities
        liabilities[i] = liabilities[i-1] * (1 + liability_roi / 100) * (1 + inflation_rate / 100)
        
        # Calculate net worth
        net_worth[i] = total_assets[i] - liabilities[i] + monthly_income - monthly_expense
        
        # Prevent negative liabilities
        if liabilities[i] < 0:
            liabilities[i] = 0
        
    return years, super_balance, total_assets, liabilities, net_worth

# Streamlit app
def main():
    """Main function to run the Streamlit app."""
    st.title("Comprehensive Cashflow Modeling")



    # Financial inputs
    st.header("Financial Inputs")
    current_age = st.slider("Current age", 20, 80, 30)
    retirement_age = st.slider("Retirement age", current_age + 1, 80, 60)
    
    #######################
    #######################



    class Asset:
        def __init__(self, name, asset_type, value, growth=0, **kwargs):
            self.name = name
            self.asset_type = asset_type
            self.value = value
            self.growth = growth

    def add_asset():
        asset_name = st.text_input("Asset Name", "e.g. Secondary home")
        asset_type = st.text_input("Asset Type", "e.g. real estate")
        asset_value = st.slider("Asset Value", 1, 1000000, 800000)
        asset_growth = st.slider("Asset Growth", 0, 50, 6)
        return Asset(asset_name, asset_type, asset_value, asset_growth)

    class Liability:
        def __init__(self, name, liability_type, value, interest, **kwargs):
            self.name = name
            self.liability_type = liability_type
            self.current_value = value
            self.interest = interest

    def add_liability():
        liability_name = st.text_input("Liability Name", "e.g. Mortgage")
        liability_type = st.text_input("Liability Type", "e.g. Home loan")
        liability_value = st.slider("Liability Value", 1, 1000000, 500000)
        liability_interest = st.slider("Liability Interest", 0, 20, 5)
        return Liability(liability_name, liability_type, liability_value, liability_interest)

    class Income:
        def __init__(self, name, frequency, current_value, growth=0, **kwargs):
            self.name = name
            self.frequency = frequency
            self.current_value = current_value
            self.growth = growth

    def add_income():
        income_name = st.text_input("Income Name", "e.g. Salary")
        income_frequency = st.text_input("Income Frequency", "e.g. Monthly")
        income_value = st.slider("Income Value", 1, 100000, 50000)
        income_growth = st.slider("Income Growth", 0, 20, 3)
        return Income(income_name, income_frequency, income_value, income_growth)

    class Expense:
        def __init__(self, name, frequency, current_value, growth=0):
            self.name = name
            self.frequency = frequency
            self.current_value = current_value
            self.growth = growth

    def add_expense():
        expense_name = st.text_input("Expense Name", "e.g. Rent")
        expense_frequency = st.text_input("Expense Frequency", "e.g. Monthly")
        expense_value = st.slider("Expense Value", 1, 10000, 2000)
        expense_growth = st.slider("Expense Growth", 0, 20, 2)
        return Expense(expense_name, expense_frequency, expense_value, expense_growth)

    st.subheader("Assets")
    assets = []
    while st.button("Add More Assets"):
        asset = add_asset()
        assets.append(asset)

    st.subheader("Liabilities")
    liabilities = []
    while st.button("Add More Liabilities"):
        liability = add_liability()
        liabilities.append(liability)

    st.subheader("Income")
    incomes = []
    while st.button("Add More Income"):
        income = add_income()
        incomes.append(income)

    st.subheader("Expenses")
    expenses = []
    while st.button("Add More Expenses"):
        expense = add_expense()
        expenses.append(expense)



    #######################
    #######################







    # Calculate cashflows
    years, super_balance, total_assets, liabilities, net_worth = calculate_cashflows(current_age, retirement_age, 
                                                                                     initial_super_bal, initial_asset_balances, 
                                                                                     annual_super_contribution, 
                                                                                     annual_asset_contributions, 
                                                                                     initial_expenses,
                                                                                     annual_expenses, monthly_expenses, 
                                                                                     asset_rois, liability_roi, 
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
