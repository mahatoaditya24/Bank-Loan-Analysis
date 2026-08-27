"""
Bank Loan Portfolio & Credit Risk Analytics Platform.
Engineered with Streamlit, Plotly & Modern Glassmorphic Web Architecture.
Features Executive Financial KPIs, Good vs Bad Loan Credit Matrices, Geographic Heatmaps,
Macro Stress Testing Engine, and Real-Time Borrower Underwriting & EMI Amortization Simulator.
"""

import os
import io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# -----------------------------------------------------------------------------
# 1. Page Configuration & Ultra-Premium Styling System
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Apex Bank | Loan Portfolio & Credit Risk Analytics",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Banking CSS Design System
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">

<style>
    /* Global Typography & Palette */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Sleek Background & Main Container */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #0b0f19 0%, #030712 90%);
        color: #f1f5f9;
    }

    /* Glassmorphic Metric Cards */
    .kpi-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(51, 65, 85, 0.6);
        border-radius: 16px;
        padding: 20px 22px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.4);
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        border-color: rgba(56, 189, 248, 0.7);
        box-shadow: 0 20px 30px -10px rgba(56, 189, 248, 0.25);
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
    }
    .kpi-card-emerald::before {
        background: linear-gradient(90deg, #10b981, #34d399, #6ee7b7);
    }
    .kpi-card-rose::before {
        background: linear-gradient(90deg, #f43f5e, #fb7185, #fda4af);
    }
    .kpi-card-amber::before {
        background: linear-gradient(90deg, #f59e0b, #fbbf24, #fde68a);
    }

    .kpi-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .kpi-value {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #ffffff;
        margin: 6px 0 4px 0;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .kpi-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 0.82rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 9999px;
    }
    .badge-green {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-red {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .badge-blue {
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    .badge-amber {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    /* Hero Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
        border: 1px solid rgba(51, 65, 85, 0.8);
        border-radius: 20px;
        padding: 24px 30px;
        margin-bottom: 24px;
        backdrop-filter: blur(12px);
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    .hero-title {
        font-size: 1.75rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff, #cbd5e1, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 4px;
    }

    /* Tab navigation polish */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.5);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(51, 65, 85, 0.5);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 18px;
        color: #94a3b8;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: #1e293b !important;
        color: #38bdf8 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }

    /* Subheader Polish */
    h3, h4, h5 {
        color: #f8fafc !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em;
    }

    /* Clean Streamlit DataFrames */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. Data Ingestion & Caching Layer
# -----------------------------------------------------------------------------
@st.cache_data(ttl=3600, show_spinner=False)
def load_bank_loan_data():
    """Load loan dataset from compressed Parquet or CSV with high-speed indexing."""
    parquet_path = os.path.join(os.path.dirname(__file__), "data", "bank_loan_data.parquet")
    csv_path = os.path.join(os.path.dirname(__file__), "data", "bank_loan_data.csv.gz")

    if os.path.exists(parquet_path):
        df = pd.read_parquet(parquet_path)
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path, compression="gzip")
    else:
        # Synthetic generator fallback
        np.random.seed(42)
        n = 15000
        states = ["CA", "NY", "TX", "FL", "IL", "PA", "OH", "GA", "NC", "VA", "WA", "AZ", "CO", "MA", "NJ"]
        grades = ["A", "B", "C", "D", "E", "F", "G"]
        purposes = ["debt_consolidation", "credit_card", "home_improvement", "major_purchase", "small_business", "car", "medical"]
        emp_lens = ["< 1 year", "1 year", "2 years", "3 years", "5 years", "10+ years"]
        home_owns = ["RENT", "MORTGAGE", "OWN"]

        dates = pd.date_range(start="2021-01-01", end="2021-12-31", periods=n)
        amounts = np.random.normal(11500, 7500, n).clip(1000, 35000).astype(int)
        int_rates = np.random.uniform(0.06, 0.24, n)
        dtis = np.random.uniform(0.05, 0.32, n)
        annual_incs = np.random.normal(71000, 36000, n).clip(20000, 250000)

        statuses = np.random.choice(["Fully Paid", "Charged Off", "Current"], size=n, p=[0.83, 0.14, 0.03])
        payments = amounts * (1 + int_rates * 1.5)
        payments[statuses == "Charged Off"] = payments[statuses == "Charged Off"] * np.random.uniform(0.2, 0.6, sum(statuses == "Charged Off"))

        df = pd.DataFrame({
            "id": range(100000, 100000 + n),
            "address_state": np.random.choice(states, n),
            "grade": np.random.choice(grades, n, p=[0.26, 0.30, 0.20, 0.12, 0.07, 0.03, 0.02]),
            "sub_grade": [f"{g}{np.random.randint(1, 6)}" for g in np.random.choice(grades, n)],
            "purpose": np.random.choice(purposes, n, p=[0.48, 0.24, 0.10, 0.06, 0.05, 0.04, 0.03]),
            "term": np.random.choice([" 36 months", " 60 months"], n, p=[0.74, 0.26]),
            "emp_length": np.random.choice(emp_lens, n),
            "home_ownership": np.random.choice(home_owns, n, p=[0.48, 0.44, 0.08]),
            "issue_date": dates,
            "loan_status": statuses,
            "annual_income": annual_incs,
            "dti": dtis,
            "int_rate": int_rates,
            "loan_amount": amounts,
            "total_payment": payments.round(2)
        })

    df["issue_date"] = pd.to_datetime(df["issue_date"])
    df["month_number"] = df["issue_date"].dt.month
    df["month_name"] = df["issue_date"].dt.strftime("%b")
    df["year"] = df["issue_date"].dt.year
    df["is_good_loan"] = df["loan_status"].apply(lambda s: 1 if s in ["Fully Paid", "Current"] else 0)
    df["is_bad_loan"] = df["loan_status"].apply(lambda s: 1 if s == "Charged Off" else 0)
    return df


raw_df = load_bank_loan_data()

# -----------------------------------------------------------------------------
# 3. Interactive Sidebar & Dynamic Filters
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
        <div style="background:linear-gradient(135deg, #0284c7, #38bdf8); padding:10px; border-radius:12px; box-shadow:0 4px 12px rgba(56,189,248,0.3);">
            🏛️
        </div>
        <div>
            <h3 style="margin:0; font-size:1.15rem; font-weight:800; color:#fff;">Apex Credit AI</h3>
            <p style="margin:0; font-size:0.75rem; color:#94a3b8;">Banking Portfolio Intelligence</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🎛️ Portfolio Slicers")

    # Grade Multiselect
    all_grades = sorted(raw_df["grade"].unique())
    selected_grades = st.multiselect("Credit Grade Band", options=all_grades, default=all_grades)

    # Loan Status Multiselect
    all_statuses = sorted(raw_df["loan_status"].unique())
    selected_statuses = st.multiselect("Loan Repayment Status", options=all_statuses, default=all_statuses)

    # Term Multiselect
    all_terms = sorted(raw_df["term"].unique())
    selected_terms = st.multiselect("Loan Term Duration", options=all_terms, default=all_terms)

    # Loan Purpose Multiselect
    all_purposes = sorted(raw_df["purpose"].unique())
    selected_purposes = st.multiselect("Borrower Purpose", options=all_purposes, default=all_purposes)

    # Interactive Range Sliders
    st.markdown("##### 💵 Principal & Yield Filter")
    min_loan, max_loan = int(raw_df["loan_amount"].min()), int(raw_df["loan_amount"].max())
    loan_range = st.slider("Loan Amount ($)", min_value=min_loan, max_value=max_loan, value=(min_loan, max_loan), step=1000)

    st.markdown("---")
    # Quick Reset Button
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.experimental_rerun()

    st.caption("🚀 **Live Stack:** `Streamlit` | `Plotly Express` | `T-SQL Data Marts` | `Power BI` | `Tableau`")

# Apply Slicers
df = raw_df[
    (raw_df["grade"].isin(selected_grades)) &
    (raw_df["loan_status"].isin(selected_statuses)) &
    (raw_df["term"].isin(selected_terms)) &
    (raw_df["purpose"].isin(selected_purposes)) &
    (raw_df["loan_amount"] >= loan_range[0]) &
    (raw_df["loan_amount"] <= loan_range[1])
]

# -----------------------------------------------------------------------------
# 4. Hero Header Banner
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div>
        <h1 class="hero-title">🏛️ Bank Loan Portfolio & Credit Risk Analytics</h1>
        <div class="hero-subtitle">
            Enterprise analytics platform monitoring <b>$435M+</b> capital disbursement, Good vs. Bad loan recovery rates, and credit risk exposures.
        </div>
    </div>
    <div style="display:flex; gap:10px;">
        <span style="background:rgba(56, 189, 248, 0.1); color:#38bdf8; border:1px solid rgba(56, 189, 248, 0.3); padding:6px 14px; border-radius:30px; font-size:0.8rem; font-weight:600;">🟢 Live Analytics</span>
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 5. Executive Financial KPI Cards
# -----------------------------------------------------------------------------
total_apps = len(df)
total_funded = df["loan_amount"].sum()
total_received = df["total_payment"].sum()
avg_int_rate = (df["int_rate"].mean() * 100) if total_apps > 0 else 0
avg_dti = (df["dti"].mean() * 100) if total_apps > 0 else 0
recovery_ratio = (total_received / total_funded * 100) if total_funded > 0 else 0

# Month-to-Date (MTD) Dec 2021 vs Prior-MTD (PMTD) Nov 2021
mtd_df = df[(df["month_number"] == 12) & (df["year"] == 2021)]
pmtd_df = df[(df["month_number"] == 11) & (df["year"] == 2021)]

mtd_apps = len(mtd_df)
pmtd_apps = len(pmtd_df) if len(pmtd_df) > 0 else 1
mom_apps_delta = ((mtd_apps - pmtd_apps) / pmtd_apps) * 100

mtd_funded = mtd_df["loan_amount"].sum()
pmtd_funded = pmtd_df["loan_amount"].sum() if pmtd_df["loan_amount"].sum() > 0 else 1
mom_funded_delta = ((mtd_funded - pmtd_funded) / pmtd_funded) * 100

mtd_received = mtd_df["total_payment"].sum()
pmtd_received = pmtd_df["total_payment"].sum() if pmtd_df["total_payment"].sum() > 0 else 1
mom_received_delta = ((mtd_received - pmtd_received) / pmtd_received) * 100

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">📋 Total Applications</div>
        <div class="kpi-value">{total_apps:,}</div>
        <span class="kpi-badge badge-green">▲ MTD MoM: +{mom_apps_delta:.1f}%</span>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card kpi-card-emerald">
        <div class="kpi-label">💰 Funded Principal</div>
        <div class="kpi-value">${total_funded / 1e6:.1f}M</div>
        <span class="kpi-badge badge-blue">▲ MTD MoM: +{mom_funded_delta:.1f}%</span>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card kpi-card-emerald">
        <div class="kpi-label">💵 Total Cash Collected</div>
        <div class="kpi-value">${total_received / 1e6:.1f}M</div>
        <span class="kpi-badge badge-green">▲ Recovery: {recovery_ratio:.1f}%</span>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card kpi-card-amber">
        <div class="kpi-label">📈 Weighted Avg Rate</div>
        <div class="kpi-value">{avg_int_rate:.2f}%</div>
        <span class="kpi-badge badge-amber">★ Portfolio Yield</span>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="kpi-card kpi-card-rose">
        <div class="kpi-label">🛡️ Average DTI Ratio</div>
        <div class="kpi-value">{avg_dti:.2f}%</div>
        <span class="kpi-badge badge-blue">● Borrower Leverage</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 6. Multi-Tab Navigation Hub
# -----------------------------------------------------------------------------
t_summary, t_credit_risk, t_geo, t_grades, t_stress, t_sim = st.tabs([
    "📊 Executive Summary",
    "🛡️ Good vs. Bad Loans",
    "🗺️ Geographic Heatmap",
    "⭐ Credit Grade Matrices",
    "⚡ Macroeconomic Stress Tester",
    "🧮 Loan Repayment & Risk Simulator"
])


# =============================================================================
# TAB 1: EXECUTIVE SUMMARY & CASH FLOW
# =============================================================================
with t_summary:
    col_s1, col_s2 = st.columns([6, 4])

    with col_s1:
        st.subheader("📈 Monthly Loan Disbursement vs. Cash Collection Trend")
        month_agg = df.groupby(["month_number", "month_name"]).agg(
            funded=("loan_amount", "sum"),
            received=("total_payment", "sum"),
            apps=("id", "count")
        ).reset_index().sort_values("month_number")

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=month_agg["month_name"],
            y=month_agg["funded"],
            name="Funded Capital ($)",
            marker=dict(color="#38bdf8", opacity=0.85, line=dict(color="#0284c7", width=1.5)),
            hovertemplate="<b>%{x}</b><br>Funded: $%{y:,.0f}<extra></extra>"
        ))
        fig_trend.add_trace(go.Bar(
            x=month_agg["month_name"],
            y=month_agg["received"],
            name="Collected Cash ($)",
            marker=dict(color="#10b981", opacity=0.85, line=dict(color="#059669", width=1.5)),
            hovertemplate="<b>%{x}</b><br>Received: $%{y:,.0f}<extra></extra>"
        ))
        fig_trend.add_trace(go.Scatter(
            x=month_agg["month_name"],
            y=month_agg["apps"] * (month_agg["funded"].max() / month_agg["apps"].max() * 0.7),
            name="Loan Application Demand",
            mode="lines+markers",
            line=dict(color="#f59e0b", width=3),
            marker=dict(size=7, color="#fbbf24"),
            yaxis="y",
            hovertemplate="<b>%{x} Demand</b><extra></extra>"
        ))

        fig_trend.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.4)",
            height=370,
            barmode="group",
            hovermode="x unified",
            legend=dict(orientation="h", y=1.12, x=0.01),
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis=dict(gridcolor="#1e293b"),
            yaxis=dict(gridcolor="#1e293b", title="Capital Amount ($)")
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_s2:
        st.subheader("🎯 Portfolio Concentration by Loan Purpose")
        purpose_agg = df.groupby("purpose")["loan_amount"].sum().reset_index().sort_values("loan_amount", ascending=False).head(7)
        fig_pie = px.pie(
            purpose_agg,
            names="purpose",
            values="loan_amount",
            hole=0.55,
            color_discrete_sequence=["#38bdf8", "#818cf8", "#34d399", "#f59e0b", "#fb7185", "#c084fc", "#94a3b8"]
        )
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(line=dict(color='#0f172a', width=2))
        )
        fig_pie.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=370,
            showlegend=False,
            margin=dict(l=10, r=10, t=20, b=20),
            annotations=[dict(text=f"<b>${total_funded / 1e6:.1f}M</b><br>Total", x=0.5, y=0.5, font_size=15, showarrow=False, font_color="#ffffff")]
        )
        st.plotly_chart(fig_pie, use_container_width=True)


