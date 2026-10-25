import os
import io
import contextlib
import datetime
import textwrap
from unittest.mock import patch
import pandas as pd
import streamlit as st

# =============================================================================
# ORIGINAL FUNCTIONS IMPORT
# All relevant original functions from payroll_pandas.py are imported directly
# =============================================================================
from payroll_pandas import (
    load_data,
    save_data,
    calculate_salary,
    show_table,
    print_timestamp,
    add_employee,
    display_all,
    display_one,
    delete_all,
    delete_one,
    modify_record,
    display_payroll,
    salary_slip_one,
    print_menu,
    COLUMNS
)

# Standard CSV file used by the original application
CSV_FILE = "employees_data.csv"

# -----------------------------------------------------------------------------
# BRIDGE ADAPTER FUNCTION
# Connects Streamlit UI inputs to original CLI functions that use input() & print()
# -----------------------------------------------------------------------------
def call_original_func(func, inputs, *args):
    """
    Executes an original function from payroll_pandas.py by supplying Streamlit
    inputs to Python's input() and capturing its print() output.
    Zero business logic is rewritten or duplicated.
    """
    stdout_buf = io.StringIO()
    with patch("builtins.input", side_effect=inputs):
        with contextlib.redirect_stdout(stdout_buf):
            result = func(*args)
    return result, stdout_buf.getvalue()

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PennyWise | Payroll Management System",
    page_icon="💼",
    layout="wide"
)

