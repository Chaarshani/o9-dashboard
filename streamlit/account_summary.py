import streamlit as st
import pandas as pd

BLUE = "#3b82f6"
GREEN = "#10b981"
AMBER = "#f59e0b"
RED = "#ef4444"
GRAY = "#6b7280"


def inject_styles():
    st.markdown("""
    <style>
    .metric-card {
        background: var(--secondary-background-color);
        border-radius: 14px;
        padding: 16px;
        border: 1px solid rgba(127,127,127,0.16);
        border-left: 4px solid #3b82f6;
        min-height: 92px;
    }
    .metric-title {
        font-size: 11px;
        font-weight: 800;
        opacity: 0.72;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 900;
    }
    .status-card {
        background: var(--secondary-background-color);
        border-radius: 16px;
        padding: 18px;
        border: 1px solid rgba(127,127,127,0.16);
        height: 100%;
    }
    .status-pill {
        padding: 12px 14px;
        border-radius: 12px;
        color: white;
        font-weight: 800;
        font-size: 14px;
        text-align: center;
        width: 100%;
        box-sizing: border-box;
    }
    </style>
    """, unsafe_allow_html=True)


def money(x):
    try:
        return f"${float(x):,.0f}"
    except Exception:
        return "$0"


def pct(x):
    try:
        return f"{float(x):.1f}%"
    except Exception:
        return "N/A"


def safe_numeric(series):
    return pd.to_numeric(series, errors="coerce")


def normalize_filter_options(values):
    vals = [v for v in values if pd.notna(v) and str(v).strip()]
    vals = sorted(pd.unique(vals).tolist())
    return ["All"] + vals


def apply_multi_filter(df, column, selected):
    if column not in df.columns:
        return df
    if not selected or "All" in selected:
        return df
    return df[df[column].isin(selected)]


def health_pill(value):
    text = str(value).strip().title()
    color_map = {
        "Green": GREEN,
        "Amber": AMBER,
        "Red": RED,
    }
    label = text.upper() if text in {"Green", "Amber", "Red"} else "UNKNOWN"
    color = color_map.get(text, GRAY)
    return f'<div class="status-pill" style="background:{color};">{label}</div>'


def advocacy_pill(value):
    text = str(value).strip().lower()
    if text == "yes":
        label, color = "YES", GREEN
    elif text == "yes with caution":
        label, color = "YES WITH CAUTION", AMBER
    elif text in {"not referenceable", "no"}:
        label, color = "NOT REFERENCEABLE", RED
    else:
        label, color = "UNKNOWN", GRAY
    return f'<div class="status-pill" style="background:{color};">{label}</div>'


def metric_card(title, value, border_color=BLUE, value_color=BLUE):
    return f"""
    <div class="metric-card" style="border-left-color:{border_color};">
        <div class="metric-title">{title}</div>
        <div class="metric-value" style="color:{value_color};">{value}</div>
    </div>
    """


def format_table(df, money_cols=None, pct_cols=None, date_cols=None):
    out = df.copy()
    money_cols = money_cols or []
    pct_cols = pct_cols or []
    date_cols = date_cols or []

    for col in money_cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0).map(lambda x: f"${x:,.0f}")

    for col in pct_cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").map(
                lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A"
            )

    for col in date_cols:
        if col in out.columns:
            out[col] = pd.to_datetime(out[col], errors="coerce").dt.strftime("%Y-%m-%d")

    return out