# =============================================================================
# TAB 2: GOOD VS BAD LOAN RISK MATRIX
# =============================================================================
with t_credit_risk:
    st.subheader("🛡️ Portfolio Credit Quality: Performing vs. Charge-Off Default Severity")

    good_loans = df[df["is_good_loan"] == 1]
    bad_loans = df[df["is_bad_loan"] == 1]

    g_apps = len(good_loans)
    b_apps = len(bad_loans)
    g_pct = (g_apps / total_apps * 100) if total_apps > 0 else 0
    b_pct = (b_apps / total_apps * 100) if total_apps > 0 else 0

    g_funded = good_loans["loan_amount"].sum()
    g_received = good_loans["total_payment"].sum()
    b_funded = bad_loans["loan_amount"].sum()
    b_received = bad_loans["total_payment"].sum()
    b_loss = max(0, b_funded - b_received)
    g_profit = g_received - g_funded

    col_gb1, col_gb2 = st.columns(2)

    with col_gb1:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg, rgba(6, 78, 59, 0.7) 0%, rgba(2, 44, 34, 0.8) 100%); border:1px solid #10b981; border-radius:16px; padding:22px; box-shadow:0 8px 25px rgba(16,185,129,0.15);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <h4 style="color:#34d399; margin:0; font-size:1.15rem;">🟢 Performing Portfolio (Good Loans)</h4>
                <span class="kpi-badge badge-green">{g_pct:.1f}% Portfolio Share</span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                <div>
                    <div style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase;">Volume Count</div>
                    <div style="font-size:1.3rem; font-weight:700; color:#fff;">{g_apps:,} Loans</div>
                </div>
                <div>
                    <div style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase;">Funded Capital</div>
                    <div style="font-size:1.3rem; font-weight:700; color:#fff;">${g_funded / 1e6:.1f}M</div>
                </div>
                <div>
                    <div style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase;">Cash Collected</div>
                    <div style="font-size:1.3rem; font-weight:700; color:#fff;">${g_received / 1e6:.1f}M</div>
                </div>
                <div>
                    <div style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase;">Net Interest Margin</div>
                    <div style="font-size:1.3rem; font-weight:700; color:#34d399;">+${g_profit / 1e6:.1f}M (+{(g_profit/g_funded*100) if g_funded>0 else 0:.1f}%)</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_gb2:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg, rgba(69, 10, 10, 0.7) 0%, rgba(30, 7, 7, 0.8) 100%); border:1px solid #ef4444; border-radius:16px; padding:22px; box-shadow:0 8px 25px rgba(239,68,68,0.15);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <h4 style="color:#f87171; margin:0; font-size:1.15rem;">🔴 Non-Performing Portfolio (Bad Loans / Defaults)</h4>
                <span class="kpi-badge badge-red">{b_pct:.1f}% Default Rate</span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                <div>
                    <div style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase;">Defaulted Volume</div>
                    <div style="font-size:1.3rem; font-weight:700; color:#fff;">{b_apps:,} Loans</div>
                </div>
                <div>
                    <div style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase;">Disbursed at Risk</div>
                    <div style="font-size:1.3rem; font-weight:700; color:#fff;">${b_funded / 1e6:.1f}M</div>
                </div>
                <div>
                    <div style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase;">Recovered Prior Loss</div>
                    <div style="font-size:1.3rem; font-weight:700; color:#fff;">${b_received / 1e6:.1f}M</div>
                </div>
                <div>
                    <div style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase;">Net Charge-Off Loss</div>
                    <div style="font-size:1.3rem; font-weight:700; color:#f87171;">-${b_loss / 1e6:.1f}M (-{(b_loss/b_funded*100) if b_funded>0 else 0:.1f}%)</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_r1, col_r2 = st.columns([5, 5])
    with col_r1:
        st.write("##### 📊 Status Breakdown & Loss Severity Waterfall")
        status_tbl = df.groupby("loan_status").agg(
            Applications=("id", "count"),
            Funded=("loan_amount", "sum"),
            Received=("total_payment", "sum"),
            Avg_Rate=("int_rate", lambda x: round(x.mean() * 100, 2)),
            Avg_DTI=("dti", lambda x: round(x.mean() * 100, 2))
        ).reset_index()
        status_tbl["Funded ($M)"] = (status_tbl["Funded"] / 1e6).round(2)
        status_tbl["Received ($M)"] = (status_tbl["Received"] / 1e6).round(2)
        status_tbl["Recovery Rate (%)"] = (status_tbl["Received"] / status_tbl["Funded"] * 100).round(1)

        st.dataframe(
            status_tbl[["loan_status", "Applications", "Funded ($M)", "Received ($M)", "Recovery Rate (%)", "Avg_Rate", "Avg_DTI"]],
            use_container_width=True
        )

    with col_r2:
        st.write("##### 💵 Net Capital Flow Comparison ($ Millions)")
        fig_bar_comp = go.Figure()
        fig_bar_comp.add_trace(go.Bar(
            name="Funded Capital",
            x=["Good Loans", "Bad Loans"],
            y=[g_funded / 1e6, b_funded / 1e6],
            marker_color="#38bdf8"
        ))
        fig_bar_comp.add_trace(go.Bar(
            name="Recovered Cash",
            x=["Good Loans", "Bad Loans"],
            y=[g_received / 1e6, b_received / 1e6],
            marker_color="#10b981"
        ))
        fig_bar_comp.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.4)",
            height=280,
            barmode="group",
            margin=dict(l=10, r=10, t=20, b=20)
        )
        st.plotly_chart(fig_bar_comp, use_container_width=True)


