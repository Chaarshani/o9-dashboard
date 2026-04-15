import streamlit as st
from data_loader import load_account_summary_customer, load_account_summary_projects, load_home_kpis
import account_summary
import finance
import client_health
import go_lives
import base64
import os

st.set_page_config(
    page_title="o9 Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 1.5rem;
    max-width: 1400px;
}
.home-header {
    font-size: 2.4rem;
    font-weight: 900;
    letter-spacing: -0.5px;
    color: var(--text-color);
    margin-bottom: 0.2rem;
}
.home-sub {
    font-size: 1rem;
    opacity: 0.6;
    color: var(--text-color);
    margin-bottom: 1.5rem;
}
.card {
    border-radius: 16px;
    padding: 28px 26px;
    border-left: 5px solid;
    min-height: 180px;
    background: var(--secondary-background-color);
    border-top: 1px solid rgba(127,127,127,0.15);
    border-right: 1px solid rgba(127,127,127,0.15);
    border-bottom: 1px solid rgba(127,127,127,0.15);
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    box-sizing: border-box;
    margin-bottom: 12px;
}
.card-account { border-color: #2563eb; }
.card-finance { border-color: #10b981; }
.card-health  { border-color: #f59e0b; }
.card-golives { border-color: #8b5cf6; }
.card-title {
    font-size: 1.3rem;
    font-weight: 800;
    margin-bottom: 8px;
    color: var(--text-color);
}
.card-desc {
    font-size: 0.92rem;
    color: var(--text-color);
    opacity: 0.65;
    line-height: 1.6;
}
.chip-row {
    display: flex;
    gap: 8px;
    margin-top: 14px;
    flex-wrap: wrap;
}
.chip {
    border-radius: 8px;
    padding: 3px 10px;
    font-size: 0.8rem;
    font-weight: 700;
}
.chip-blue   { background: rgba(37,99,235,0.12);  color: #2563eb; }
.chip-green  { background: rgba(16,185,129,0.12); color: #10b981; }
.chip-amber  { background: rgba(245,158,11,0.12); color: #f59e0b; }
.chip-red    { background: rgba(220,38,38,0.12);  color: #dc2626; }
.chip-purple { background: rgba(139,92,246,0.12); color: #8b5cf6; }
.sidebar-brand {
    font-size: 1.1rem;
    font-weight: 800;
    color: var(--text-color);
    margin-bottom: 0.3rem;
}
.stButton > button {
    border-radius: 12px !important;
    height: 44px;
    font-weight: 700;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ── Logo ──────────────────────────────────────────────────────────────────
def show_logo():
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.sidebar.markdown(
            f"""<div style="background:white; padding:8px 12px;
                border-radius:10px; display:inline-block;
                margin-bottom:12px;">
                <img src="data:image/png;base64,{data}"
                style="width:80px; display:block;"></div>""",
            unsafe_allow_html=True
        )
    else:
        st.sidebar.markdown("**o9 Solutions**")

# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    show_logo()
    st.markdown('<div class="sidebar-brand">o9 Dashboard</div>',
                unsafe_allow_html=True)
    st.divider()

    pages = ["Home", "Account Summary", "Finance Summary",
             "Client Health", "Go-Lives"]

    selected = st.radio(
        "Navigation", pages,
        index=pages.index(st.session_state.get("page", "Home")),
        label_visibility="collapsed"
    )
    if selected != st.session_state.get("page"):
        st.session_state.page = selected
        st.rerun()

    st.divider()
    st.markdown(
        '<div style="opacity:0.45; font-size:0.78rem;">o9 Solutions · RDAF Team</div>',
        unsafe_allow_html=True
    )

# ── Load data ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def get_data():
    return (
        load_account_summary_customer(),
        load_account_summary_projects()
    )

df_customer, df_projects = get_data()
kpis = load_home_kpis()

# ── Helper ────────────────────────────────────────────────────────────────
def nav_to(page):
    st.session_state.page = page
    st.rerun()

# ── Home ──────────────────────────────────────────────────────────────────
if st.session_state.page == "Home":

    st.markdown('<div class="home-header">o9 Dashboard</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="home-sub">Customer Success · RDAF Team</div>',
                unsafe_allow_html=True)

    

    # Navigation cards
    col1, col2 = st.columns(2, gap="large")
    col3, col4 = st.columns(2, gap="large")

    total_cust = int(kpis["total_customers"])  if kpis is not None else "—"
    total_rev  = f"${kpis['total_revenue']:,.0f}" if kpis is not None else "—"
    green      = int(kpis["green_count"])      if kpis is not None else "—"
    amber      = int(kpis["amber_count"])      if kpis is not None else "—"
    red        = int(kpis["red_count"])        if kpis is not None else "—"
    ref        = int(kpis["referenceable_count"]) if kpis is not None else "—"
    total_proj = int(kpis["total_projects"])   if kpis is not None else "—"
    on_time    = int(kpis["on_time_count"])    if kpis is not None else "—"
    delayed    = int(kpis["delayed_count"])    if kpis is not None else "—"

    with col1:
        st.markdown(f"""
        <div class="card card-account">
            <div class="card-title"> Account Summary</div>
            <div class="card-desc">
                Consolidated per-customer view across finance,
                client health, advocacy and go-lives.
                Drill into any account for a full 360° profile.
            </div>
            <div class="chip-row">
                <span class="chip chip-blue">{total_cust} Customers</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Account Summary →",
                     use_container_width=True, key="nav_account"):
            nav_to("Account Summary")

    with col2:
        st.markdown(f"""
        <div class="card card-finance">
            <div class="card-title"> Finance Summary</div>
            <div class="card-desc">
                Executive finance view — total revenue, SaaS,
                services, gross margin trends, FAC vs EAC
                across the entire portfolio.
            </div>
            <div class="chip-row">
                <span class="chip chip-green">{total_rev} Revenue</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Finance Summary →",
                     use_container_width=True, key="nav_finance"):
            nav_to("Finance Summary")

    with col3:
        st.markdown(f"""
        <div class="card card-health">
            <div class="card-title"> Client Health & Advocacy</div>
            <div class="card-desc">
                Monitor client health scores and referenceability
                status across all accounts. Track changes and
                review notes over time.
            </div>
            <div class="chip-row">
                <span class="chip chip-green">🟢 {green}</span>
                <span class="chip chip-amber">🟡 {amber}</span>
                <span class="chip chip-red">🔴 {red}</span>
                <span class="chip chip-amber">{ref} Referenceable</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Client Health →",
                     use_container_width=True, key="nav_health"):
            nav_to("Client Health")

    with col4:
        st.markdown(f"""
        <div class="card card-golives">
            <div class="card-title"> Go-Lives</div>
            <div class="card-desc">
                Track project deployments, go-live dates,
                delivery status and duration variance
                across all customer projects.
            </div>
            <div class="chip-row">
                <span class="chip chip-purple">{total_proj} Projects</span>
                <span class="chip chip-green">{on_time} On Time</span>
                <span class="chip chip-red">{delayed} Delayed</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Go-Lives →",
                     use_container_width=True, key="nav_golives"):
            nav_to("Go-Lives")

    st.divider()
    st.markdown(
        '<div style="opacity:0.45; font-size:0.82rem;">o9 Solutions · RDAF Team</div>',
        unsafe_allow_html=True
    )

elif st.session_state.page == "Account Summary":
    account_summary.show(df_customer, df_projects)

elif st.session_state.page == "Finance Summary":
    finance.show()

elif st.session_state.page == "Client Health":
    client_health.show()

elif st.session_state.page == "Go-Lives":
    go_lives.show()