CREATE TABLE IF NOT EXISTS financials (
    date TEXT,
    department TEXT,
    revenue REAL,
    operating_cost REAL,
    payroll_cost REAL,
    profit REAL,
    gross_margin REAL,
    payroll_ratio REAL,
    operating_cost_ratio REAL,
    revenue_mom_change REAL,
    profit_mom_change REAL
);

CREATE TABLE IF NOT EXISTS department_summary (
    department TEXT,
    total_revenue REAL,
    total_profit REAL,
    avg_margin REAL,
    avg_payroll_ratio REAL
);