# =============================================================================
# TAB 3: GEOGRAPHIC HEATMAP & REGIONAL EXPOSURE
# =============================================================================
with t_geo:
    st.subheader("🗺️ US State-Level Credit Exposure & Default Risk Map")

    state_df = df.groupby("address_state").agg(
        total_apps=("id", "count"),
        funded=("loan_amount", "sum"),
        received=("total_payment", "sum"),
        defaults=("is_bad_loan", "sum"),
        avg_dti=("dti", "mean")
    ).reset_index()
    state_df["default_rate"] = (state_df["defaults"] / state_df["total_apps"] * 100).round(2)
    state_df["avg_dti"] = (state_df["avg_dti"] * 100).round(2)

    col_map1, col_map2 = st.columns([7, 3])

    with col_map1:
        map_metric = st.selectbox("Select Map Color Metric:", ["Total Funded Capital ($)", "Default Rate (%)", "Total Applications"])

        if map_metric == "Total Funded Capital ($)":
            z_col = "funded"
            colorscale = "Blues"
        elif map_metric == "Default Rate (%)":
            z_col = "default_rate"
            colorscale = "Reds"
        else:
            z_col = "total_apps"
            colorscale = "Viridis"

        fig_map = px.choropleth(
            state_df,
            locations="address_state",
            locationmode="USA-states",
            color=z_col,
            scope="usa",
            hover_name="address_state",
            hover_data={"funded": ":$,.0f", "total_apps": ":,", "default_rate": ":.2f%", "avg_dti": ":.2f%"},
            color_continuous_scale=colorscale
        )
        fig_map.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=430,
            margin=dict(l=0, r=0, t=10, b=0),
            geo=dict(bgcolor="rgba(0,0,0,0)", lakecolor="#0f172a")
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_map2:
        st.write("##### 🏆 Top 10 State Markets")
        top_states = state_df.sort_values("funded", ascending=False).head(10)[["address_state", "total_apps", "funded", "default_rate"]]
        top_states.columns = ["State", "Apps", "Funded ($)", "Default %"]
        top_states["Funded ($)"] = top_states["Funded ($)"].apply(lambda x: f"${x / 1e6:.1f}M")
        top_states["Default %"] = top_states["Default %"].apply(lambda x: f"{x:.1f}%")
        st.dataframe(top_states, use_container_width=True, height=380)


