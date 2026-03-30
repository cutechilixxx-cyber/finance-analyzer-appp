import streamlit as st
import pandas as pd

st.set_page_config(page_title="Financial Analyzer", page_icon="📈")

st.title("📈 Financial Analysis Tool")
st.write("Calculate loan parameters and compare offers instantly.")

# Ввод данных
col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("Loan Amount", min_value=1000, value=100000, step=1000)
    interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.1, value=15.0, step=0.1)
    
with col2:
    years = st.number_input("Term (Years)", min_value=1, value=5)
    
# Математический расчет (Формула аннуитета)
monthly_rate = interest_rate / 100 / 12
months = years * 12
monthly_payment = (amount * monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
total_payment = monthly_payment * months
total_interest = total_payment - amount

# Вывод результатов
st.divider()
st.subheader("📊 Calculation Results")
res_col1, res_col2, res_col3 = st.columns(3)

res_col1.metric("Monthly Payment", f"{monthly_payment:,.2f}")
res_col2.metric("Total Interest", f"{total_interest:,.2f}")
res_col3.metric("Total to Repay", f"{total_payment:,.2f}")

# График платежей
st.subheader("📅 Payment Schedule")
schedule = []
remaining_balance = amount

for i in range(1, months + 1):
    interest_part = remaining_balance * monthly_rate
    principal_part = monthly_payment - interest_part
    remaining_balance -= principal_part
    schedule.append([i, monthly_payment, principal_part, interest_part, max(0, remaining_balance)])

df = pd.DataFrame(schedule, columns=["Month", "Payment", "Principal", "Interest", "Balance"])
st.dataframe(df.style.format("{:.2f}"))

st.line_chart(df["Balance"])
