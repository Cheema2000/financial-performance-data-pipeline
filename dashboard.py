"""
Financial Performance BI Dashboard
Professional Streamlit dashboard for financial analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page Configuration
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
        color: #1e3a5f;
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
    .kpi-card h3 {
        font-size: 14px;
        opacity: 0.9;
        margin-bottom: 8px;
    }
    .kpi-card p {
        font-size: 32px;
        font-weight: bold;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """Load and cache the dataset"""
    df = pd.read_csv(file_path)
    return df


def format_currency(value: float) -> str:
    """Format value as currency"""
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    elif abs(value) >= 1_000:
        return f"${value/1_000:.2f}K"
    return f"${value:,.2f}"


def format_percentage(value: float) -> str:
    """Format value as percentage"""
    return f"{value*100:.2f}%"


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the data"""
    df = df.copy()

    # Convert date column
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Fill missing values for numeric columns
    numeric_cols = ['revenue', 'operating_cost', 'payroll_cost', 'profit',
                   'gross_margin', 'payroll_ratio', 'operating_cost_ratio',
                   'revenue_mom_change', 'profit_mom_change']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


def create_kpi_cards(df: pd.DataFrame) -> None:
    """Create executive KPI cards"""
    st.markdown('<p class="section-header">Executive Summary</p>', unsafe_allow_html=True)

    # Calculate KPIs
    total_revenue = df['revenue'].sum()
    total_profit = df['profit'].sum()
    avg_margin = df['gross_margin'].mean()
    avg_payroll_ratio = df['payroll_ratio'].mean()
    total_departments = df['department'].nunique()

    # Create columns for KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Revenue",
            value=format_currency(total_revenue)
        )

    with col2:
        st.metric(
            label="Total Profit",
            value=format_currency(total_profit),
            delta=format_percentage(total_profit/total_revenue) if total_revenue > 0 else "0%"
        )

    with col3:
        st.metric(
            label="Average Gross Margin",
            value=format_percentage(avg_margin),
            delta="vs target 20%" if avg_margin >= 0.2 else None
        )

    with col4:
        st.metric(
            label="Departments",
            value=total_departments
        )


def create_trend_chart(df: pd.DataFrame) -> None:
    """Create revenue and profit trend line chart"""
    st.markdown('<p class="section-header">Revenue & Profit Trends</p>', unsafe_allow_html=True)

    # Aggregate by date
    trend_df = df.groupby('date').agg({
        'revenue': 'sum',
        'profit': 'sum'
    }).reset_index()

    trend_df = trend_df.sort_values('date')

    # Create dual-axis chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Revenue line
    fig.add_trace(
        go.Scatter(
            x=trend_df['date'],
            y=trend_df['revenue'],
            name="Revenue",
            line=dict(color='#667eea', width=3),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ),
        secondary_y=False
    )

    # Profit line
    fig.add_trace(
        go.Scatter(
            x=trend_df['date'],
            y=trend_df['profit'],
            name="Profit",
            line=dict(color='#10b981', width=3),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.1)'
        ),
        secondary_y=True
    )

    fig.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        paper_bgcolor='white',
        plot_bgcolor='white',
        height=400
    )

    fig.update_yaxes(title_text="Revenue ($)", secondary_y=False, showgrid=True, gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(title_text="Profit ($)", secondary_y=True, showgrid=False)
    fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')

    st.plotly_chart(fig, width='stretch')


def create_department_chart(df: pd.DataFrame) -> None:
    """Create department-level revenue and profit bar chart"""
    st.markdown('<p class="section-header">Revenue & Profit by Department</p>', unsafe_allow_html=True)

    # Aggregate by department
    dept_df = df.groupby('department').agg({
        'revenue': 'sum',
        'profit': 'sum'
    }).reset_index()

    dept_df = dept_df.sort_values('revenue', ascending=True)

    # Create grouped bar chart
    fig = go.Figure(data=[
        go.Bar(
            y=dept_df['department'],
            x=dept_df['revenue'],
            name='Revenue',
            orientation='h',
            marker_color='#667eea'
        ),
        go.Bar(
            y=dept_df['department'],
            x=dept_df['profit'],
            name='Profit',
            orientation='h',
            marker_color='#10b981'
        )
    ])

    fig.update_layout(
        barmode='group',
        hovermode="y unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        paper_bgcolor='white',
        plot_bgcolor='white',
        height=400,
        xaxis_title="Amount ($)",
        yaxis_title=""
    )

    fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')

    st.plotly_chart(fig, width='stretch')


def create_margin_comparison(df: pd.DataFrame) -> None:
    """Create margin comparison by department"""
    st.markdown('<p class="section-header">Margin Analysis by Department</p>', unsafe_allow_html=True)

    # Calculate margin by department
    margin_df = df.groupby('department').agg({
        'gross_margin': 'mean',
        'payroll_ratio': 'mean',
        'operating_cost_ratio': 'mean'
    }).reset_index()

    margin_df = margin_df.sort_values('gross_margin', ascending=False)

    # Create bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=margin_df['department'],
        x=margin_df['gross_margin'],
        name='Gross Margin',
        orientation='h',
        marker_color='#667eea',
        text=[f'{x:.1%}' for x in margin_df['gross_margin']],
        textposition='outside'
    ))

    fig.update_layout(
        hovermode="y unified",
        paper_bgcolor='white',
        plot_bgcolor='white',
        height=400,
        xaxis_title="Margin (%)",
        yaxis_title="",
        xaxis_tickformat='.0%'
    )

    fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)', range=[0, max(margin_df['gross_margin'])*1.3])

    st.plotly_chart(fig, width='stretch')