# =============================================================================
# TAB 4: CREDIT GRADE MATRICES
# =============================================================================
with t_grades:
    st.subheader("⭐ Credit Grade & Sub-Grade Risk Pricing Progression")

    col_gr1, col_gr2 = st.columns(2)

    with col_gr1:
        st.write("##### 📈 Grade A to G Default Curve vs Interest Yield")
        grade_agg = df.groupby("grade").agg(
            apps=("id", "count"),
            funded=("loan_amount", "sum"),
            avg_rate=("int_rate", lambda x: x.mean() * 100),
            defaults=("is_bad_loan", "sum")
        ).reset_index()
        grade_agg["default_rate"] = (grade_agg["defaults"] / grade_agg["apps"] * 100).round(2)

        fig_gr = make_subplots(specs=[[{"secondary_y": True}]])
        fig_gr.add_trace(
            go.Bar(x=grade_agg["grade"], y=grade_agg["avg_rate"], name="Avg Interest Rate (%)", marker_color="#38bdf8", opacity=0.85),
            secondary_y=False
        )
        fig_gr.add_trace(
            go.Scatter(x=grade_agg["grade"], y=grade_agg["default_rate"], name="Default Rate (%)", mode="lines+markers", line=dict(color="#f43f5e", width=3), marker=dict(size=8, color="#fb7185")),
            secondary_y=True
        )
        fig_gr.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.4)",
            height=340,
            hovermode="x unified",
            legend=dict(orientation="h", y=1.15),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        fig_gr.update_yaxes(title_text="Interest Rate (%)", secondary_y=False, gridcolor="#1e293b")
        fig_gr.update_yaxes(title_text="Default Rate (%)", secondary_y=True)
        st.plotly_chart(fig_gr, use_container_width=True)

    with col_gr2:
        st.write("##### 🏢 Loan Term Distribution (36 vs. 60 Months)")
        term_agg = df.groupby("term").agg(
            funded=("loan_amount", "sum"),
            received=("total_payment", "sum"),
            defaults=("is_bad_loan", "sum"),
            apps=("id", "count")
        ).reset_index()
        term_agg["default_rate"] = (term_agg["defaults"] / term_agg["apps"] * 100).round(1)

        fig_term = go.Figure()
        fig_term.add_trace(go.Bar(x=term_agg["term"], y=term_agg["funded"] / 1e6, name="Funded ($M)", marker_color="#38bdf8"))
        fig_term.add_trace(go.Bar(x=term_agg["term"], y=term_agg["received"] / 1e6, name="Received ($M)", marker_color="#10b981"))
        fig_term.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.4)",
            height=340,
            barmode="group",
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_term, use_container_width=True)


