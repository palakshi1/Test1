"""
╔══════════════════════════════════════════════════════════════════════════╗
║   DataVizor BI  —  AI-Powered Power BI Dashboard Generator              ║
║   Single-file Streamlit application                                      ║
║   Run:  streamlit run app.py                                             ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

# ── Standard library ───────────────────────────────────────────────────────
import io
import json
import time
import zipfile
from datetime import datetime
from typing import Optional

# ── Third-party ────────────────────────────────────────────────────────────
import pandas as pd
import streamlit as st


# ══════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION  (must be first Streamlit call)
# ══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="DataVizor BI",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ══════════════════════════════════════════════════════════════════════════
# GLOBAL STYLES
# ══════════════════════════════════════════════════════════════════════════
STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --blue-700:  #1D4ED8;
    --blue-600:  #2563EB;
    --blue-100:  #DBEAFE;
    --blue-50:   #EFF6FF;
    --slate-900: #0F172A;
    --slate-800: #1E293B;
    --slate-600: #475569;
    --slate-400: #94A3B8;
    --slate-200: #E2E8F0;
    --slate-100: #F1F5F9;
    --slate-50:  #F8FAFC;
    --white:     #FFFFFF;
    --green-100: #DCFCE7;
    --green-700: #15803D;
    --amber-100: #FEF3C7;
    --amber-700: #B45309;
    --red-100:   #FEE2E2;
    --red-700:   #B91C1C;
    --radius:    10px;
    --radius-lg: 16px;
    --shadow-sm: 0 1px 2px rgba(0,0,0,.06);
    --shadow:    0 1px 3px rgba(0,0,0,.10), 0 1px 2px rgba(0,0,0,.06);
}

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
    color: var(--slate-800);
}
.stApp { background: var(--slate-50); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: .75rem !important; padding-bottom: 2rem !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1px solid var(--slate-200);
}
section[data-testid="stSidebar"] .block-container { padding-top: .5rem; }

/* App header */
.app-header {
    background: var(--white);
    border-bottom: 1px solid var(--slate-200);
    border-radius: 0 0 var(--radius-lg) var(--radius-lg);
    padding: 18px 32px 16px;
    margin-bottom: 16px;
    box-shadow: var(--shadow-sm);
    display: flex;
    align-items: center;
    gap: 16px;
}
.app-header .brand-icon {
    width: 44px; height: 44px;
    background: var(--blue-600);
    border-radius: var(--radius);
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.app-header .brand-icon svg { width: 24px; height: 24px; }
.app-header h1 {
    margin: 0; font-size: 21px; font-weight: 800;
    color: var(--blue-700); letter-spacing: -.4px;
}
.app-header p { margin: 0; font-size: 12.5px; color: var(--slate-400); }

/* Empty state */
.empty-state {
    text-align: center;
    padding: 72px 20px;
}
.empty-state .es-icon {
    width: 64px; height: 64px;
    background: var(--blue-50);
    border-radius: var(--radius-lg);
    display: inline-flex; align-items: center; justify-content: center;
    margin-bottom: 18px;
    border: 1px solid var(--blue-100);
}
.empty-state .es-icon svg { width: 32px; height: 32px; }
.empty-state h2 { font-size: 20px; font-weight: 700; color: var(--slate-600); margin: 0 0 6px; }
.empty-state p  { font-size: 14px; color: var(--slate-400); margin: 0; }

/* Chat */
.chat-wrapper {
    max-width: 820px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
    padding: 4px 4px 20px;
}
.msg-row { display: flex; align-items: flex-start; gap: 10px; }
.msg-row.user { flex-direction: row-reverse; }

.avatar {
    width: 34px; height: 34px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    font-size: 10px; font-weight: 700; letter-spacing: .4px;
    color: #fff;
}
.avatar.user { background: var(--blue-600); }
.avatar.bot  { background: linear-gradient(135deg, var(--blue-700), #0EA5E9); }

.bubble {
    max-width: 78%;
    padding: 13px 17px;
    border-radius: var(--radius-lg);
    font-size: 14px;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-word;
    box-shadow: var(--shadow-sm);
}
.bubble.user {
    background: var(--blue-600);
    color: #fff;
    border-bottom-right-radius: 4px;
}
.bubble.bot {
    background: var(--white);
    border: 1px solid var(--slate-200);
    color: var(--slate-800);
    border-bottom-left-radius: 4px;
}
.bubble code {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px;
    background: var(--slate-100);
    border-radius: 4px;
    padding: 1px 5px;
    color: var(--blue-700);
}

/* Typing cursor */
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
.cursor {
    display: inline-block; width: 2px; height: .9em;
    background: var(--blue-600); margin-left: 2px;
    animation: blink 900ms step-start infinite;
    vertical-align: text-bottom;
}

/* Sidebar label */
.sb-label {
    font-size: 10px; font-weight: 700; letter-spacing: 1px;
    text-transform: uppercase; color: var(--slate-400);
    margin: 12px 0 6px;
}

/* Alert boxes */
.alert {
    border-radius: var(--radius);
    padding: 10px 14px;
    font-size: 13px;
    line-height: 1.55;
    margin: 8px 0;
}
.alert.warning { background: var(--amber-100); border: 1px solid #FCD34D; color: var(--amber-700); }
.alert.error   { background: var(--red-100);   border: 1px solid #FCA5A5; color: var(--red-700); }
.alert.success { background: var(--green-100); border: 1px solid #86EFAC; color: var(--green-700); }
.alert .alert-title { font-weight: 700; margin-bottom: 3px; }
.alert .alert-mono {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11.5px;
    background: rgba(0,0,0,.07);
    border-radius: 4px;
    padding: 2px 7px;
    display: inline-block;
    margin-top: 4px;
}

.hr { border: none; border-top: 1px solid var(--slate-200); margin: 10px 0; }

/* Notice bar */
.pbix-notice {
    background: var(--blue-50);
    border: 1px solid var(--blue-100);
    border-radius: var(--radius);
    padding: 9px 14px;
    font-size: 12.5px;
    color: var(--blue-700);
    margin-top: 6px;
}

/* Button overrides */
.stButton > button {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    border-radius: var(--radius) !important;
    transition: all .15s ease !important;
}
</style>
"""
st.markdown(STYLES, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# SVG ICONS  (inline, no external dependencies)
# ══════════════════════════════════════════════════════════════════════════
ICON_CHART = """
<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"
     stroke="#fff" stroke-width="2" stroke-linecap="round"
     stroke-linejoin="round" fill="none">
  <rect x="3"  y="12" width="4" height="9" rx="1"/>
  <rect x="10" y="7"  width="4" height="14" rx="1"/>
  <rect x="17" y="3"  width="4" height="18" rx="1"/>
</svg>"""

ICON_CHART_BLUE = """
<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"
     stroke="#2563EB" stroke-width="2" stroke-linecap="round"
     stroke-linejoin="round" fill="none">
  <rect x="3"  y="12" width="4" height="9" rx="1"/>
  <rect x="10" y="7"  width="4" height="14" rx="1"/>
  <rect x="17" y="3"  width="4" height="18" rx="1"/>
</svg>"""


# ══════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════
AI_NAME    = "DataVizor BI"
AI_TAGLINE = "Transforming raw data into executive-ready Power BI insights."

EXAMPLE_PROMPTS = [
    "Create a Sales Performance Dashboard",
    "Build a Finance KPI Dashboard with YoY Growth",
    "Design a Regional Sales Breakdown Report",
    "Generate an HR Headcount and Attrition Dashboard",
    "Build an Inventory and Supply Chain Report",
    "Create an E-Commerce Funnel Analytics Dashboard",
]

DOMAIN_KPIS = {
    "sales"    : ["Total Revenue", "Gross Profit", "Units Sold", "Profit Margin %", "YoY Growth %"],
    "finance"  : ["Net Revenue", "EBITDA", "Net Profit", "Operating Cost", "Budget Variance"],
    "hr"       : ["Total Headcount", "Attrition Rate", "New Hires", "Avg Tenure (Yrs)", "Open Positions"],
    "inventory": ["Total SKUs", "Stockout Rate %", "Reorder Items", "Avg Lead Time", "Inventory Value"],
    "ecommerce": ["Total Orders", "Conversion Rate", "Avg Order Value", "Cart Abandonment %", "Revenue"],
    "regional" : ["Total Regions", "Top Region Revenue", "Growth %", "Market Coverage", "Net Sales"],
}


# ══════════════════════════════════════════════════════════════════════════
# SESSION STATE BOOTSTRAP
# ══════════════════════════════════════════════════════════════════════════
_DEFAULTS: dict = {
    "messages"       : [],
    "df"             : None,
    "file_name"      : None,
    "col_types"      : {},
    "input_key"      : 0,
    "pending_prompt" : None,
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ══════════════════════════════════════════════════════════════════════════
# FILE LOADING — robust multi-format, graceful error messages
# ══════════════════════════════════════════════════════════════════════════
def load_file(uploaded_file) -> tuple:
    """
    Load an uploaded file into a DataFrame.
    Returns (DataFrame | None, error_message | None).
    Never raises — all errors are caught and returned as clean messages.
    """
    name = uploaded_file.name.lower()
    raw  = uploaded_file.read()

    # ── CSV ──────────────────────────────────────────────────────────────
    if name.endswith(".csv"):
        try:
            return pd.read_csv(io.BytesIO(raw)), None
        except Exception as exc:
            return None, ("csv_parse", str(exc))

    # ── Excel ─────────────────────────────────────────────────────────────
    if name.endswith((".xlsx", ".xls")):
        is_xlsx = name.endswith(".xlsx")
        engine  = "openpyxl" if is_xlsx else "xlrd"
        pkg     = "openpyxl" if is_xlsx else "xlrd"
        fmt     = "Excel (.xlsx)" if is_xlsx else "Legacy Excel (.xls)"

        try:
            if engine == "openpyxl":
                import openpyxl  # noqa: F401
            else:
                import xlrd      # noqa: F401
        except ImportError:
            return None, ("missing_pkg", pkg, fmt)

        try:
            return pd.read_excel(io.BytesIO(raw), engine=engine), None
        except Exception as exc:
            return None, ("excel_parse", str(exc))

    # ── JSON ──────────────────────────────────────────────────────────────
    if name.endswith(".json"):
        try:
            data = json.loads(raw)
            df   = pd.DataFrame(data) if isinstance(data, list) \
                   else pd.DataFrame.from_dict(data)
            return df, None
        except Exception as exc:
            return None, ("json_parse", str(exc))

    return None, ("unsupported",)


def render_file_error(err_tuple: tuple):
    """
    Display a styled, readable error message for file-load failures.
    Replaces raw red Streamlit error blocks.
    """
    kind = err_tuple[0]

    if kind == "missing_pkg":
        _, pkg, fmt = err_tuple
        st.markdown(
            f"""
            <div class="alert error">
                <div class="alert-title">Missing dependency — {fmt}</div>
                The Python package <span class="alert-mono">{pkg}</span>
                is required to open this file but is not installed.<br><br>
                Run this command in your terminal, then restart the app:<br>
                <span class="alert-mono">pip install {pkg}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif kind in ("csv_parse", "excel_parse", "json_parse"):
        detail = err_tuple[1]
        label  = {"csv_parse": "CSV", "excel_parse": "Excel",
                  "json_parse": "JSON"}[kind]
        st.markdown(
            f"""
            <div class="alert error">
                <div class="alert-title">Could not parse {label} file</div>
                The file may be corrupted or in an unexpected format.<br>
                <span class="alert-mono">{detail[:120]}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        st.markdown(
            """
            <div class="alert warning">
                <div class="alert-title">Unsupported file format</div>
                Please upload a <span class="alert-mono">.csv</span>,
                <span class="alert-mono">.xlsx</span>,
                <span class="alert-mono">.xls</span>, or
                <span class="alert-mono">.json</span> file.
            </div>
            """,
            unsafe_allow_html=True,
        )


def classify_columns(df: pd.DataFrame) -> dict:
    """Classify DataFrame columns into numeric / categorical / date."""
    result: dict = {"numeric": [], "categorical": [], "date": []}
    for col in df.columns:
        dtype = df[col].dtype
        if pd.api.types.is_numeric_dtype(dtype):
            result["numeric"].append(col)
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            result["date"].append(col)
        else:
            try:
                parsed    = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")
                null_frac = parsed.isna().mean()
                if null_frac < 0.35:
                    result["date"].append(col)
                    continue
            except Exception:
                pass
            result["categorical"].append(col)
    return result


# ══════════════════════════════════════════════════════════════════════════
# DASHBOARD GENERATION ENGINE
# ══════════════════════════════════════════════════════════════════════════
def detect_domain(prompt: str) -> str:
    p = prompt.lower()
    keyword_map = {
        "finance": ["finance", "revenue", "profit", "budget", "ebitda", "cash flow"],
        "hr"     : ["hr", "human resource", "employee", "headcount", "attrition", "hire"],
        "inventory": ["inventory", "stock", "sku", "supply chain", "warehouse", "reorder"],
        "ecommerce": ["ecommerce", "e-commerce", "cart", "order", "conversion", "funnel"],
        "regional" : ["regional", "region", "territory", "market", "geography"],
        "sales"    : ["sales", "revenue", "units", "deal", "pipeline"],
    }
    for domain, keywords in keyword_map.items():
        if any(kw in p for kw in keywords):
            return domain
    return "sales"


def pick_visuals(col_types: dict, domain: str) -> list:
    nums  = col_types.get("numeric", [])
    cats  = col_types.get("categorical", [])
    dates = col_types.get("date", [])
    vs    = []

    if dates and nums:
        vs.append(f"Line Chart   : {dates[0]} vs {nums[0]}  (trend over time)")
    if cats and nums:
        vs.append(f"Bar Chart    : {cats[0]} vs {nums[0]}  (comparison)")
    if len(cats) >= 2 and nums:
        vs.append(f"Stacked Bar  : {cats[0]} stacked by {cats[1]}")
    if nums:
        vs.append(f"KPI Cards    : {', '.join(nums[:4])}")
    if cats and nums:
        vs.append(f"Donut Chart  : {cats[0]} share of {nums[0]}")
    if len(nums) >= 2:
        vs.append(f"Scatter Plot : {nums[0]} vs {nums[1]}")
    if any("region" in c.lower() for c in cats):
        vs.append("Filled Map   : Regional revenue distribution")

    if not vs:
        fallback = {
            "sales"    : ["Line Chart: Date vs Revenue", "Bar Chart: Region vs Sales",
                          "KPI Cards: Revenue, Profit, Units", "Donut: Category split"],
            "finance"  : ["Waterfall: Revenue to EBITDA", "Bar: Budget vs Actual by Dept",
                          "Line: Monthly Cash Flow", "KPI: Net Profit Margin"],
            "hr"       : ["Bar: Headcount by Department", "Line: Monthly Attrition",
                          "Donut: Dept distribution", "KPI: Headcount, Attrition %"],
            "inventory": ["Line: Stock Level Over Time", "Bar: SKU vs Stock Count",
                          "Gauge: Stockout Rate", "Table: Reorder Alerts"],
            "ecommerce": ["Funnel: Sessions > Cart > Purchase", "Line: Daily Orders",
                          "Bar: Top 10 Products", "KPI: CVR, AOV, Revenue"],
            "regional" : ["Filled Map: Sales by Region", "Bar: Top 10 Territories",
                          "Line: Region Growth Trend", "KPI: Active Markets"],
        }
        vs = fallback.get(domain, fallback["sales"])
    return vs


def build_dax_measures(col_types: dict, domain: str) -> list:
    nums  = col_types.get("numeric", [])
    dates = col_types.get("date", [])
    tbl   = "Data"
    dax   = []

    if nums:
        n = nums[0]
        dax += [
            f"Total {n} = SUM({tbl}[{n}])",
            f"Avg {n} = AVERAGE({tbl}[{n}])",
        ]
        if len(nums) >= 2:
            n2 = nums[1]
            dax.append(
                f"{n} Margin % = DIVIDE([Total {n}] - [Total {n2}], [Total {n}], 0)"
            )
    if dates and nums:
        n = nums[0]; d = dates[0]
        dax += [
            f"YoY Growth % = DIVIDE(\n"
            f"    [Total {n}] - CALCULATE([Total {n}], SAMEPERIODLASTYEAR({tbl}[{d}])),\n"
            f"    CALCULATE([Total {n}], SAMEPERIODLASTYEAR({tbl}[{d}])), 0)",
            f"MTD {n} = TOTALMTD([Total {n}], {tbl}[{d}])",
            f"QTD {n} = TOTALQTD([Total {n}], {tbl}[{d}])",
            f"YTD {n} = TOTALYTD([Total {n}], {tbl}[{d}])",
        ]

    if not dax:
        fallback = {
            "sales"  : [
                "Total Sales = SUM(Sales[Amount])",
                "Gross Profit = [Total Sales] - SUM(Sales[Cost])",
                "Profit Margin % = DIVIDE([Gross Profit], [Total Sales], 0)",
                "YoY Growth % = DIVIDE([Total Sales] - CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Calendar[Date])), CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Calendar[Date])), 0)",
                "MTD Sales = TOTALMTD([Total Sales], Calendar[Date])",
            ],
            "finance": [
                "Net Revenue = SUM(Finance[Revenue])",
                "EBITDA Margin = DIVIDE([EBITDA], [Net Revenue], 0)",
                "Budget Variance = [Actual] - [Budget]",
                "Variance % = DIVIDE([Budget Variance], [Budget], 0)",
            ],
            "hr"     : [
                "Total Headcount = COUNTROWS(Employees)",
                "Attrition Rate = DIVIDE([Exits], [Total Headcount], 0)",
                "Avg Tenure Yrs = AVERAGE(Employees[Tenure_Years])",
                "New Hires = CALCULATE([Total Headcount], Employees[Status] = \"New\")",
            ],
        }
        dax = fallback.get(domain, fallback["sales"])
    return dax


def build_schema(col_types: dict, domain: str) -> list:
    nums  = col_types.get("numeric", [])
    cats  = col_types.get("categorical", [])
    dates = col_types.get("date", [])
    tables = []

    if nums or cats or dates:
        cols_str = ", ".join((nums + cats + dates)[:7])
        tables.append(f"FactData ({cols_str})")
    else:
        fallback = {
            "sales"  : ["FactSales (Date, ProductKey, CustomerKey, Amount, Qty, Discount)",
                        "DimProduct (ProductKey, Name, Category, Brand)",
                        "DimCustomer (CustomerKey, Name, Region, Segment)"],
            "finance": ["FactFinance (Date, DeptKey, Revenue, Cost, Budget)",
                        "DimDepartment (DeptKey, Name, CostCenter, Manager)"],
            "hr"     : ["FactHR (EmployeeKey, Date, Status, Salary)",
                        "DimEmployee (EmployeeKey, Name, Dept, Grade, StartDate)"],
        }
        tables = fallback.get(domain, fallback["sales"])

    if dates:
        tables.append(f"DimDate ({dates[0]}, Month, Quarter, Year, IsWeekend)")
    elif not any("Date" in t for t in tables):
        tables.append("DimDate (Date, Month, Quarter, Year, FiscalYear)")
    return tables


def generate_response(prompt: str,
                       df: Optional[pd.DataFrame],
                       col_types: dict) -> str:
    """
    Rule-based dashboard generation engine.
    INTEGRATION POINT: replace body with OpenAI / Anthropic API call
    to upgrade to fully LLM-powered generation.
    """
    domain  = detect_domain(prompt)
    title   = (prompt.strip().title()
                if len(prompt) < 55
                else f"{domain.title()} Performance Dashboard")

    kpis    = DOMAIN_KPIS.get(domain, DOMAIN_KPIS["sales"])
    visuals = pick_visuals(col_types, domain)
    schema  = build_schema(col_types, domain)
    dax     = build_dax_measures(col_types, domain)

    data_note = ""
    if df is not None:
        r, c = df.shape
        data_note = (
            f"\nData context: {r:,} rows x {c} columns "
            f"-- visuals and DAX are tailored to your uploaded dataset.\n"
        )

    layout = (
        "Row 1  :  KPI Summary Cards (full width, 4-5 cards)\n"
        "Row 2  :  Primary trend visual [60%]  |  Donut / Pie [40%]\n"
        "Row 3  :  Categorical bar chart [50%]  |  Detail table [50%]\n"
        "Filters:  Date range slicer, Category dropdown, Region slicer"
    )

    lines = [
        f"Dashboard Title: {title}",
        data_note,
        "-" * 50,
        "",
        "1. Key Metrics (KPI Cards)",
        *[f"   - {k}" for k in kpis],
        "",
        "-" * 50,
        "",
        "2. Recommended Visuals",
        *[f"   - {v}" for v in visuals],
        "",
        "-" * 50,
        "",
        "3. Data Model -- Table Schema",
        *[f"   - {s}" for s in schema],
        "",
        "-" * 50,
        "",
        "4. DAX Measures",
        *[f"   {m}" for m in dax],
        "",
        "-" * 50,
        "",
        "5. Dashboard Layout",
        f"   {layout}",
        "",
        "-" * 50,
        "",
        "Power BI Setup Tips",
        "   - Import data via Get Data > Excel / CSV",
        "   - Create DimDate with CALENDARAUTO() and mark as date table",
        "   - Enable Row-level Security for regional or role-based access",
        "   - Use Bookmarks for executive summary toggle views",
        "",
        "Note: Direct .pbix export is simulated via structured templates.",
        "      Use the export buttons below to download your dashboard package.",
    ]
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════
# EXPORT BUILDERS
# ══════════════════════════════════════════════════════════════════════════
def compile_dax(messages: list) -> str:
    lines = [
        f"// DAX Measures -- {AI_NAME}",
        f"// Generated: {datetime.now():%Y-%m-%d %H:%M}",
        "",
    ]
    for m in messages:
        if m["role"] != "assistant" or "4. DAX Measures" not in m["content"]:
            continue
        capture = False
        for line in m["content"].splitlines():
            if "4. DAX Measures" in line:
                capture = True; continue
            if capture:
                if line.startswith("-" * 10) or line.startswith("5."):
                    break
                stripped = line.strip()
                if stripped:
                    lines.append(stripped)
    return "\n".join(lines)


def compile_json_spec(messages: list,
                      df: Optional[pd.DataFrame],
                      col_types: dict) -> str:
    last_bot = next(
        (m["content"] for m in reversed(messages) if m["role"] == "assistant"), ""
    )
    ds = "No dataset uploaded"
    if df is not None:
        r, c = df.shape
        ds   = (
            f"{r:,} rows x {c} columns | "
            f"Numeric: {', '.join(col_types.get('numeric', []))} | "
            f"Categorical: {', '.join(col_types.get('categorical', []))} | "
            f"Date: {', '.join(col_types.get('date', []))}"
        )
    spec = {
        "tool"           : AI_NAME,
        "generated_at"   : datetime.now().isoformat(),
        "disclaimer"     : "Direct .pbix generation is simulated. Use this spec in Power BI Desktop.",
        "dashboard_spec" : last_bot,
        "dataset_summary": ds,
    }
    return json.dumps(spec, indent=2, ensure_ascii=False)


def build_zip(messages: list,
              df: Optional[pd.DataFrame],
              col_types: dict) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        transcript = "\n\n".join(
            f"[{m['role'].upper()}]\n{m['content']}" for m in messages
        )
        zf.writestr("chat_transcript.txt", transcript)
        zf.writestr("dax_measures.dax",    compile_dax(messages))
        zf.writestr("dashboard_spec.json", compile_json_spec(messages, df, col_types))
        zf.writestr("README.txt", (
            f"{AI_NAME} -- Export Package\n"
            "=" * 40 + "\n\n"
            "Files included:\n"
            "  chat_transcript.txt   Full conversation history\n"
            "  dax_measures.dax      DAX measures for Power BI\n"
            "  dashboard_spec.json   Machine-readable dashboard spec\n\n"
            "How to use in Power BI Desktop:\n"
            "  1. Open Power BI Desktop and load your data via Get Data\n"
            "  2. Open Modeling > New Measure and paste from dax_measures.dax\n"
            "  3. Build visuals following the spec layout instructions\n\n"
            "Note: Direct .pbix export is simulated via structured outputs.\n"
        ))
    buf.seek(0)
    return buf.read()


# ══════════════════════════════════════════════════════════════════════════
# CHAT RENDER HELPERS
# ══════════════════════════════════════════════════════════════════════════
def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_message(role: str, content: str):
    cls   = "user" if role == "user" else "bot"
    label = "YOU"  if role == "user" else "AI"
    st.markdown(
        f'<div class="msg-row {cls}">'
        f'  <div class="avatar {cls}">{label}</div>'
        f'  <div class="bubble {cls}">{_esc(content)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def stream_response(placeholder, text: str, chunk: int = 4, delay: float = 0.004):
    """Reveal the response progressively for a typing effect."""
    displayed = ""
    for i in range(0, len(text), chunk):
        displayed += text[i : i + chunk]
        placeholder.markdown(
            f'<div class="msg-row bot">'
            f'  <div class="avatar bot">AI</div>'
            f'  <div class="bubble bot">{_esc(displayed)}<span class="cursor"></span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        time.sleep(delay)
    # Final render without cursor
    placeholder.markdown(
        f'<div class="msg-row bot">'
        f'  <div class="avatar bot">AI</div>'
        f'  <div class="bubble bot">{_esc(displayed)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════
with st.sidebar:

    st.markdown(
        f"""
        <div style="text-align:center;padding:14px 0 10px">
            <div style="font-size:27px;font-weight:800;color:#2563EB;letter-spacing:-.5px">
                {AI_NAME}
            </div>
            <div style="font-size:11px;color:#94A3B8;margin-top:3px">
                AI Dashboard Generator
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<hr class="hr">', unsafe_allow_html=True)

    if st.button("New Conversation", use_container_width=True):
        st.session_state.messages      = []
        st.session_state.df            = None
        st.session_state.file_name     = None
        st.session_state.col_types     = {}
        st.session_state.input_key    += 1
        st.rerun()

    st.markdown('<hr class="hr">', unsafe_allow_html=True)

    # ── File Upload ─────────────────────────────────────────────────────
    st.markdown('<div class="sb-label">Upload Data File</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Choose file",
        type=["csv", "xlsx", "xls", "json"],
        label_visibility="collapsed",
        help="Supports CSV, Excel (.xlsx / .xls), and JSON",
    )

    if uploaded:
        result = load_file(uploaded)

        if isinstance(result[1], tuple) or isinstance(result[1], str) and result[0] is None:
            # Error path
            err = result[1]
            if not isinstance(err, tuple):
                err = ("unsupported",)
            render_file_error(err)
            st.session_state.df        = None
            st.session_state.file_name = None
            st.session_state.col_types = {}

        elif result[1] is not None:
            # Tuple-style error
            render_file_error(result[1])
            st.session_state.df        = None
            st.session_state.file_name = None
            st.session_state.col_types = {}

        else:
            df_loaded = result[0]
            st.session_state.df        = df_loaded
            st.session_state.file_name = uploaded.name
            st.session_state.col_types = classify_columns(df_loaded)

            st.markdown(
                f"""
                <div class="alert success">
                    <div class="alert-title">File loaded successfully</div>
                    {_esc(uploaded.name)} &mdash;
                    {df_loaded.shape[0]:,} rows, {df_loaded.shape[1]} columns
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("Data Preview (first 8 rows)", expanded=False):
                st.dataframe(df_loaded.head(8), use_container_width=True)

            with st.expander("Column Classification", expanded=False):
                ct = st.session_state.col_types
                for kind in ("numeric", "categorical", "date"):
                    cols_list = ct.get(kind, [])
                    val = ", ".join(cols_list) if cols_list else "None detected"
                    st.markdown(f"**{kind.title()}**: {val}")

    elif st.session_state.file_name:
        st.markdown(
            f"""
            <div class="alert success">
                <div class="alert-title">Active dataset</div>
                {_esc(st.session_state.file_name)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Missing openpyxl hint (proactive)
    try:
        import openpyxl  # noqa: F401
    except ImportError:
        st.markdown(
            """
            <div class="alert warning">
                <div class="alert-title">Optional dependency missing</div>
                To open <span class="alert-mono">.xlsx</span> files, install:
                <br><span class="alert-mono">pip install openpyxl</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="hr">', unsafe_allow_html=True)

    # ── Example Prompts ─────────────────────────────────────────────────
    st.markdown('<div class="sb-label">Example Prompts</div>', unsafe_allow_html=True)

    for ep in EXAMPLE_PROMPTS:
        if st.button(ep, use_container_width=True, key=f"ep_{ep}"):
            st.session_state.pending_prompt = ep

    st.markdown('<hr class="hr">', unsafe_allow_html=True)

    # ── About ────────────────────────────────────────────────────────────
    with st.expander("About this tool", expanded=False):
        st.markdown(
            f"""
**{AI_NAME}** generates structured Power BI dashboard
specifications from natural language prompts.

**Capabilities**
- Dashboard structure and KPIs
- Visual type recommendations
- DAX measure generation
- Data model schema design
- Downloadable export package

**Supported file types**
CSV, Excel (.xlsx / .xls), JSON

**Note:** Direct .pbix export is simulated via
structured templates and DAX files.
            """
        )


# ══════════════════════════════════════════════════════════════════════════
# MAIN AREA — Header bar
# ══════════════════════════════════════════════════════════════════════════
st.markdown(
    f"""
    <div class="app-header">
        <div class="brand-icon">{ICON_CHART}</div>
        <div>
            <h1>{AI_NAME}</h1>
            <p>{AI_TAGLINE}</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ══════════════════════════════════════════════════════════════════════════
# CHAT HISTORY
# ══════════════════════════════════════════════════════════════════════════
chat_area = st.container()

with chat_area:
    if not st.session_state.messages:
        st.markdown(
            f"""
            <div class="empty-state">
                <div class="es-icon">{ICON_CHART_BLUE}</div>
                <h2>Start by describing your dashboard</h2>
                <p>
                    Try: <em>"Create a Sales Performance Dashboard"</em><br>
                    or upload a data file and ask about your data.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            render_message(msg["role"], msg["content"])
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# EXPORT SECTION
# ══════════════════════════════════════════════════════════════════════════
has_responses = any(m["role"] == "assistant" for m in st.session_state.messages)

if has_responses:
    st.markdown("---")

    ec1, ec2, ec3 = st.columns(3)

    with ec1:
        st.download_button(
            label               = "Export Power BI Package (.zip)",
            data                = build_zip(
                                      st.session_state.messages,
                                      st.session_state.df,
                                      st.session_state.col_types,
                                  ),
            file_name           = "datavizor_powerbi_package.zip",
            mime                = "application/zip",
            use_container_width = True,
        )

    with ec2:
        st.download_button(
            label               = "Download DAX Measures (.dax)",
            data                = compile_dax(st.session_state.messages),
            file_name           = "dax_measures.dax",
            mime                = "text/plain",
            use_container_width = True,
        )

    with ec3:
        st.download_button(
            label               = "Download Spec (.json)",
            data                = compile_json_spec(
                                      st.session_state.messages,
                                      st.session_state.df,
                                      st.session_state.col_types,
                                  ),
            file_name           = "dashboard_spec.json",
            mime                = "application/json",
            use_container_width = True,
        )

    st.markdown(
        """
        <div class="pbix-notice">
            <strong>Limitation notice:</strong>
            Direct <code>.pbix</code> file generation is not natively supported in Python.
            The export package contains structured templates, DAX measures, and a JSON
            specification intended for manual import into Power BI Desktop.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════
# CHAT INPUT
# ══════════════════════════════════════════════════════════════════════════
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

prefill = st.session_state.pending_prompt or ""

input_col, btn_col = st.columns([9, 1])

with input_col:
    user_input = st.text_input(
        "prompt",
        placeholder="Describe your dashboard -- e.g. 'Build a Finance KPI dashboard with YoY growth'",
        label_visibility="collapsed",
        key=f"chat_input_{st.session_state.input_key}",
        value=prefill,
    )

with btn_col:
    send_clicked = st.button("Send", use_container_width=True)

# Clear pending prompt after populating the input box
if st.session_state.pending_prompt:
    st.session_state.pending_prompt = None


# ══════════════════════════════════════════════════════════════════════════
# PROCESS & RESPOND
# ══════════════════════════════════════════════════════════════════════════
if send_clicked:
    prompt = user_input.strip()

    if not prompt:
        st.warning("Please enter a prompt before sending.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = generate_response(
            prompt,
            st.session_state.df,
            st.session_state.col_types,
        )

        anim_slot = st.empty()
        stream_response(anim_slot, response)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.input_key += 1
        st.rerun()
