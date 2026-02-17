import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Financial Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .section-header {
        font-size: 24px;
        font-weight: 600;
        color: #1e3c72;
        margin-top: 30px;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #e0e0e0;
    }
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
    .kpi-value {
        font-size: 36px;
        font-weight: bold;
    }
    .kpi-label {
        font-size: 14px;
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("bi_dataset.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ File 'bi_dataset.csv' not found. Please ensure the file exists in the project directory.")
    st.stop()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Date range filter
min_date = df["date"].min()
max_date = df["date"].max()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Department filter
departments = ["All"] + sorted(df["department"].unique().tolist())
selected_dept = st.sidebar.selectbox("Select Department", departments)

# Apply filters
filtered_df = df.copy()
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["date"] >= pd.to_datetime(date_range[0])) &
        (filtered_df["date"] <= pd.to_datetime(date_range[1]))
    ]
if selected_dept != "All":
    filtered_df = filtered_df[filtered_df["department"] == selected_dept]

# Header
st.title("📊 Financial Performance Dashboard")
st.markdown(f"**Period:** {filtered_df['date'].min().strftime('%B %Y')} - {filtered_df['date'].max().strftime('%B %Y')}")
st.markdown("---")

# ==================== KPI CARDS ====================
st.markdown('<p class="section-header">📈 Executive Summary</p>', unsafe_allow_html=True)

total_revenue = filtered_df["revenue"].sum()
total_profit = filtered_df["profit"].sum()
avg_margin = filtered_df["gross_margin"].mean() * 100

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Revenue</div>
        <div class="kpi-value">${total_revenue:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Profit</div>
        <div class="kpi-value">${total_profit:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Average Gross Margin</div>
        <div class="kpi-value">{avg_margin:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Additional KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Operating Cost", f"${filtered_df['operating_cost'].sum():,.0f}")
with col2:
    st.metric("Total Payroll Cost", f"${filtered_df['payroll_cost'].sum():,.0f}")
with col3:
    st.metric("Avg Payroll Ratio", f"{filtered_df['payroll_ratio'].mean()*100:.1f}%")
with col4:
    st.metric("Total Records", f"{len(filtered_df):,}")

# ==================== REVENUE & PROFIT TREND ====================
st.markdown('<p class="section-header">📉 Revenue & Profit Trend</p>', unsafe_allow_html=True)

# Aggregate by month
monthly_df = filtered_df.groupby(filtered_df["date"].dt.to_period("M")).agg({
    "revenue": "sum",
    "profit": "sum"
}).reset_index()
monthly_df["date"] = monthly_df["date"].dt.to_timestamp()

fig_trend = make_subplots(specs=[[{"secondary_y": True}]])

fig_trend.add_trace(
    go.Scatter(x=monthly_df["date"], y=monthly_df["revenue"], name="Revenue",
               mode="lines+markers", line=dict(color="#667eea", width=3)),
    secondary_y=False
)

fig_trend.add_trace(
    go.Scatter(x=monthly_df["date"], y=monthly_df["profit"], name="Profit",
               mode="lines+markers", line=dict(color="#764ba2", width=3)),
    secondary_y=True
)

fig_trend.update_layout(
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    paper_bgcolor="white",
    plot_bgcolor="white"
)
fig_trend.update_yaxes(title_text="Revenue ($)", secondary_y=False, showgrid=True, gridcolor="#f0f0f0")
fig_trend.update_yaxes(title_text="Profit ($)", secondary_y=True, showgrid=False)

st.plotly_chart(fig_trend, use_container_width=True)

# ==================== DEPARTMENT ANALYSIS ====================
st.markdown('<p class="section-header">🏢 Department Performance</p>', unsafe_allow_html=True)

dept_summary = filtered_df.groupby("department").agg({
    "revenue": "sum",
    "profit": "sum",
    "gross_margin": "mean"
}).reset_index()
dept_summary["gross_margin_pct"] = dept_summary["gross_margin"] * 100

col1, col2 = st.columns(2)

with col1:
    fig_dept_rev = px.bar(
        dept_summary.sort_values("revenue", ascending=True),
        x="revenue", y="department", orientation="h",
        title="Revenue by Department",
        color="revenue", color_continuous_scale="Blues",
        text_auto="$,.0f"
    )
    fig_dept_rev.update_layout(paper_bgcolor="white", plot_bgcolor="white", showlegend=False)
    st.plotly_chart(fig_dept_rev, use_container_width=True)

with col2:
    fig_dept_profit = px.bar(
        dept_summary.sort_values("profit", ascending=True),
        x="profit", y="department", orientation="h",
        title="Profit by Department",
        color="profit", color_continuous_scale="Greens",
        text_auto="$,.0f"
    )
    fig_dept_profit.update_layout(paper_bgcolor="white", plot_bgcolor="white", showlegend=False)
    st.plotly_chart(fig_dept_profit, use_container_width=True)

# ==================== MARGIN COMPARISON ====================
st.markdown('<p class="section-header">📊 Margin Comparison by Department</p>', unsafe_allow_html=True)

fig_margin = px.bar(
    dept_summary.sort_values("gross_margin_pct", ascending=True),
    x="gross_margin_pct", y="department", orientation="h",
    title="Gross Margin % by Department",
    color="gross_margin_pct", color_continuous_scale="RdYlGn",
    text=".1f%"
)
fig_margin.update_layout(
    paper_bgcolor="white",
    plot_bgcolor="white",
    showlegend=False,
    xaxis_title="Gross Margin (%)",
    xaxis=dict(showgrid=True, gridcolor="#f0f0f0")
)
st.plotly_chart(fig_margin, use_container_width=True)

# ==================== MONTH-OVER-MONTH VARIANCE ====================
st.markdown('<p class="section-header">📅 Month-over-Month Variance</p>', unsafe_allow_html=True)

mom_df = filtered_df.groupby(filtered_df["date"].dt.to_period("M")).agg({
    "revenue": "sum",
    "profit": "sum"
}).reset_index()
mom_df["date"] = mom_df["date"].dt.to_timestamp()
mom_df = mom_df.sort_values("date")
mom_df["revenue_mom_change"] = mom_df["revenue"].pct_change() * 100
mom_df["profit_mom_change"] = mom_df["profit"].pct_change() * 100

mom_display = mom_df.copy()
mom_display["date"] = mom_display["date"].dt.strftime("%B %Y")
mom_display["revenue"] = mom_display["revenue"].apply(lambda x: f"${x:,.0f}")
mom_display["profit"] = mom_display["profit"].apply(lambda x: f"${x:,.0f}")
mom_display["revenue_mom_change"] = mom_display["revenue_mom_change"].apply(lambda x: f"{x:+.1f}%" if pd.notna(x) else "-")
mom_display["profit_mom_change"] = mom_display["profit_mom_change"].apply(lambda x: f"{x:+.1f}%" if pd.notna(x) else "-")

st.dataframe(
    mom_display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "date": st.column_config.TextColumn("Month"),
        "revenue": st.column_config.TextColumn("Revenue"),
        "profit": st.column_config.TextColumn("Profit"),
        "revenue_mom_change": st.column_config.TextColumn("Revenue MoM %"),
        "profit_mom_change": st.column_config.TextColumn("Profit MoM %")
    }
)

# ==================== RAW DATA ====================
st.markdown('<p class="section-header">📋 Raw Data</p>', unsafe_allow_html=True)

with st.expander("View Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)

# Download filtered data
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_financial_data.csv",
    mime="text/csv"
)