# =============================================================================
# TAB 5: MACROECONOMIC STRESS TESTER
# =============================================================================
with t_stress:
    st.subheader("⚡ Macroeconomic Portfolio Stress Testing Engine")
    st.write("Simulate adverse economic shocks (interest rate hikes, inflation, unemployment spikes) to estimate portfolio default risk surge and net capital at risk.")

    col_st1, col_st2 = st.columns([4, 6])

    with col_st1:
        st.markdown("##### 🎛️ Shock Parameters")
        rate_hike_bps = st.slider("Interest Rate Hike (Basis Points)", min_value=0, max_value=500, value=150, step=25)
        unemp_shock = st.slider("Unemployment Surge Factor", min_value=1.0, max_value=2.5, value=1.35, step=0.05)
        dti_degradation = st.slider("Borrower Debt Service Strain (+% DTI)", min_value=0.0, max_value=10.0, value=3.5, step=0.5)

        # Stress calculation model
        baseline_default_rate = b_pct
        stressed_default_rate = min(45.0, baseline_default_rate * unemp_shock + (rate_hike_bps / 100.0) * 1.8 + (dti_degradation * 0.6))
        stressed_default_apps = int(total_apps * (stressed_default_rate / 100.0))
        incremental_defaults = stressed_default_apps - b_apps

        avg_loss_per_default = (b_loss / b_apps) if b_apps > 0 else 5500
        incremental_loss_exposure = max(0, incremental_defaults * avg_loss_per_default)

    with col_st2:
        st.markdown("##### 🔮 Stress Test Impact Analysis")
        sc1, sc2 = st.columns(2)
        with sc1:
            st.metric("Baseline Default Rate", f"{baseline_default_rate:.2f}%")
            st.metric("Projected Stressed Defaults", f"{stressed_default_apps:,} Loans", delta=f"+{incremental_defaults:,} Defaults", delta_color="inverse")
        with sc2:
            st.metric("Stressed Default Rate", f"{stressed_default_rate:.2f}%", delta=f"+{(stressed_default_rate - baseline_default_rate):.2f}% Shock", delta_color="inverse")
            st.metric("Incremental Loss Exposure", f"${incremental_loss_exposure / 1e6:.2f}M", delta=f"+${incremental_loss_exposure / 1e6:.2f}M at Risk", delta_color="inverse")

        # Gauge Chart for Portfolio Health
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=stressed_default_rate,
            title={'text': "Stressed Default Risk Level (%)", 'font': {'color': "#ffffff", 'size': 16}},
            gauge={
                'axis': {'range': [0, 45], 'tickwidth': 1, 'tickcolor': "#ffffff"},
                'bar': {'color': "#f43f5e" if stressed_default_rate > 20 else "#f59e0b"},
                'steps': [
                    {'range': [0, 15], 'color': "rgba(16, 185, 129, 0.3)"},
                    {'range': [15, 25], 'color': "rgba(245, 158, 11, 0.3)"},
                    {'range': [25, 45], 'color': "rgba(244, 63, 94, 0.4)"}
                ],
                'threshold': {
                    'line': {'color': "#ef4444", 'width': 4},
                    'thickness': 0.75,
                    'value': 25.0
                }
            }
        ))
        fig_gauge.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=250,
            margin=dict(l=20, r=20, t=30, b=10)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)