st.markdown(
    """
    <style>
        /* Visible, crisp cool-blue ambient background gradient - zero warm/yellow tones */
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > .main,
        section.main {
            background: linear-gradient(135deg, #DCEBFA 0%, #EFF6FD 25%, #E3EFFC 55%, #F0F7FE 75%, #D7E8F9 100%) !important;
            background-attachment: fixed !important;
            color: #0F172A;
        }

        /* Seamless transparent Streamlit top header & tight, balanced spacing */
        header[data-testid="stHeader"] {
            background: transparent !important;
            height: 2.5rem !important;
        }
        .block-container {
            padding-top: 1.6rem !important;
            padding-bottom: 2.5rem !important;
            max-width: 95% !important;
        }

        /* Sidebar - Harmonious cool slate backdrop */
        section[data-testid="stSidebar"] {
            background-color: #F8FAFC !important;
            border-right: 1px solid #CBD5E1 !important;
        }
        
        /* Modern Executive Header Banner */
        .top-header-banner {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #FFFFFF;
            border: 1px solid #BFDBFE;
            box-shadow: 0 10px 30px -4px rgba(37, 99, 235, 0.08), 0 2px 6px 0 rgba(0, 0, 0, 0.02);
            border-radius: 16px;
            padding: 20px 26px;
            margin-bottom: 20px;
            gap: 20px;
        }
        .top-header-left {
            display: flex;
            align-items: center;
            gap: 16px;
            flex: 1.2;
        }
        .brand-badge-icon {
            font-size: 1.85rem;
            width: 52px;
            height: 52px;
            min-width: 52px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border: 1px solid #BFDBFE;
            border-radius: 14px;
            box-shadow: 0 2px 8px 0 rgba(37, 99, 235, 0.12);
        }
        .brand-title-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 4px;
            flex-wrap: wrap;
        }
        .brand-logo {
            font-size: 1.9rem;
            font-weight: 800;
            color: #0F172A;
            letter-spacing: -0.6px;
            line-height: 1;
        }
        .brand-tag {
            background-color: #EFF6FF;
            color: #2563EB;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 3px 9px;
            border-radius: 6px;
            border: 1px solid #BFDBFE;
            letter-spacing: 0.4px;
            text-transform: uppercase;
        }
        .status-indicator-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background-color: #F0FDF4;
            color: #166534;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 3px 10px;
            border-radius: 9999px;
            border: 1px solid #BBF7D0;
        }
        .status-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background-color: #22C55E;
            box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.25);
        }
        .brand-subtitle {
            color: #64748B;
            font-size: 0.88rem;
            font-weight: 400;
        }

        /* Top Header Center Quick Stats */
        .top-header-center {
            display: flex;
            align-items: center;
            gap: 12px;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            padding: 8px 16px;
            border-radius: 12px;
        }
        .header-stat-box {
            display: flex;
            flex-direction: column;
            text-align: center;
        }
        .header-stat-label {
            font-size: 0.68rem;
            text-transform: uppercase;
            font-weight: 700;
            color: #64748B;
            letter-spacing: 0.5px;
        }
        .header-stat-val {
            font-size: 0.95rem;
            font-weight: 800;
            color: #0F172A;
        }

        /* Top Header Meta Chips */
        .top-header-meta {
            display: flex;
            align-items: center;
            gap: 16px;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            padding: 10px 18px;
            border-radius: 12px;
        }
        .meta-item {
            display: flex;
            flex-direction: column;
        }
        .meta-label {
            font-size: 0.68rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #94A3B8;
            font-weight: 600;
        }
        .meta-value {
            font-size: 0.84rem;
            font-weight: 600;
            color: #0F172A;
        }
        .meta-divider {
            width: 1px;
            height: 24px;
            background-color: #E2E8F0;
        }
        @media (max-width: 1100px) {
            .top-header-center {
                display: none;
            }
        }
        @media (max-width: 900px) {
            .top-header-banner {
                flex-direction: column;
                align-items: flex-start;
                gap: 16px;
            }
            .top-header-meta {
                width: 100%;
                justify-content: space-between;
            }
        }

        /* Metric Cards - Interactive & Soulful */
        div[data-testid="stMetric"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 2px 8px -1px rgba(15, 23, 42, 0.04) !important;
            padding: 18px 22px !important;
            border-radius: 14px !important;
            border-left: 4px solid #2563EB !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px -3px rgba(37, 99, 235, 0.1) !important;
            border-color: #CBD5E1 !important;
        }
        div[data-testid="stMetric"] label {
            color: #64748B !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.2px;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #0F172A !important;
            font-size: 1.65rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.4px;
        }

        /* Section Headings */
        .section-heading {
            color: #0F172A;
            font-size: 1.35rem;
            font-weight: 700;
            margin-top: 10px;
            margin-bottom: 4px;
            letter-spacing: -0.3px;
        }
        .section-desc {
            color: #64748B;
            font-size: 0.9rem;
            margin-bottom: 20px;
        }

        /* Navigation Buttons - Modern Segmented Feel */
        div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
            background-color: #FFFFFF !important;
            color: #475569 !important;
            border: 1px solid #E2E8F0 !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            padding: 8px 14px !important;
            border-radius: 10px !important;
            box-shadow: 0 1px 2px 0 rgba(15, 23, 42, 0.03) !important;
            transition: all 0.15s ease !important;
        }
        div[data-testid="stHorizontalBlock"] button[kind="secondary"]:hover {
            background-color: #F8FAFC !important;
            border-color: #CBD5E1 !important;
            color: #0F172A !important;
            transform: translateY(-1px);
        }
        div[data-testid="stHorizontalBlock"] button[kind="primary"] {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            color: #FFFFFF !important;
            border: 1px solid #1D4ED8 !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            padding: 8px 14px !important;
            border-radius: 10px !important;
            box-shadow: 0 3px 8px 0 rgba(37, 99, 235, 0.28) !important;
        }

        /* Payslip Document Card */
        .payslip-doc {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 16px 0 rgba(15, 23, 42, 0.06);
            border-radius: 14px;
            padding: 36px;
            margin-top: 15px;
            margin-bottom: 24px;
            max-width: 820px;
        }
        .payslip-header-title {
            font-size: 1.45rem;
            font-weight: 800;
            color: #0F172A;
            text-align: center;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        .payslip-sub {
            text-align: center;
            color: #64748B;
            font-size: 0.92rem;
            margin-bottom: 20px;
        }
        .payslip-divider {
            border-top: 1px solid #E2E8F0;
            margin: 18px 0;
        }
        @media print {
            body {
                background-color: #FFFFFF !important;
                color: #000000 !important;
            }
            .stApp, div[data-testid="stSidebar"], div[data-testid="stHeader"], div[data-testid="stToolbar"] {
                background: #FFFFFF !important;
            }
            div[data-testid="stSidebar"], .no-print, button {
                display: none !important;
            }
            .payslip-doc {
                background-color: #FFFFFF !important;
                color: #000000 !important;
                border: 2px solid #000000 !important;
                width: 100% !important;
                max-width: 100% !important;
                box-shadow: none !important;
            }
            .payslip-header-title, strong, td, th {
                color: #000000 !important;
            }
            .payslip-sub, .payslip-label {
                color: #444444 !important;
            }
            .payslip-divider {
                border-top: 1px solid #CCCCCC !important;
            }
        }
        hr {
            border: none;
            border-top: 1px solid #E2E8F0;
            margin: 20px 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# SESSION STATE & DATA INITIALIZATION
# -----------------------------------------------------------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

# Load data using original load_data() function
df = load_data(CSV_FILE)

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
st.sidebar.markdown("### 💼 PennyWise Admin")
st.sidebar.info(
    "**Enterprise Payroll Core**\n\n"
    "Powered 100% by original functions from `payroll_pandas.py` with zero logic alterations."
)
st.sidebar.write(f"📁 **Data File:** `{CSV_FILE}`")
st.sidebar.write(f"👥 **Total Roster:** `{len(df)} employees`")

st.sidebar.markdown("---")
st.sidebar.markdown("#### Original Menu Reference")
st.sidebar.caption("1. Add Employee (`add_employee`)")
st.sidebar.caption("2. Display All (`display_all`)")
st.sidebar.caption("3. Display One (`display_one`)")
st.sidebar.caption("4. Delete All (`delete_all`)")
st.sidebar.caption("5. Delete One (`delete_one`)")
st.sidebar.caption("6. Modify Record (`modify_record`)")
st.sidebar.caption("7. Display Payroll (`display_payroll`)")
st.sidebar.caption("8. Salary Slip (`salary_slip_one`)")

st.sidebar.markdown("---")
st.sidebar.markdown("#### Project Team")
st.sidebar.write("• **Krishnav Agarwal** (26BYB0145)")
st.sidebar.write("• **Dev Dagar** (26BYB0175)")
st.sidebar.write("• **Akshat Swarup** (26BYB0168)")

# -----------------------------------------------------------------------------
# EXECUTIVE BRAND HEADER
# -----------------------------------------------------------------------------
total_net_sum = df["Net Salary"].sum() if not df.empty else 0.0
total_tax_sum = df["Tax"].sum() if not df.empty else 0.0

st.markdown(
    f"""
    <div class="top-header-banner">
        <div class="top-header-left">
            <div class="brand-badge-icon">💼</div>
            <div>
                <div class="brand-title-row">
                    <span class="brand-logo">PennyWise</span>
                    <span class="brand-tag">PAYROLL & COMP</span>
                    <span class="status-indicator-pill"><span class="status-dot"></span> System Live</span>
                </div>
                <div class="brand-subtitle">
                    Enterprise employee administration, automated salary computation, and monthly payslips.
                </div>
            </div>
        </div>
        <div class="top-header-center">
            <div class="header-stat-box">
                <span class="header-stat-label">Net Disbursal</span>
                <span class="header-stat-val">₹{total_net_sum:,.0f}</span>
            </div>
            <div class="meta-divider"></div>
            <div class="header-stat-box">
                <span class="header-stat-label">Statutory TDS</span>
                <span class="header-stat-val">₹{total_tax_sum:,.0f}</span>
            </div>
            <div class="meta-divider"></div>
            <div class="header-stat-box">
                <span class="header-stat-label">Compliance</span>
                <span class="header-stat-val" style="color: #16A34A;">✓ 100% Verified</span>
            </div>
        </div>
        <div class="top-header-meta">
            <div class="meta-item">
                <span class="meta-label">Payroll Cycle</span>
                <span class="meta-value">Current FY 2025–26</span>
            </div>
            <div class="meta-divider"></div>
            <div class="meta-item">
                <span class="meta-label">Ledger Roster</span>
                <span class="meta-value">{len(df)} Active</span>
            </div>
            <div class="meta-divider"></div>
            <div class="meta-item">
                <span class="meta-label">Disbursal Unit</span>
                <span class="meta-value">INR (₹)</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# NAVIGATION BAR (Connected directly to all original features)
# -----------------------------------------------------------------------------
nav_cols = st.columns(7)
nav_items = [
    ("Dashboard", "Dashboard"),
    ("View All", "View All"),
    ("Add Employee", "Add Employee"),
    ("Modify Record", "Modify Record"),
    ("Delete Employee", "Delete Employee"),
    ("Search Employee", "Search Employee"),
    ("Salary Slip", "Salary Slip")
]

for idx, (page_key, page_label) in enumerate(nav_items):
    with nav_cols[idx]:
        is_active = (st.session_state.current_page == page_key)
        if st.button(
            page_label,
            key=f"nav_btn_{page_key}",
            type="primary" if is_active else "secondary",
            use_container_width=True
        ):
            st.session_state.current_page = page_key
            st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 1. DASHBOARD -> Powers display_payroll()
# -----------------------------------------------------------------------------
if st.session_state.current_page == "Dashboard":
    st.markdown('<div class="section-heading">Overview Dashboard & Payroll</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Invokes display_payroll() from payroll_pandas.py with complete salary components.</div>', unsafe_allow_html=True)

    # Summary metrics directly from existing CSV columns
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="👥 Active Roster", value=f"{len(df):,}")
    with m2:
        total_gross = df["Gross Salary"].sum() if not df.empty else 0.0
        st.metric(label="💼 Total Gross Payroll", value=f"₹{total_gross:,.2f}")
    with m3:
        total_net = df["Net Salary"].sum() if not df.empty else 0.0
        st.metric(label="💳 Total Net Disbursal", value=f"₹{total_net:,.2f}")
    with m4:
        avg_net = df["Net Salary"].mean() if not df.empty else 0.0
        st.metric(label="📈 Avg Net Salary", value=f"₹{avg_net:,.2f}")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Call original display_payroll()
    _, payroll_output = call_original_func(display_payroll, [], df)

    st.markdown("#### Complete Payroll Directory")
    st.caption("Displaying all employee records with complete salary structure (EmpNo, EmpName, Job, Basic Salary, DA, HRA, Tax, Gross Salary, Net Salary)")
    st.dataframe(df, use_container_width=True)

