"""
Bank Loan Portfolio & Credit Risk Analytics Dashboard.
Built with Streamlit, Plotly & Pandas.
Provides Executive Summary KPIs, Good vs. Bad Loan Profiling, Geographic Trends,
Credit Grade Risk Matrices, and an Interactive Loan EMI & Risk Assessment Simulator.
"""

import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# Page Configuration & Modern Theme Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Bank Loan Portfolio & Credit Risk Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark-mode banking intelligence aesthetic
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .metric-title {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .metric-delta {
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 4px;
    }
    .delta-green { color: #10b981; }
    .delta-red { color: #ef4444; }
    .delta-blue { color: #38bdf8; }
    .delta-gold { color: #f59e0b; }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Data Loading Engine (Cached)
# -----------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def load_bank_loan_data():
    """Load loan dataset from compressed parquet or csv with synthetic fallback."""
    parquet_path = os.path.join(os.path.dirname(__file__), "data", "bank_loan_data.parquet")
    csv_path = os.path.join(os.path.dirname(__file__), "data", "bank_loan_data.csv.gz")

    if os.path.exists(parquet_path):
        df = pd.read_parquet(parquet_path)
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path, compression="gzip")
    else:
        # High-fidelity synthetic fallback
        np.random.seed(42)
        n = 10000
        states = ["CA", "NY", "TX", "FL", "IL", "PA", "OH", "GA", "NC", "VA", "WA", "AZ", "CO"]
        grades = ["A", "B", "C", "D", "E", "F", "G"]
        purposes = ["debt_consolidation", "credit_card", "home_improvement", "major_purchase", "small_business", "car"]
        emp_lens = ["< 1 year", "2 years", "5 years", "10+ years"]
        home_owns = ["RENT", "MORTGAGE", "OWN"]

        dates = pd.date_range(start="2021-01-01", end="2021-12-31", periods=n)
        amounts = np.random.normal(11200, 7400, n).clip(1000, 35000).astype(int)
        int_rates = np.random.uniform(0.06, 0.24, n)
        dtis = np.random.uniform(0.05, 0.30, n)
        annual_incs = np.random.normal(69000, 35000, n).clip(20000, 250000)

        statuses = np.random.choice(["Fully Paid", "Charged Off", "Current"], size=n, p=[0.83, 0.14, 0.03])
        payments = amounts * (1 + int_rates * 1.5)
        payments[statuses == "Charged Off"] = payments[statuses == "Charged Off"] * np.random.uniform(0.2, 0.6, sum(statuses == "Charged Off"))

        df = pd.DataFrame({
            "id": range(100000, 100000 + n),
            "address_state": np.random.choice(states, n),
            "grade": np.random.choice(grades, n, p=[0.25, 0.30, 0.20, 0.12, 0.08, 0.03, 0.02]),
            "sub_grade": [f"{g}{np.random.randint(1, 6)}" for g in np.random.choice(grades, n)],
            "purpose": np.random.choice(purposes, n, p=[0.48, 0.24, 0.10, 0.07, 0.06, 0.05]),
            "term": np.random.choice([" 36 months", " 60 months"], n, p=[0.75, 0.25]),
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


df = load_bank_loan_data()

# -----------------------------------------------------------------------------
# Sidebar Filtering Controls
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bank-building.png", width=64)
    st.title("Bank Loan Analytics")
    st.caption("Credit Risk & Portfolio Intelligence")
    st.markdown("---")

    st.subheader("🎛️ Filter Portfolio")
    selected_grades = st.multiselect(
        "Credit Grades",
        options=sorted(df["grade"].unique()),
        default=sorted(df["grade"].unique())
    )

    selected_terms = st.multiselect(
        "Loan Term",
        options=sorted(df["term"].unique()),
        default=sorted(df["term"].unique())
    )

    selected_purposes = st.multiselect(
        "Loan Purpose",
        options=sorted(df["purpose"].unique()),
        default=sorted(df["purpose"].unique())
    )

    st.markdown("---")
    st.caption("📌 **Tech Stack:** `Python` | `Power BI` | `Tableau` | `SQL Server` | `Streamlit`")


# Apply Filters
filtered_df = df[
    (df["grade"].isin(selected_grades)) &
    (df["term"].isin(selected_terms)) &
    (df["purpose"].isin(selected_purposes))
]


# -----------------------------------------------------------------------------
# Top Header Banner
# -----------------------------------------------------------------------------
st.title("🏦 Bank Loan Portfolio & Credit Risk Analytics")
st.markdown("Executive portfolio KPIs, Month-over-Month (MoM) loan issuance tracking, Good vs. Bad loan risk profiling, and geographic capital allocation.")

# Metric Calculations
total_apps = len(filtered_df)
total_funded = filtered_df["loan_amount"].sum()
total_received = filtered_df["total_payment"].sum()
avg_int_rate = filtered_df["int_rate"].mean() * 100
avg_dti = filtered_df["dti"].mean() * 100

# Month-to-Date (MTD: Dec 2021) vs Prior MTD (PMTD: Nov 2021)
mtd_df = filtered_df[(filtered_df["month_number"] == 12) & (filtered_df["year"] == 2021)]
pmtd_df = filtered_df[(filtered_df["month_number"] == 11) & (filtered_df["year"] == 2021)]

mtd_apps = len(mtd_df)
pmtd_apps = len(pmtd_df) if len(pmtd_df) > 0 else 1
mom_apps_growth = ((mtd_apps - pmtd_apps) / pmtd_apps) * 100

mtd_funded = mtd_df["loan_amount"].sum()
pmtd_funded = pmtd_df["loan_amount"].sum() if pmtd_df["loan_amount"].sum() > 0 else 1
mom_funded_growth = ((mtd_funded - pmtd_funded) / pmtd_funded) * 100

mtd_received = mtd_df["total_payment"].sum()
pmtd_received = pmtd_df["total_payment"].sum() if pmtd_df["total_payment"].sum() > 0 else 1
mom_received_growth = ((mtd_received - pmtd_received) / pmtd_received) * 100

# Top KPI Metric Cards
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Applications</div>
        <div class="metric-value">{total_apps:,}</div>
        <div class="metric-delta delta-green">📈 MTD MoM: +{mom_apps_growth:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Capital Funded</div>
        <div class="metric-value">${total_funded / 1e6:.1f}M</div>
        <div class="metric-delta delta-blue">💰 MTD MoM: +{mom_funded_growth:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Cash Received</div>
        <div class="metric-value">${total_received / 1e6:.1f}M</div>
        <div class="metric-delta delta-green">💵 MTD MoM: +{mom_received_growth:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Average Interest Rate</div>
        <div class="metric-value">{avg_int_rate:.2f}%</div>
        <div class="metric-delta delta-gold">📊 Portfolio Yield</div>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Average DTI Ratio</div>
        <div class="metric-value">{avg_dti:.2f}%</div>
        <div class="metric-delta delta-blue">🛡️ Borrower Leverage</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Main Dashboard Tabs
# -----------------------------------------------------------------------------
tab_summary, tab_risk, tab_geo, tab_grades, tab_sim = st.tabs([
    "📊 Executive Portfolio Summary",
    "🛡️ Good vs. Bad Loans (Credit Risk)",
    "🗺️ Geographic & Regional Trends",
    "⭐ Credit Grade & Segmentation Deep-Dive",
    "🧮 Interactive EMI & Risk Calculator"
])


# =============================================================================
# TAB 1: EXECUTIVE SUMMARY
# =============================================================================
with tab_summary:
    col_s1, col_s2 = st.columns([6, 4])

    with col_s1:
        st.subheader("Monthly Loan Issuance & Cash Recovery Trend")
        monthly_grp = filtered_df.groupby(["month_number", "month_name"]).agg(
            funded=("loan_amount", "sum"),
            received=("total_payment", "sum"),
            apps=("id", "count")
        ).reset_index().sort_values("month_number")

        fig_month = go.Figure()
        fig_month.add_trace(go.Bar(x=monthly_grp["month_name"], y=monthly_grp["funded"], name="Funded Capital ($)", marker_color="#38bdf8"))
        fig_month.add_trace(go.Bar(x=monthly_grp["month_name"], y=monthly_grp["received"], name="Received Capital ($)", marker_color="#10b981"))
        fig_month.update_layout(template="plotly_dark", height=350, barmode="group", hovermode="x unified", legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_month, use_container_width=True)

    with col_s2:
        st.subheader("Top Loan Purposes Breakdown")
        purpose_grp = filtered_df.groupby("purpose")["loan_amount"].sum().reset_index().sort_values("loan_amount", ascending=False).head(6)
        fig_purpose = px.pie(
            purpose_grp,
            names="purpose",
            values="loan_amount",
            hole=0.45,
            color_discrete_sequence=px.colors.sequential.Teal
        )
        fig_purpose.update_layout(template="plotly_dark", height=350)
        st.plotly_chart(fig_purpose, use_container_width=True)


# =============================================================================
# TAB 2: GOOD VS BAD LOANS (CREDIT RISK)
# =============================================================================
with tab_risk:
    st.subheader("🛡️ Portfolio Credit Quality: Performing vs. Default Risk")

    good_df = filtered_df[filtered_df["is_good_loan"] == 1]
    bad_df = filtered_df[filtered_df["is_bad_loan"] == 1]

    good_apps = len(good_df)
    bad_apps = len(bad_df)
    good_pct = (good_apps / total_apps * 100) if total_apps > 0 else 0
    bad_pct = (bad_apps / total_apps * 100) if total_apps > 0 else 0

    good_funded = good_df["loan_amount"].sum()
    good_received = good_df["total_payment"].sum()
    bad_funded = bad_df["loan_amount"].sum()
    bad_received = bad_df["total_payment"].sum()
    bad_net_loss = max(0, bad_funded - bad_received)

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown(f"""
        <div style="background:#064e3b; border:1px solid #10b981; border-radius:10px; padding:16px 20px;">
            <h4 style="color:#10b981; margin:0 0 10px 0;">🟢 Good Loan Portfolio (Fully Paid & Current)</h4>
            <p style="margin:2px 0; color:#f8fafc;"><b>Good Loan Share:</b> {good_pct:.1f}% ({good_apps:,} Applications)</p>
            <p style="margin:2px 0; color:#f8fafc;"><b>Funded Capital:</b> ${good_funded / 1e6:.1f}M</p>
            <p style="margin:2px 0; color:#f8fafc;"><b>Total Cash Collected:</b> ${good_received / 1e6:.1f}M</p>
            <p style="margin:2px 0; color:#10b981;"><b>Net Recovery Profit:</b> +${(good_received - good_funded) / 1e6:.1f}M</p>
        </div>
        """, unsafe_allow_html=True)

    with col_g2:
        st.markdown(f"""
        <div style="background:#450a0a; border:1px solid #ef4444; border-radius:10px; padding:16px 20px;">
            <h4 style="color:#ef4444; margin:0 0 10px 0;">🔴 Bad Loan Portfolio (Charged Off Defaults)</h4>
            <p style="margin:2px 0; color:#f8fafc;"><b>Default Rate:</b> {bad_pct:.1f}% ({bad_apps:,} Applications)</p>
            <p style="margin:2px 0; color:#f8fafc;"><b>Disbursed Capital at Risk:</b> ${bad_funded / 1e6:.1f}M</p>
            <p style="margin:2px 0; color:#f8fafc;"><b>Recovered Prior to Default:</b> ${bad_received / 1e6:.1f}M</p>
            <p style="margin:2px 0; color:#ef4444;"><b>Net Capital Charge-Off Loss:</b> -${bad_net_loss / 1e6:.1f}M</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_r1, col_r2 = st.columns([5, 5])
    with col_r1:
        st.write("##### Loan Status Distribution")
        status_counts = filtered_df["loan_status"].value_counts().reset_index()
        status_counts.columns = ["loan_status", "count"]
        fig_status = px.pie(
            status_counts,
            names="loan_status",
            values="count",
            hole=0.45,
            color="loan_status",
            color_discrete_map={"Fully Paid": "#10b981", "Current": "#38bdf8", "Charged Off": "#ef4444"}
        )
        fig_status.update_layout(template="plotly_dark", height=320)
        st.plotly_chart(fig_status, use_container_width=True)

    with col_r2:
        st.write("##### Capital Recovery by Loan Status")
        status_grp = filtered_df.groupby("loan_status").agg(
            funded=("loan_amount", "sum"),
            received=("total_payment", "sum")
        ).reset_index()
        fig_rec = px.bar(
            status_grp,
            x="loan_status",
            y=["funded", "received"],
            barmode="group",
            labels={"value": "Amount ($)", "loan_status": "Loan Status"},
            color_discrete_sequence=["#38bdf8", "#10b981"]
        )
        fig_rec.update_layout(template="plotly_dark", height=320)
        st.plotly_chart(fig_rec, use_container_width=True)


# =============================================================================
# TAB 3: GEOGRAPHIC & REGIONAL TRENDS
# =============================================================================
with tab_geo:
    st.subheader("🗺️ US State-Level Credit Exposure & Default Risk Map")

    state_summary = filtered_df.groupby("address_state").agg(
        total_apps=("id", "count"),
        total_funded=("loan_amount", "sum"),
        total_received=("total_payment", "sum"),
        avg_dti=("dti", "mean"),
        defaults=("is_bad_loan", "sum")
    ).reset_index()
    state_summary["default_rate"] = (state_summary["defaults"] / state_summary["total_apps"] * 100).round(2)
    state_summary["avg_dti"] = (state_summary["avg_dti"] * 100).round(2)

    col_m1, col_m2 = st.columns([7, 3])

    with col_m1:
        fig_map = px.choropleth(
            state_summary,
            locations="address_state",
            locationmode="USA-states",
            color="total_funded",
            scope="usa",
            hover_name="address_state",
            hover_data={"total_funded": ":$,.0f", "total_apps": ":,", "default_rate": ":.2f%"},
            color_continuous_scale="Viridis",
            labels={"total_funded": "Total Funded ($)"},
            title="State-wise Loan Portfolio Capital Allocation"
        )
        fig_map.update_layout(template="plotly_dark", height=420)
        st.plotly_chart(fig_map, use_container_width=True)

    with col_m2:
        st.write("##### Top 10 States by Volume")
        st.dataframe(
            state_summary.sort_values("total_funded", ascending=False)[["address_state", "total_apps", "total_funded", "default_rate"]].head(10),
            use_container_width=True
        )


# =============================================================================
# TAB 4: CREDIT GRADE DEEP DIVE
# =============================================================================
with tab_grades:
    st.subheader("⭐ Credit Grade & Borrower Risk Profile Breakdown")

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.write("##### Default Rate & Interest Rate Progression by Credit Grade")
        grade_grp = filtered_df.groupby("grade").agg(
            total_apps=("id", "count"),
            funded=("loan_amount", "sum"),
            avg_int=("int_rate", "mean"),
            defaults=("is_bad_loan", "sum")
        ).reset_index()
        grade_grp["default_rate"] = (grade_grp["defaults"] / grade_grp["total_apps"] * 100).round(2)
        grade_grp["avg_int"] = (grade_grp["avg_int"] * 100).round(2)

        fig_grade = go.Figure()
        fig_grade.add_trace(go.Bar(x=grade_grp["grade"], y=grade_grp["avg_int"], name="Avg Interest Rate (%)", marker_color="#f59e0b"))
        fig_grade.add_trace(go.Line(x=grade_grp["grade"], y=grade_grp["default_rate"], name="Default Rate (%)", marker_color="#ef4444", mode="lines+markers"))
        fig_grade.update_layout(template="plotly_dark", height=340, hovermode="x unified", legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_grade, use_container_width=True)

    with col_g2:
        st.write("##### Loan Term Breakdown (36 vs 60 Months)")
        term_grp = filtered_df.groupby("term").agg(
            funded=("loan_amount", "sum"),
            received=("total_payment", "sum")
        ).reset_index()
        fig_term = px.bar(
            term_grp,
            x="term",
            y=["funded", "received"],
            barmode="group",
            color_discrete_sequence=["#38bdf8", "#10b981"],
            title="Loan Term Capital Distribution"
        )
        fig_term.update_layout(template="plotly_dark", height=340)
        st.plotly_chart(fig_term, use_container_width=True)


# =============================================================================
# TAB 5: LOAN EMI & RISK CALCULATOR
# =============================================================================
with tab_sim:
    st.subheader("🧮 Interactive Loan Repayment & Borrower Risk Tier Simulator")
    st.write("Evaluate potential borrower loan terms, monthly installments (EMI), Debt-to-Income impact, and credit risk rating in real-time.")

    col_c1, col_c2 = st.columns([5, 5])

    with col_c1:
        st.write("##### 🎛️ Loan Parameters")
        sim_loan_amt = st.slider("Loan Principal Amount ($)", min_value=1000, max_value=40000, value=15000, step=500)
        sim_int_rate = st.slider("Annual Interest Rate (%)", min_value=5.0, max_value=28.0, value=12.5, step=0.25)
        sim_term_months = st.selectbox("Repayment Term", options=[36, 60], format_func=lambda x: f"{x} Months ({x // 12} Years)")
        sim_annual_inc = st.number_input("Borrower Annual Income ($)", min_value=10000.0, value=75000.0, step=2500.0)
        sim_monthly_debt = st.number_input("Existing Monthly Debt Obligations ($)", min_value=0.0, value=650.0, step=50.0)

        # Financial Calculations (Standard Amortization Formula)
        monthly_r = (sim_int_rate / 100.0) / 12.0
        emi = (sim_loan_amt * monthly_r * ((1 + monthly_r) ** sim_term_months)) / (((1 + monthly_r) ** sim_term_months) - 1)
        total_repayment = emi * sim_term_months
        total_interest = total_repayment - sim_loan_amt

        monthly_income = sim_annual_inc / 12.0
        total_monthly_debt_with_loan = sim_monthly_debt + emi
        calculated_dti = (total_monthly_debt_with_loan / monthly_income) * 100.0

    with col_c2:
        st.write("##### 🔮 Underwriting Assessment & Output")
        m_out1, m_out2 = st.columns(2)
        with m_out1:
            st.metric("Monthly EMI Installment", f"${emi:,.2f}")
            st.metric("Total Repayment Amount", f"${total_repayment:,.2f}")
        with m_out2:
            st.metric("Total Interest Payable", f"${total_interest:,.2f}")
            st.metric("Projected DTI Ratio", f"{calculated_dti:.1f}%")

        if calculated_dti < 20:
            st.success("🟢 **Credit Risk Tier: PRIME (Low Risk).** Debt-to-income is well within safe underwriting boundaries (<20%).")
        elif calculated_dti <= 35:
            st.info("🟡 **Credit Risk Tier: NEAR-PRIME (Moderate Risk).** Standard underwriting verification recommended.")
        else:
            st.error("🔴 **Credit Risk Tier: SUBPRIME (High Risk).** DTI exceeds 35% threshold. Recommend co-signer or reduced principal.")

# Footer
st.markdown("---")
st.caption("Bank Loan Portfolio & Credit Risk Analytics | Engineered with Power BI, Tableau, SQL Server & Streamlit")
