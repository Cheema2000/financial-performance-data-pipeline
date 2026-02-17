# Financial Performance Data Pipeline

An end-to-end data engineering and business intelligence project that processes financial data, calculates KPIs, and presents insights through an interactive dashboard.

## Project Overview

This project demonstrates skills in:
- **Data Engineering**: ETL pipelines with Python and Pandas
- **Data Validation**: Cleaning and validating financial data
- **Financial Analysis**: KPI calculations and variance analysis
- **Business Intelligence**: Interactive dashboards with Streamlit & Plotly
- **Database Management**: SQL schema design and SQLite operations

## Project Structure

```
financial-performance-data-pipeline/
├── Data/
│   ├── raw/
│   │   └── financials.csv           # Raw financial data
│   └── processed/
│       ├── financials_clean.csv     # Cleaned & validated data
│       ├── financials_kpi.csv       # Data with calculated KPIs
│       └── department_summary.csv   # Department aggregations
├── src/
│   ├── ingest_data.py               # Load raw data
│   ├── clean_validate.py            # Clean & validate data
│   ├── financial_metrics.py        # Calculate financial KPIs
│   ├── department_summary.py       # Department-level aggregation
│   └── load_to_sql.py              # Load data to SQLite
├── sql/
│   └── schema.sql                  # Database schema
├── dashboard.py                     # Streamlit BI Dashboard
├── bi_dataset.csv                   # BI dashboard dataset
├── financials.db                   # SQLite database
└── README.md
```

## Data Pipeline

### 1. Data Ingestion (`src/ingest_data.py`)
- Loads raw financial data from CSV
- Provides initial data overview

### 2. Data Cleaning & Validation (`src/clean_validate.py`)
- Converts date columns to datetime
- Drops missing critical values (date, department)
- Validates numeric fields (no negative values)
- Calculates profit metric
- Outputs cleaned dataset

### 3. Financial Metrics (`src/financial_metrics.py`)
Calculates key performance indicators:
- **Gross Margin**: Profit / Revenue
- **Payroll Ratio**: Payroll Cost / Revenue
- **Operating Cost Ratio**: Operating Cost / Revenue
- **Month-over-Month Variance**: Revenue & Profit changes

### 4. Department Summary (`src/department_summary.py`)
Aggregates metrics by department:
- Total Revenue & Profit
- Average Gross Margin
- Average Payroll Ratio

### 5. Database Loading (`src/load_to_sql.py`)
- Loads processed data to SQLite database
- Creates `financials` and `department_summary` tables

## Interactive Dashboard

The **Streamlit Dashboard** (`dashboard.py`) provides:

### Features
- **Executive KPI Cards**: Total Revenue, Profit, Average Margin, Department Count
- **Trend Analysis**: Revenue & Profit over time (line chart)
- **Department Comparison**: Bar chart showing Revenue & Profit by department
- **Margin Analysis**: Gross margin comparison across departments
- **Month-over-Month Variance**: Variance table with delta indicators
- **Department Details**: Comprehensive performance table
- **Filters**: Department and date range filters
- **Professional UI**: Custom styling, proper formatting

### Visualizations
- Dual-axis line chart (Revenue vs Profit)
- Horizontal bar charts for department comparison
- Sortable data tables
- Interactive hover tooltips

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming language |
| Pandas | Data manipulation & analysis |
| Plotly | Interactive data visualization |
| Streamlit | Web dashboard framework |
| SQLite | Lightweight database |
| Git | Version control |

## How to Run

### 1. Run the Pipeline
```bash
# Data ingestion
python src/ingest_data.py

# Clean and validate
python src/clean_validate.py

# Calculate KPIs
python src/financial_metrics.py

# Department summary
python src/department_summary.py

# Load to database
python src/load_to_sql.py
```

### 2. Run the Dashboard
```bash
streamlit run dashboard.py
```

The dashboard will open at `http://localhost:8501`

### 3. View the BI Dashboard
The dashboard loads from `bi_dataset.csv` by default. You can:
- Filter by department
- Filter by date range
- Explore interactive charts
- View detailed tables

## Sample Data

The project includes sample financial data with:
- **4 Departments**: Engineering, Marketing, Sales, Operations
- **12 Months**: Monthly data from 2024
- **Metrics**: Revenue, Operating Costs, Payroll Costs, Profit

## Skills Demonstrated

| Skill | Implementation |
|-------|---------------|
| Data Cleaning | Handling nulls, type conversion, data validation |
| ETL Pipeline | Sequential data processing workflow |
| Financial Analysis | Margin, ratios, variance calculations |
| Database Design | SQL schema, table creation, data loading |
| Visualization | Plotly charts, interactive dashboards |
| Python | Pandas, functions, error handling |

## Live Dashboard

To deploy publicly:
1. Push to GitHub
2. Connect to Streamlit Community Cloud
3. Select `dashboard.py` as the main file

---

*Built for portfolio demonstration | Data Engineering & Business Intelligence*