def create_mom_variance_table(df: pd.DataFrame) -> None:
    """Create month-over-month variance table"""
    st.markdown('<p class="section-header">Month-over-Month Variance</p>', unsafe_allow_html=True)

    # Create date column if not present
    if 'date' in df.columns:
        df['month'] = pd.to_datetime(df['date']).dt.to_period('M')

        # Aggregate by month
        mom_df = df.groupby('month').agg({
            'revenue': 'sum',
            'profit': 'sum',
            'revenue_mom_change': 'mean',
            'profit_mom_change': 'mean'
        }).reset_index()

        mom_df['month'] = mom_df['month'].astype(str)
        mom_df = mom_df.sort_values('month', ascending=False)

        # Format columns
        mom_df['revenue'] = mom_df['revenue'].apply(format_currency)
        mom_df['profit'] = mom_df['profit'].apply(format_currency)
        mom_df['revenue_mom_change'] = mom_df['revenue_mom_change'].apply(
            lambda x: f"⬆️ {x*100:.1f}%" if pd.notna(x) and x > 0 else (f"⬇️ {abs(x)*100:.1f}%" if pd.notna(x) else "-")
        )
        mom_df['profit_mom_change'] = mom_df['profit_mom_change'].apply(
            lambda x: f"⬆️ {x*100:.1f}%" if pd.notna(x) and x > 0 else (f"⬇️ {abs(x)*100:.1f}%" if pd.notna(x) else "-")
        )

        mom_df.columns = ['Month', 'Revenue', 'Profit', 'Revenue Δ', 'Profit Δ']

        st.dataframe(
            mom_df,
            width='stretch',
            hide_index=True,
            column_config={
                'Revenue': st.column_config.TextColumn(width='medium'),
                'Profit': st.column_config.TextColumn(width='medium'),
                'Revenue Δ': st.column_config.TextColumn(width='small'),
                'Profit Δ': st.column_config.TextColumn(width='small'),
            }
        )


def create_department_detail_table(df: pd.DataFrame) -> None:
    """Create detailed department summary table"""
    st.markdown('<p class="section-header">Department Performance Details</p>', unsafe_allow_html=True)

    # Aggregate by department
    dept_detail = df.groupby('department').agg({
        'revenue': ['sum', 'mean'],
        'profit': ['sum', 'mean'],
        'gross_margin': 'mean',
        'payroll_ratio': 'mean'
    }).reset_index()

    # Flatten column names
    dept_detail.columns = ['Department', 'Total Revenue', 'Avg Revenue', 'Total Profit',
                          'Avg Profit', 'Avg Margin', 'Avg Payroll Ratio']

    # Format columns
    dept_detail['Total Revenue'] = dept_detail['Total Revenue'].apply(format_currency)
    dept_detail['Avg Revenue'] = dept_detail['Avg Revenue'].apply(format_currency)
    dept_detail['Total Profit'] = dept_detail['Total Profit'].apply(format_currency)
    dept_detail['Avg Profit'] = dept_detail['Avg Profit'].apply(format_currency)
    dept_detail['Avg Margin'] = dept_detail['Avg Margin'].apply(format_percentage)
    dept_detail['Avg Payroll Ratio'] = dept_detail['Avg Payroll Ratio'].apply(format_percentage)

    st.dataframe(
        dept_detail,
        width='stretch',
        hide_index=True
    )


def main():
    """Main application"""

    # Header
    st.title("📊 Financial Performance Dashboard")
    st.markdown("### Business Intelligence Analytics")
    st.markdown("---")

import os

# Determine base path for local vs deployment
base_path = os.path.dirname(os.path.abspath(__file__))
default_file = os.path.join(base_path, "bi_dataset.csv")

# File path input
file_path = st.sidebar.text_input("Data File Path", value=default_file)

    # Sidebar filters
    st.sidebar.markdown("---")
    st.sidebar.header("Filters")

    try:
        # Load data
        df = load_data(file_path)
        df = clean_data(df)

        # Department filter
        departments = ["All"] + sorted(df['department'].dropna().unique().tolist())
        selected_dept = st.sidebar.selectbox("Department", departments)

        # Date range filter
        if 'date' in df.columns:
            date_min = df['date'].min()
            date_max = df['date'].max()
            date_range = st.sidebar.date_input(
                "Date Range",
                value=(date_min, date_max),
                help="Select date range for analysis"
            )

        # Apply filters
        filtered_df = df.copy()
        if selected_dept != "All":
            filtered_df = filtered_df[filtered_df['department'] == selected_dept]

        if 'date' in df.columns and len(date_range) == 2:
            filtered_df = filtered_df[
                (filtered_df['date'] >= pd.to_datetime(date_range[0])) &
                (filtered_df['date'] <= pd.to_datetime(date_range[1]))
            ]

        # Display metrics
        create_kpi_cards(filtered_df)
        st.markdown("---")

        # Charts
        if 'date' in filtered_df.columns:
            create_trend_chart(filtered_df)
            st.markdown("---")

        create_department_chart(filtered_df)
        st.markdown("---")

        create_margin_comparison(filtered_df)
        st.markdown("---")

        # Tables
        create_mom_variance_table(filtered_df)
        st.markdown("---")

        create_department_detail_table(filtered_df)

        # Footer
        st.markdown("---")
        st.markdown(
            "<p style='text-align: center; color: #888;'>"
            "Financial Performance Dashboard | Business Intelligence"
            "</p>",
            unsafe_allow_html=True
        )

    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        st.info("Please ensure the CSV file exists and the path is correct.")
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Please check your data format matches the expected schema.")


if __name__ == "__main__":
    main()
