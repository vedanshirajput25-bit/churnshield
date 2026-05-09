"""
ChurnShield - Streamlit Dashboard
AI-Powered Customer Churn Predictor for Small Indian E-Commerce Sellers
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from model import predict_churn
from generate_sample_data import generate_dataset

st.set_page_config(page_title="ChurnShield", page_icon="shield", layout="wide")

st.markdown("""
<style>
.metric-card{background:white;border-radius:12px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,0.08);text-align:center}
.metric-val{font-size:2.2rem;font-weight:800;margin:0}
.metric-lbl{font-size:0.85rem;color:#64748b;margin:0}
.stButton>button{background:#0d9488;color:white;border:none;border-radius:8px;padding:0.5rem 1.5rem;font-weight:600}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## ChurnShield")
    st.markdown("*Predict. Retain. Grow.*")
    st.markdown("---")
    st.markdown("### Upload Your Data")
    uploaded = st.file_uploader("Upload customer CSV", type=["csv"])
    st.markdown("**Required columns:**")
    st.code("customer_name\nlast_order_date\nnum_orders\ntotal_spend", language="text")
    st.markdown("---")
    use_sample = st.button("Use Sample Data (200 customers)")
    st.markdown("---")
    st.markdown("""
**Risk Levels:**
- High — 46+ days inactive
- Medium — 21-45 days inactive
- Low — Active in last 20 days

Built for BluePrint 2026
    """)

st.markdown("# ChurnShield Dashboard")
st.markdown("##### AI-Powered Churn Predictor for Indian E-Commerce Sellers")
st.markdown("---")

df_raw = None
if uploaded:
    df_raw = pd.read_csv(uploaded)
    st.success(f"Loaded {len(df_raw)} customers from uploaded file.")
elif use_sample or st.session_state.get("use_sample"):
    st.session_state["use_sample"] = True
    df_raw = generate_dataset(200)
    st.info("Using sample dataset of 200 customers.")

if df_raw is None:
    st.markdown("""
    <div style='text-align:center;padding:60px;background:white;border-radius:16px;margin-top:40px;box-shadow:0 2px 12px rgba(0,0,0,0.06)'>
        <h2>Welcome to ChurnShield!</h2>
        <p style='color:#64748b;font-size:1.1rem'>Upload your customer CSV or click <b>Use Sample Data</b> to get started.</p>
        <p style='font-size:2rem'>Upload → Analyse → Retain</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

with st.spinner("Analysing customer data..."):
    df, model = predict_churn(df_raw)

# KPI cards
total       = len(df)
high_risk   = len(df[df["churn_risk"] == "High"])
medium_risk = len(df[df["churn_risk"] == "Medium"])
low_risk    = len(df[df["churn_risk"] == "Low"])
rev_at_risk = df[df["churn_risk"] == "High"]["total_spend"].sum()

c1, c2, c3, c4, c5 = st.columns(5)
for col, val, lbl, color in [
    (c1, total, "Total Customers", "#0d1b2a"),
    (c2, high_risk, "High Risk", "#ef4444"),
    (c3, medium_risk, "Medium Risk", "#f59e0b"),
    (c4, low_risk, "Loyal", "#10b981"),
    (c5, f"Rs.{rev_at_risk:,.0f}", "Revenue at Risk", "#f59e0b"),
]:
    col.markdown(f"""<div class='metric-card'>
        <p class='metric-val' style='color:{color}'>{val}</p>
        <p class='metric-lbl'>{lbl}</p></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Charts
ch1, ch2 = st.columns(2)
with ch1:
    st.markdown("#### Customer Risk Distribution")
    risk_counts = df["churn_risk"].value_counts().reindex(["High", "Medium", "Low"]).fillna(0)
    fig = px.pie(values=risk_counts.values, names=risk_counts.index, hole=0.45,
                 color=risk_counts.index,
                 color_discrete_map={"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"})
    fig.update_layout(margin=dict(t=10, b=10), height=300)
    st.plotly_chart(fig, use_container_width=True)

with ch2:
    st.markdown("#### RFM Score vs Days Inactive")
    fig2 = px.scatter(df, x="recency", y="rfm_score", color="churn_risk",
                      color_discrete_map={"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"},
                      labels={"recency": "Days Since Last Order", "rfm_score": "RFM Score"},
                      hover_data=["customer_name", "total_spend"])
    fig2.update_layout(margin=dict(t=10, b=10), height=300)
    st.plotly_chart(fig2, use_container_width=True)

# Table
st.markdown("---")
st.markdown("#### Customer Churn Risk Table")
rf, search_col = st.columns([2, 4])
risk_filter = rf.selectbox("Filter by Risk", ["All", "High", "Medium", "Low"])
search = search_col.text_input("Search by name", placeholder="e.g. Anjali")

display = df.copy()
if risk_filter != "All":
    display = display[display["churn_risk"] == risk_filter]
if search:
    display = display[display["customer_name"].str.contains(search, case=False, na=False)]

show = ["customer_name", "last_order_date", "num_orders", "total_spend", "recency", "rfm_score", "churn_risk", "churn_probability"]
rename = {"customer_name": "Customer", "last_order_date": "Last Order", "num_orders": "Orders",
          "total_spend": "Total Spend", "recency": "Days Inactive", "rfm_score": "RFM Score",
          "churn_risk": "Risk Level", "churn_probability": "Churn %"}

def color_risk(val):
    return {"High": "background-color:#fee2e2", "Medium": "background-color:#fef3c7",
            "Low": "background-color:#d1fae5"}.get(val, "")

styled = (display[show].rename(columns=rename)
          .sort_values("Days Inactive", ascending=False)
          .style.applymap(color_risk, subset=["Risk Level"])
          .format({"Total Spend": "Rs.{:,.0f}", "RFM Score": "{:.2f}", "Churn %": "{:.1f}%"}))
st.dataframe(styled, use_container_width=True, height=380)

# Retention messages
st.markdown("---")
st.markdown("#### WhatsApp Retention Messages")
st.markdown("Personalised messages for your high-risk customers — copy and send on WhatsApp!")

for _, row in df[df["churn_risk"] == "High"].sort_values("recency", ascending=False).head(10).iterrows():
    with st.expander(f"HIGH RISK: {row['customer_name']} — {row['recency']} days inactive — Rs.{row['total_spend']:,.0f} spent"):
        st.info(row["retention_message"])
        st.code(row["retention_message"])

# Download
st.markdown("---")
csv_out = display[show].rename(columns=rename).to_csv(index=False).encode("utf-8")
st.download_button("Download Full Report as CSV", data=csv_out,
                   file_name="churnshield_report.csv", mime="text/csv")

st.markdown("<br><center><sub>ChurnShield - Built for BluePrint 2026 - P P Savani University</sub></center>",
            unsafe_allow_html=True)
