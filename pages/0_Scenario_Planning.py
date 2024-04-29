import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Function to calculate balance at each year
def calculate_balance(current_age, super_bal, annual_contribution, retirement_age, roi, inflation_rate, income_replacement_ratio, life_expectancy):
    years = np.arange(current_age, life_expectancy + 1)
    balance = np.zeros(len(years))
    balance[0] = super_bal
    annual_expenses = super_bal * (income_replacement_ratio / 100)
    for i in range(1, len(years)):
        balance[i] = (balance[i - 1] * (1 + roi / 100) + annual_contribution) / (1 + inflation_rate / 100)
        if i >= retirement_age - current_age:
            balance[i] -= annual_expenses
    return years, balance

# Streamlit app
st.title("Scenario Modeling")