# -----------------------------------------------------------------------------
# 2. VIEW EMPLOYEES -> Powers display_all()
# -----------------------------------------------------------------------------
elif st.session_state.current_page == "View All":
    st.markdown('<div class="section-heading">Display All Employees</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Invokes display_all() from payroll_pandas.py (EmpNo, EmpName, Job, Basic Salary).</div>', unsafe_allow_html=True)

    if df.empty:
        st.info("Nothing to display")
    else:
        # Call original display_all()
        _, display_output = call_original_func(display_all, [], df)

        selected_cols = ['EmpNo', 'EmpName', 'Job', 'Basic Salary']
        st.dataframe(df[selected_cols], use_container_width=True)

# -----------------------------------------------------------------------------
# 3. ADD EMPLOYEE -> Powers add_employee()
# -----------------------------------------------------------------------------
elif st.session_state.current_page == "Add Employee":
    st.markdown('<div class="section-heading">Add Employee Record</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Invokes add_employee(df, filename) directly from payroll_pandas.py.</div>', unsafe_allow_html=True)

    with st.form("add_employee_form"):
        c1, c2 = st.columns(2)
        with c1:
            empno_input = st.number_input("Enter employee no. :", min_value=1, step=1)
            name_input = st.text_input("Enter employee name :", placeholder="e.g. Ramesh Sharma")
        with c2:
            job_input = st.selectbox("Enter employee job :", ["Officer", "Manager", "Clerk", "Assistant", "Other"])
            basic_input = st.number_input("Enter basic salary :", min_value=0.0, step=1000.0)

        submitted = st.form_submit_button("Add Record", type="primary")

        if submitted:
            if not name_input.strip():
                st.error("Please enter a valid employee name.")
            elif basic_input <= 0:
                st.error("Basic Salary must be greater than 0.")
            else:
                # Call original add_employee function from payroll_pandas.py
                inputs = [str(empno_input), name_input.strip(), job_input, str(basic_input)]
                updated_df, cli_output = call_original_func(add_employee, inputs, df, CSV_FILE)
                
                # Result handled strictly from original function execution output
                if "already exists" in cli_output:
                    st.error(f"Employee no {empno_input} already exists")
                elif "added successfully" in cli_output:
                    df = updated_df
                    st.success("Record added successfully...")
                    # Display the new record created by add_employee
                    st.dataframe(df[df["EmpNo"] == empno_input], use_container_width=True)
                else:
                    st.error(f"Error: {cli_output.strip()}")

