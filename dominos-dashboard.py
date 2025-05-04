import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page configuration
st.set_page_config(page_title="Domino's Sales Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("dominos_sales_data.csv")

df = load_data()

# Title and Description
st.title("Domino's Sales Performance Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
dates = pd.to_datetime(df['Date'])
df['Date'] = dates
start_date, end_date = st.sidebar.date_input("Select Date Range", [dates.min(), dates.max()])

staff_filter = st.sidebar.multiselect("Select Staff", options=df['Staff'].unique(), default=df['Staff'].unique())
payment_filter = st.sidebar.multiselect("Select Payment Method", options=df['Payment Method'].unique(), default=df['Payment Method'].unique())

# Apply filters
filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) &
                 (df['Date'] <= pd.to_datetime(end_date)) &
                 (df['Staff'].isin(staff_filter)) &
                 (df['Payment Method'].isin(payment_filter))]

# KPIs
st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${filtered_df['Total Price'].sum():,.2f}")
col2.metric("Total Orders", len(filtered_df))
col3.metric("Average Order Value", f"${filtered_df['Total Price'].mean():.2f}")
col4.metric("Total Items Sold", filtered_df['Quantity'].sum())

# Charts
st.subheader("Sales Trend Over Time")
sales_by_date = filtered_df.groupby("Date")["Total Price"].sum().reset_index()
fig1, ax1 = plt.subplots()
ax1.plot(sales_by_date['Date'], sales_by_date['Total Price'], marker='o')
ax1.set_title("Daily Revenue")
ax1.set_xlabel("Date")
ax1.set_ylabel("Revenue ($)")
plt.xticks(rotation=45)
st.pyplot(fig1)

st.subheader("Top Selling Items")
top_items = filtered_df.groupby("Item")["Quantity"].sum().sort_values(ascending=False).head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_items.values, y=top_items.index, ax=ax2)
ax2.set_title("Top 10 Items by Quantity Sold")
ax2.set_xlabel("Quantity Sold")
st.pyplot(fig2)

st.subheader("Staff Performance")
staff_perf = filtered_df.groupby("Staff")["Total Price"].sum().sort_values(ascending=False)
fig3, ax3 = plt.subplots()
sns.barplot(x=staff_perf.values, y=staff_perf.index, ax=ax3)
ax3.set_title("Revenue by Staff")
ax3.set_xlabel("Total Revenue ($)")
st.pyplot(fig3)

# Enhancements
st.sidebar.markdown("---")
st.sidebar.markdown("### Additional Insights")
if st.sidebar.checkbox("Show Hourly Sales Heatmap"):
    df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M').dt.hour
    heatmap_data = df.groupby(['Hour', 'Date'])['Total Price'].sum().unstack(fill_value=0)
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    sns.heatmap(heatmap_data, cmap="YlGnBu", ax=ax4)
    ax4.set_title("Hourly Sales Heatmap")
    st.pyplot(fig4)

if st.sidebar.checkbox("Show Payment Method Breakdown"):
    payment_breakdown = filtered_df['Payment Method'].value_counts()
    fig5, ax5 = plt.subplots()
    ax5.pie(payment_breakdown.values, labels=payment_breakdown.index, autopct='%1.1f%%', startangle=90)
    ax5.axis('equal')
    st.pyplot(fig5)

st.markdown("---")
st.markdown("Dashboard created for stakeholder analysis to optimize operations and maximize profitability.")
