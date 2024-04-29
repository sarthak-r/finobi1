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
st.title("Retirement Cashflow Model")

current_age = st.slider("Current age", 20, 80, 30)
super_bal = st.slider("Current super balance", 100, 1000000, 250000)
annual_contribution = st.slider("Annual contribution to super", 0, 50000, 10000)
retirement_age = st.slider("Retirement age", current_age + 1, 80, 60)
roi = st.slider("Return percentage", 0, 25, 7)
inflation_rate = st.slider("Inflation rate", 0, 10, 2)
income_replacement_ratio = st.slider("Income replacement ratio (%)", 50, 150, 70)
life_expectancy = st.slider("Life expectancy", 80, 100, 85)

years, balance = calculate_balance(current_age, super_bal, annual_contribution, retirement_age, roi, inflation_rate, income_replacement_ratio, life_expectancy)
df = pd.DataFrame({"Year": years, "Balance": balance})

st.write("### Cashflow Model")

# Bar chart with interactive tooltip
tooltip = [alt.Tooltip("Year:O", title="Year"), alt.Tooltip("Balance:Q", title="Balance", format=".2f")]
chart = alt.Chart(df).mark_bar().encode(
    x="Year:O",
    y="Balance:Q",
    tooltip=tooltip
).properties(
    width=700,
    height=400
)

st.altair_chart(chart, use_container_width=True)