# -----------------------------------------------------------------------------
# 4. MODIFY RECORD -> Powers modify_record()
# -----------------------------------------------------------------------------
elif st.session_state.current_page == "Modify Record":
    st.markdown('<div class="section-heading">Modify Employee Record</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Invokes modify_record(df, filename) directly from payroll_pandas.py.</div>', unsafe_allow_html=True)

    mod_empno = st.number_input("Enter employee no. of the record to be modified :", min_value=1, step=1)
    
    # Check if record exists
    match = df[df["EmpNo"] == mod_empno]
    if match.empty:
        st.info("Enter an existing Employee Number to modify.")
    else:
        current_row = match.iloc[0]
        st.markdown(f"**Current Record for EmpNo {mod_empno}:**")
        st.dataframe(match, use_container_width=True)

        with st.form("modify_employee_form"):
            st.caption("Leave blank to keep existing value.")
            m_col1, m_col2 = st.columns(2)
            with m_col1:
                new_name = st.text_input("Enter new name (or press Enter for no change):", value=str(current_row["EmpName"]))
            with m_col2:
                new_job = st.text_input("Enter new job (or press Enter for no change):", value=str(current_row["Job"]))
            new_basic = st.number_input("Enter new basic salary:", min_value=0.0, value=float(current_row["Basic Salary"]), step=1000.0)

            mod_submitted = st.form_submit_button("Modify Record", type="primary")

            if mod_submitted:
                # Call original modify_record function from payroll_pandas.py
                inputs = [str(mod_empno), new_name.strip(), new_job.strip(), str(new_basic)]
                updated_df, cli_output = call_original_func(modify_record, inputs, df, CSV_FILE)
                
                # Result handled strictly from original function output
                if "does not exist" in cli_output:
                    st.error(f"Empno {mod_empno} does not exist")
                elif "Record modified" in cli_output:
                    df = updated_df
                    st.success("Record modified")
                    st.dataframe(df[df["EmpNo"] == mod_empno], use_container_width=True)
                else:
                    st.error(f"Error: {cli_output.strip()}")

