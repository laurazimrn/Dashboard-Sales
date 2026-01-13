import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import time
from datetime import datetime

engine = create_engine('postgresql://postgres:password@localhost:5432/sales_dashboard')

st.set_page_config(page_title="Live Sales Dashboard", layout="wide")
st.title("📊 Real-Time Sales Dashboard")
st.write("⏱️ Auto-refreshes every 60 seconds. Click the button below to manually refresh.")

if 'last_refresh' not in st.session_state:
    st.session_state['last_refresh'] = datetime.now()

if st.button("🔄 Manual Refresh Now"):
    st.session_state['last_refresh'] = datetime.now()

st.caption(f"Last refreshed: {st.session_state['last_refresh'].strftime('%Y-%m-%d %H:%M:%S')}")

@st.cache_data(ttl=60)
def load_data():
    query = "SELECT * FROM sales_data ORDER BY sale_time DESC LIMIT 100;"
    df = pd.read_sql(query, engine)
    return df

df = load_data()

st.subheader("Recent Sales Data")
st.dataframe(df)

st.subheader("Sales by Product")
fig = px.bar(df, x='product', y='total_sales', color='region', title="Total Sales per Product")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Sales by Region")
region_data = df.groupby("region")["total_sales"].sum().reset_index()
fig2 = px.pie(region_data, values="total_sales", names="region", title="Sales by Region")
st.plotly_chart(fig2, use_container_width=True)

time.sleep(60)
st.rerun()  # Use st.rerun() instead of st.experimental_rerun()