def show(df_customer, df_projects):
    inject_styles()

    st.markdown("## Account Summary")
    st.markdown("Select a customer and month-year to view the consolidated account profile.")
    st.divider()

    if df_customer is None or df_customer.empty:
        st.warning("No customer summary data available.")
        return

    df_customer = df_customer.copy()
    df_projects = df_projects.copy() if df_projects is not None else pd.DataFrame()

    numeric_cols_customer = [
        "total_revenue", "total_fac_cost", "total_eac_cost", "gross_margin_fac",
        "margin_pct_fac", "services_revenue", "saas_revenue",
        "services_fac", "cs_fac", "hosting_cost_fac", "saas_fac", "devops_cost",
        "services_eac", "cs_eac", "hosting_cost_eac", "saas_eac",
        "client_health_score"
    ]
    for col in numeric_cols_customer:
        if col in df_customer.columns:
            df_customer[col] = safe_numeric(df_customer[col])

    for col in ["duration_original", "duration_actual", "duration_variance"]:
        if col in df_projects.columns:
            df_projects[col] = safe_numeric(df_projects[col])

    if {"year", "month_num"}.issubset(df_customer.columns):
        df_customer = df_customer.sort_values(["year", "month_num"])

    # Filters
    f1, f2, f3 = st.columns([2, 2, 2])

    with f1:
        customer_options = normalize_filter_options(df_customer["customer_name"].dropna().unique())
        selected_customer = st.selectbox("Customer", customer_options)

    with f2:
        month_year_options = normalize_filter_options(
            df_customer["year_month"].dropna().astype(str).unique()
        ) if "year_month" in df_customer.columns else ["All"]
        selected_month_year = st.multiselect(
            "Month-Year",
            month_year_options,
            default=["All"]
        )

    with f3:
        portfolio_options = normalize_filter_options(
            df_customer["portfolio"].dropna().unique()
        ) if "portfolio" in df_customer.columns else ["All"]
        selected_portfolio = st.multiselect(
            "Portfolio",
            portfolio_options,
            default=["All"]
        )

    # Apply filters
    df = df_customer.copy()
    df_proj = df_projects.copy()

    if selected_customer != "All":
        df = df[df["customer_name"] == selected_customer]
        if not df_proj.empty and "customer_name" in df_proj.columns:
            df_proj = df_proj[df_proj["customer_name"] == selected_customer]

    df = apply_multi_filter(df, "year_month", selected_month_year)
    df = apply_multi_filter(df, "portfolio", selected_portfolio)

    if not df_proj.empty and "portfolio" in df_proj.columns:
        df_proj = apply_multi_filter(df_proj, "portfolio", selected_portfolio)

    if df.empty:
        st.warning("No data found for selected filters.")
        return

    latest = df.iloc[-1]

    # Header
    st.markdown(f"""
    <div style="
        background:var(--secondary-background-color);
        border-radius:16px;
        padding:20px 24px;
        border-left:5px solid {BLUE};
        margin-bottom:18px;">
        <div style="font-size:1.7rem;font-weight:900;">
            {latest.get('customer_name', '—')}
        </div>
        <div style="opacity:0.7;font-size:0.95rem;margin-top:6px;">
            Portfolio: <b>{latest.get('portfolio', '—')}</b> &nbsp;|&nbsp;
            Client Manager: <b>{latest.get('client_manager', '—')}</b> &nbsp;|&nbsp;
            Parent: <b>{latest.get('parent_name', '—')}</b> &nbsp;|&nbsp;
            Status: <b>{latest.get('customer_status', '—')}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Top cards
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        st.markdown("### Client Health")
        st.markdown(health_pill(latest.get("client_health_std", "Unknown")), unsafe_allow_html=True)
        if pd.notna(latest.get("client_health_score", None)):
            st.caption(f"Score: {latest.get('client_health_score')}")
        if pd.notna(latest.get("health_notes", None)) and str(latest.get("health_notes")).strip():
            st.caption(f"Notes: {latest.get('health_notes')}")
        if pd.notna(latest.get("health_last_review_date", None)):
            st.caption(f"Last Reviewed: {latest.get('health_last_review_date')}")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        st.markdown("### Advocacy")
        st.markdown(advocacy_pill(latest.get("referenceability", "Unknown")), unsafe_allow_html=True)
        if pd.notna(latest.get("advocacy_reason", None)) and str(latest.get("advocacy_reason")).strip():
            st.caption(f"Reason: {latest.get('advocacy_reason')}")
        if pd.notna(latest.get("advocacy_last_review_date", None)):
            st.caption(f"Last Reviewed: {latest.get('advocacy_last_review_date')}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # Financial Summary
    st.markdown("### Financial Summary")
    basis = st.radio("Cost Basis", ["FAC", "EAC"], horizontal=True, index=0)

    total_revenue = df["total_revenue"].sum() if "total_revenue" in df.columns else 0

    if basis == "FAC":
        total_cost = df["total_fac_cost"].sum() if "total_fac_cost" in df.columns else 0
        gross_margin = df["gross_margin_fac"].sum() if "gross_margin_fac" in df.columns else total_revenue - total_cost
        avg_margin = df["margin_pct_fac"].mean() if "margin_pct_fac" in df.columns else None

        services_cost = df["services_fac"].sum() if "services_fac" in df.columns else 0
        saas_cost = df["saas_fac"].sum() if "saas_fac" in df.columns else 0
        hosting_cost = df["hosting_cost_fac"].sum() if "hosting_cost_fac" in df.columns else 0
        cs_cost = df["cs_fac"].sum() if "cs_fac" in df.columns else 0
        devops_cost = df["devops_cost"].sum() if "devops_cost" in df.columns else 0
    else:
        total_cost = df["total_eac_cost"].sum() if "total_eac_cost" in df.columns else 0
        gross_margin = total_revenue - total_cost
        avg_margin = (gross_margin / total_revenue * 100) if total_revenue else None

        services_cost = df["services_eac"].sum() if "services_eac" in df.columns else 0
        saas_cost = df["saas_eac"].sum() if "saas_eac" in df.columns else 0
        hosting_cost = df["hosting_cost_eac"].sum() if "hosting_cost_eac" in df.columns else 0
        cs_cost = df["cs_eac"].sum() if "cs_eac" in df.columns else 0
        devops_cost = df["devops_cost"].sum() if "devops_cost" in df.columns else 0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(metric_card("Total Revenue", money(total_revenue), BLUE, BLUE), unsafe_allow_html=True)
    with k2:
        st.markdown(
            metric_card(
                f"Total {basis} Cost",
                money(total_cost),
                RED if basis == "FAC" else AMBER,
                RED if basis == "FAC" else AMBER
            ),
            unsafe_allow_html=True
        )
    with k3:
        st.markdown(metric_card(f"Gross Margin {basis}", money(gross_margin), GREEN, GREEN), unsafe_allow_html=True)
    with k4:
        st.markdown(metric_card(f"Avg Margin % {basis}", pct(avg_margin) if avg_margin is not None else "N/A", BLUE, BLUE), unsafe_allow_html=True)

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    # Services row
    st.markdown("#### Services")
    services_revenue = df["services_revenue"].sum() if "services_revenue" in df.columns else 0
    services_gm = services_revenue - services_cost
    services_gm_pct = (services_gm / services_revenue * 100) if services_revenue else None

    srv1, srv2, srv3, srv4 = st.columns(4)
    with srv1:
        st.markdown(metric_card("Revenue", money(services_revenue), BLUE, BLUE), unsafe_allow_html=True)
    with srv2:
        st.markdown(
            metric_card(
                f"Cost ({basis})",
                money(services_cost),
                RED if basis == "FAC" else AMBER,
                RED if basis == "FAC" else AMBER
            ),
            unsafe_allow_html=True
        )
    with srv3:
        st.markdown(metric_card(f"GM ({basis})", money(services_gm), GREEN, GREEN), unsafe_allow_html=True)
    with srv4:
        st.markdown(metric_card(f"GM % ({basis})", pct(services_gm_pct) if services_gm_pct is not None else "N/A", BLUE, BLUE), unsafe_allow_html=True)

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    # SaaS row
    st.markdown("#### SaaS")
    saas_revenue = df["saas_revenue"].sum() if "saas_revenue" in df.columns else 0
    saas_gm = saas_revenue - saas_cost
    saas_gm_pct = (saas_gm / saas_revenue * 100) if saas_revenue else None

    sa1, sa2, sa3, sa4 = st.columns(4)
    with sa1:
        st.markdown(metric_card("Revenue", money(saas_revenue), BLUE, BLUE), unsafe_allow_html=True)
    with sa2:
        st.markdown(
            metric_card(
                f"Cost ({basis})",
                money(saas_cost),
                RED if basis == "FAC" else AMBER,
                RED if basis == "FAC" else AMBER
            ),
            unsafe_allow_html=True
        )
    with sa3:
        st.markdown(metric_card(f"GM ({basis})", money(saas_gm), GREEN, GREEN), unsafe_allow_html=True)
    with sa4:
        st.markdown(metric_card(f"GM % ({basis})", pct(saas_gm_pct) if saas_gm_pct is not None else "N/A", BLUE, BLUE), unsafe_allow_html=True)

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # SaaS components row
    st.markdown("**SaaS Cost Components**")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(metric_card("Hosting", money(hosting_cost), AMBER, AMBER), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("CS", money(cs_cost), AMBER, AMBER), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("DevOps", money(devops_cost), AMBER, AMBER), unsafe_allow_html=True)

    st.divider()

    # Go-Lives
    st.markdown("### Go-Lives")
    if df_proj.empty:
        st.info("No project / go-live data available for this customer.")
    else:
        p1, p2, p3, p4 = st.columns(4)
        with p1:
            st.metric("Total Projects", df_proj["project_sk"].nunique() if "project_sk" in df_proj.columns else len(df_proj))
        with p2:
            st.metric("On Time", int((df_proj["delivery_status"] == "On Time").sum()) if "delivery_status" in df_proj.columns else 0)
        with p3:
            st.metric("Delayed", int((df_proj["delivery_status"] == "Delayed").sum()) if "delivery_status" in df_proj.columns else 0)
        with p4:
            avg_var = df_proj["duration_variance"].mean() if "duration_variance" in df_proj.columns else None
            st.metric("Avg Variance", f"{avg_var:.1f}" if avg_var is not None and pd.notna(avg_var) else "N/A")

        proj_cols = [
            c for c in [
                "project",
                "project_type",
                "release",
                "solution",
                "current_phase",
                "release_type",
                "go_live_original",
                "actual_go_live",
                "duration_original",
                "duration_actual",
                "duration_variance",
                "delivery_status",
                "delays",
                "ttv"
            ] if c in df_proj.columns
        ]

        proj_display = df_proj[proj_cols].rename(columns={
            "project": "Project",
            "project_type": "Project Type",
            "release": "Release",
            "solution": "Solution",
            "current_phase": "Current Phase",
            "release_type": "Release Type",
            "go_live_original": "Original Go-Live",
            "actual_go_live": "Actual Go-Live",
            "duration_original": "Original Duration",
            "duration_actual": "Actual Duration",
            "duration_variance": "Duration Variance",
            "delivery_status": "Delivery Status",
            "delays": "Delays",
            "ttv": "TTV",
        })

        proj_display = format_table(
            proj_display,
            date_cols=["Original Go-Live", "Actual Go-Live"]
        )
        st.dataframe(proj_display, use_container_width=True, hide_index=True)