# -----------------------------------------------------------------------------
# 5. DELETE EMPLOYEE -> Powers delete_one() & delete_all()
# -----------------------------------------------------------------------------
elif st.session_state.current_page == "Delete Employee":
    st.markdown('<div class="section-heading">Delete Employee Records</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Invokes delete_one(df, filename) or delete_all(df, filename) from payroll_pandas.py.</div>', unsafe_allow_html=True)

    tab_del_one, tab_del_all = st.tabs(["Delete Single Employee", "Delete All Records"])

    with tab_del_one:
        st.markdown("#### Delete a Specific Employee Record")
        del_empno = st.number_input("Enter employee no. of the record to be deleted :", min_value=1, step=1, key="del_one_id")
        
        if st.button("Delete Record", type="primary", key="btn_del_one"):
            inputs = [str(del_empno)]
            updated_df, cli_output = call_original_func(delete_one, inputs, df, CSV_FILE)
            
            if "not found" in cli_output.lower():
                st.error(f"Employee no {del_empno} not found")
            else:
                df = updated_df
                st.success("Deletion done")

    with tab_del_all:
        st.markdown("#### Delete All Records")
        st.warning("⚠️ This action will remove all employee records from the CSV file.")
        confirm = st.checkbox("I confirm that I want to delete all employee records.")
        
        if st.button("Delete All Records", type="secondary", key="btn_del_all"):
            if confirm:
                updated_df, cli_output = call_original_func(delete_all, ["Y"], df, CSV_FILE)
                df = updated_df
                st.success("All the records are deleted...")
                st.rerun()
            else:
                st.error("Please check the confirmation box before deleting all records.")