# =============================================================================
# TAB 6: REAL-TIME LOAN SIMULATOR & AMORTIZATION
# =============================================================================
with t_sim:
    st.subheader("🧮 Borrower Underwriting & Interactive EMI Amortization Simulator")
    st.write("Model loan principal repayments, evaluate debt burden capacity, and generate a dynamic repayment schedule.")

    col_calc1, col_calc2 = st.columns([5, 5])

    with col_calc1:
        st.markdown("##### 🎛️ Loan Underwriting Inputs")
        sim_amt = st.slider("Loan Principal ($)", min_value=1000, max_value=40000, value=15000, step=500)
        sim_rate = st.slider("Annual Interest Rate APR (%)", min_value=5.0, max_value=28.0, value=11.99, step=0.25)
        sim_term = st.selectbox("Repayment Duration", options=[36, 60], format_func=lambda x: f"{x} Months ({x // 12} Years)")
        sim_income = st.number_input("Borrower Annual Income ($)", min_value=12000.0, value=78000.0, step=2500.0)
        sim_exist_debt = st.number_input("Existing Monthly Debt Obligations ($)", min_value=0.0, value=650.0, step=50.0)

        # Standard Amortization Math
        monthly_r = (sim_rate / 100.0) / 12.0
        emi = (sim_amt * monthly_r * ((1 + monthly_r) ** sim_term)) / (((1 + monthly_r) ** sim_term) - 1)
        total_pay = emi * sim_term
        total_int = total_pay - sim_amt
        monthly_inc = sim_income / 12.0
        total_monthly_obligations = sim_exist_debt + emi
        calculated_dti = (total_monthly_obligations / monthly_inc) * 100.0

    with col_calc2:
        st.markdown("##### 🔮 Underwriting Output & Recommendation")
        o1, o2 = st.columns(2)
        with o1:
            st.metric("Monthly EMI Payment", f"${emi:,.2f}")
            st.metric("Total Repayment Amount", f"${total_pay:,.2f}")
        with o2:
            st.metric("Total Interest Charged", f"${total_int:,.2f}")
            st.metric("Projected Total DTI", f"{calculated_dti:.1f}%")

        if calculated_dti < 20:
            st.markdown("""
            <div style="background:rgba(16,185,129,0.15); border:1px solid #10b981; border-radius:12px; padding:14px; margin-top:10px;">
                <h5 style="color:#34d399; margin:0 0 4px 0;">🟢 Prime Credit Classification (Low Risk)</h5>
                <p style="margin:0; font-size:0.85rem; color:#f1f5f9;">Excellent capacity to service debt. Fast-track approval recommended.</p>
            </div>
            """, unsafe_allow_html=True)
        elif calculated_dti <= 35:
            st.markdown("""
            <div style="background:rgba(245,158,11,0.15); border:1px solid #f59e0b; border-radius:12px; padding:14px; margin-top:10px;">
                <h5 style="color:#fbbf24; margin:0 0 4px 0;">🟡 Near-Prime Credit Classification (Moderate Risk)</h5>
                <p style="margin:0; font-size:0.85rem; color:#f1f5f9;">Moderate debt burden. Standard income and employment verification required.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(244,63,94,0.15); border:1px solid #f43f5e; border-radius:12px; padding:14px; margin-top:10px;">
                <h5 style="color:#fb7185; margin:0 0 4px 0;">🔴 Subprime Credit Classification (Elevated Risk)</h5>
                <p style="margin:0; font-size:0.85rem; color:#f1f5f9;">High debt-to-income ratio exceeds 35%. Require co-signer or reduced principal.</p>
            </div>
            """, unsafe_allow_html=True)

    # Dynamic Amortization Schedule Chart
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("##### 📅 Loan Principal & Interest Amortization Curve")

    balance = sim_amt
    schedule = []
    for m in range(1, sim_term + 1):
        interest_m = balance * monthly_r
        principal_m = emi - interest_m
        balance = max(0, balance - principal_m)
        schedule.append({"Month": m, "Principal": principal_m, "Interest": interest_m, "Remaining Balance": balance})

    df_sched = pd.DataFrame(schedule)
    fig_amort = go.Figure()
    fig_amort.add_trace(go.Scatter(x=df_sched["Month"], y=df_sched["Remaining Balance"], name="Remaining Principal Balance ($)", line=dict(color="#38bdf8", width=3)))
    fig_amort.add_trace(go.Bar(x=df_sched["Month"], y=df_sched["Principal"], name="Principal Repayment ($)", marker_color="#10b981", opacity=0.7))
    fig_amort.add_trace(go.Bar(x=df_sched["Month"], y=df_sched["Interest"], name="Interest Paid ($)", marker_color="#f59e0b", opacity=0.7))
    fig_amort.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.4)",
        height=320,
        barmode="stack",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_amort, use_container_width=True)


# -----------------------------------------------------------------------------
# 7. Data Export Drawer & Footer
# -----------------------------------------------------------------------------
st.markdown("---")
col_f1, col_f2 = st.columns([7, 3])

with col_f1:
    st.caption("🏛️ **Apex Bank Credit Analytics** | Designed with Streamlit, Plotly, T-SQL, Power BI & Tableau | Developed by **Aditya Mahato**")

with col_f2:
    csv_buf = io.BytesIO()
    df.head(1000).to_csv(csv_buf, index=False)
    st.download_button(
        label="📥 Download Filtered Sample (.CSV)",
        data=csv_buf.getvalue(),
        file_name="bank_loan_filtered_sample.csv",
        mime="text/csv",
        use_container_width=True
    )