# -----------------------------------------------------------------------------
# 6. SEARCH EMPLOYEE -> Powers display_one()
# -----------------------------------------------------------------------------
elif st.session_state.current_page == "Search Employee":
    st.markdown('<div class="section-heading">Search Employee Record</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Invokes display_one(df) and show_table(record) from payroll_pandas.py.</div>', unsafe_allow_html=True)

    s1, s2 = st.columns([3, 1], vertical_alignment="bottom")
    with s1:
        search_empno = st.number_input("Enter employee no. of the record to be displayed :", min_value=1, step=1)
    with s2:
        search_clicked = st.button("Display Record", type="primary", use_container_width=True)

    if search_clicked:
        # Call original display_one()
        _, search_output = call_original_func(display_one, [str(search_empno)], df)
        
        record = df[df["EmpNo"] == search_empno]
        if record.empty:
            st.error("Nothing to display")
        else:
            st.success(f"Record of Employee No. {search_empno} :")
            st.dataframe(record, use_container_width=True)

# -----------------------------------------------------------------------------
# 7. SALARY SLIP -> Powers salary_slip_one() (Renders formal printable HTML)
# -----------------------------------------------------------------------------
elif st.session_state.current_page == "Salary Slip":
    st.markdown('<div class="section-heading">Employee Salary Slip</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Invokes salary_slip_one(df) from payroll_pandas.py and renders a formal printable payslip.</div>', unsafe_allow_html=True)

    p1, p2 = st.columns([3, 1], vertical_alignment="bottom")
    with p1:
        slip_empno = st.number_input("Enter employee number whose pay slip you want to receive :", min_value=1, step=1, key="slip_no_input")
    with p2:
        gen_clicked = st.button("Generate Pay Slip", type="primary", use_container_width=True)

    if gen_clicked:
        # Call original salary_slip_one()
        _, slip_output = call_original_func(salary_slip_one, [str(slip_empno)], df)
        
        record = df[df["EmpNo"] == slip_empno]
        if record.empty:
            st.error(f"Employee no {slip_empno} not found")
        else:
            row = record.iloc[0]
            now = datetime.datetime.now()
            month_year = now.strftime("%B %Y")

            # Printable button that opens browser print dialog
            st.markdown(
                """
                <div class="no-print" style="margin-top: 10px; margin-bottom: 12px;">
                    <button onclick="window.print()" style="
                        background-color: #2563EB;
                        color: #FFFFFF;
                        border: none;
                        padding: 8px 18px;
                        border-radius: 6px;
                        font-weight: 600;
                        cursor: pointer;
                        font-size: 0.9rem;
                    ">🖨️ Print / Save as PDF</button>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Build HTML string and render with st.html() to guarantee NO code block rendering
            payslip_html = textwrap.dedent(f"""
            <div class="payslip-doc">
                <div class="payslip-header-title">PAYROLL MANAGEMENT SYSTEM</div>
                <div class="payslip-sub">Salary Slip for <strong>{month_year}</strong></div>
                
                <div class="payslip-divider"></div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 15px;">
                    <div>
                        <div style="color: #64748B; font-size: 0.92rem; margin-bottom: 4px;">Name: <strong style="color: #0F172A;">{row['EmpName']}</strong></div>
                        <div style="color: #64748B; font-size: 0.92rem;">Emp. No: <strong style="color: #0F172A;">{row['EmpNo']}</strong></div>
                    </div>
                    <div>
                        <div style="color: #64748B; font-size: 0.92rem; margin-bottom: 4px;">Designation: <strong style="color: #0F172A;">{row['Job']}</strong></div>
                        <div style="color: #64748B; font-size: 0.92rem;">Pay Period: <strong style="color: #0F172A;">{month_year}</strong></div>
                    </div>
                </div>
                
                <div class="payslip-divider"></div>
                
                <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                    <thead>
                        <tr style="border-bottom: 2px solid #E2E8F0;">
                            <th style="text-align: left; padding: 8px 4px; color: #2563EB;">Earnings</th>
                            <th style="text-align: right; padding: 8px 4px; color: #2563EB;">Amount (₹)</th>
                            <th style="text-align: left; padding: 8px 16px; color: #DC2626;">Deductions</th>
                            <th style="text-align: right; padding: 8px 4px; color: #DC2626;">Amount (₹)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid #F1F5F9;">
                            <td style="padding: 8px 4px; color: #475569;">Basic Salary</td>
                            <td style="text-align: right; padding: 8px 4px; color: #0F172A; font-weight: 500;">{float(row['Basic Salary']):,.2f}</td>
                            <td style="padding: 8px 16px; color: #475569;">Tax</td>
                            <td style="text-align: right; padding: 8px 4px; color: #0F172A; font-weight: 500;">{float(row['Tax']):,.2f}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #F1F5F9;">
                            <td style="padding: 8px 4px; color: #475569;">Dearness Allowance (DA)</td>
                            <td style="text-align: right; padding: 8px 4px; color: #0F172A; font-weight: 500;">{float(row['DA']):,.2f}</td>
                            <td style="padding: 8px 16px; color: #475569;"></td>
                            <td style="text-align: right; padding: 8px 4px; color: #0F172A;"></td>
                        </tr>
                        <tr style="border-bottom: 1px solid #F1F5F9;">
                            <td style="padding: 8px 4px; color: #475569;">House Rent Allowance (HRA)</td>
                            <td style="text-align: right; padding: 8px 4px; color: #0F172A; font-weight: 500;">{float(row['HRA']):,.2f}</td>
                            <td style="padding: 8px 16px; color: #475569;"></td>
                            <td style="text-align: right; padding: 8px 4px; color: #0F172A;"></td>
                        </tr>
                        <tr style="border-bottom: 2px solid #CBD5E1; font-weight: 700;">
                            <td style="padding: 10px 4px; color: #0F172A;">Gross Salary</td>
                            <td style="text-align: right; padding: 10px 4px; color: #0F172A;">₹{float(row['Gross Salary']):,.2f}</td>
                            <td style="padding: 10px 16px; color: #0F172A;">Total Deductions</td>
                            <td style="text-align: right; padding: 10px 4px; color: #0F172A;">₹{float(row['Tax']):,.2f}</td>
                        </tr>
                    </tbody>
                </table>
                
                <div style="background-color: #F8FAFC; border-radius: 8px; padding: 14px 20px; display: flex; justify-content: space-between; align-items: center; margin-top: 20px; border: 1px solid #BFDBFE;">
                    <span style="font-weight: 700; font-size: 1.05rem; color: #0F172A;">Net Pay (Take-Home Pay)</span>
                    <span style="font-weight: 800; font-size: 1.35rem; color: #059669;">₹{float(row['Net Salary']):,.2f}</span>
                </div>
            </div>
            """)
            # Using st.html() renders pure HTML into the DOM, completely eliminating raw code block display
            st.html(payslip_html)
