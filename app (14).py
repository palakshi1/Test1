"""
╔══════════════════════════════════════════════════════════════════════╗
║         Power BI Dashboard AI Assistant — Streamlit App             ║
║  Generates Power BI dashboard specs, DAX, layouts from natural NLP  ║
╚══════════════════════════════════════════════════════════════════════╝

Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import json
import re
import time
import io
import zipfile
from datetime import datetime
from typing import Optional

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PowerBI AI Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS — Clean white + steel-blue theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root variables ── */
:root {
    --primary:   #2563EB;
    --primary-lt:#DBEAFE;
    --accent:    #0EA5E9;
    --surface:   #F8FAFC;
    --card:      #FFFFFF;
    --border:    #E2E8F0;
    --text:      #1E293B;
    --muted:     #64748B;
    --user-bg:   #EFF6FF;
    --bot-bg:    #FFFFFF;
    --radius:    12px;
    --shadow:    0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.04);
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text);
}

/* ── App background ── */
.stApp {
    background: var(--surface);
}

/* ── Hide Streamlit default chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--card) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container { padding-top: .5rem; }

/* ── Chat container ── */
.chat-wrapper {
    max-width: 860px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 8px 4px 24px;
}

/* ── Message bubbles ── */
.msg-row {
    display: flex;
    align-items: flex-start;
    gap: 10px;
}
.msg-row.user  { flex-direction: row-reverse; }
.msg-row.bot   { flex-direction: row; }

.avatar {
    width: 34px; height: 34px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}
.avatar.user { background: var(--primary); color: #fff; }
.avatar.bot  { background: linear-gradient(135deg,#2563EB,#0EA5E9); color: #fff; }

.bubble {
    max-width: 78%;
    padding: 14px 18px;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    font-size: 14.5px;
    line-height: 1.65;
    white-space: pre-wrap;
    word-break: break-word;
}
.bubble.user {
    background: var(--primary);
    color: #fff;
    border-bottom-right-radius: 4px;
}
.bubble.bot {
    background: var(--bot-bg);
    border: 1px solid var(--border);
    border-bottom-left-radius: 4px;
}

/* ── Code blocks inside bubbles ── */
.bubble code, .bubble pre {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12.5px;
    background: #F1F5F9;
    border-radius: 6px;
    padding: 2px 6px;
}
.bubble pre { padding: 10px 14px; display: block; overflow-x: auto; }

/* ── App title bar ── */
.app-header {
    background: var(--card);
    border-bottom: 1px solid var(--border);
    padding: 14px 28px;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
    border-radius: 0 0 var(--radius) var(--radius);
    box-shadow: var(--shadow);
}
.app-header .logo { font-size: 26px; }
.app-header h1 {
    margin: 0; font-size: 20px; font-weight: 700;
    color: var(--primary);
    letter-spacing: -.3px;
}
.app-header p { margin: 0; font-size: 12.5px; color: var(--muted); }

/* ── Section badges ── */
.section-badge {
    display: inline-block;
    background: var(--primary-lt);
    color: var(--primary);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .4px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

/* ── Data preview table ── */
.data-preview {
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    margin-top: 8px;
}

/* ── Prompt chip ── */
.stButton > button {
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    transition: all .15s ease !important;
}

/* ── Download button accent ── */
.dl-btn > button {
    background: var(--primary) !important;
    color: white !important;
    border: none !important;
}

/* ── Typing cursor animation ── */
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
.cursor { display: inline-block; width: 2px; height: 1em;
          background: var(--primary); margin-left: 2px;
          animation: blink 1s step-start infinite; vertical-align: text-bottom; }

/* ── Info notice ── */
.notice {
    background: #FFF7ED; border: 1px solid #FED7AA;
    color: #9A3412; border-radius: 8px;
    padding: 8px 14px; font-size: 12.5px; margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
EXAMPLE_PROMPTS = [
    "📈 Sales Performance Dashboard",
    "💰 Finance KPI with YoY Growth",
    "🌍 Regional Sales Breakdown",
    "👥 HR Headcount & Attrition",
    "📦 Inventory & Supply Chain",
    "🛒 E-Commerce Funnel Dashboard",
]

DASHBOARD_KEYWORDS = {
    "sales":     ["Sales", "Revenue", "Profit", "Discount", "Units Sold"],
    "finance":   ["Revenue", "EBITDA", "Net Profit", "Operating Cost", "Budget vs Actual"],
    "hr":        ["Headcount", "Attrition Rate", "Avg Tenure", "Hire vs Exit", "Department"],
    "inventory": ["Stock Level", "Reorder Point", "Stockout Rate", "Lead Time", "SKU"],
    "ecommerce": ["Orders", "Conversion Rate", "Avg Order Value", "Cart Abandonment", "Sessions"],
    "regional":  ["Region", "Territory", "Sales by Area", "Top Markets", "Growth %"],
}

# ─────────────────────────────────────────────
# SESSION STATE INITIALISATION
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "messages":      [],
        "df":            None,
        "file_name":     None,
        "col_types":     {},
        "input_key":     0,
        "pending_prompt": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────
# DATA ANALYSIS HELPERS
# ─────────────────────────────────────────────
def classify_columns(df: pd.DataFrame) -> dict:
    """Classify dataframe columns into numeric / categorical / date types."""
    col_types = {"numeric": [], "categorical": [], "date": []}
    for col in df.columns:
        dtype = df[col].dtype
        if pd.api.types.is_numeric_dtype(dtype):
            col_types["numeric"].append(col)
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            col_types["date"].append(col)
        else:
            # Try parsing as date
            try:
                parsed = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")
                null_frac = parsed.isna().mean()
                if null_frac < 0.3:
                    col_types["date"].append(col)
                    continue
            except Exception:
                pass
            col_types["categorical"].append(col)
    return col_types


def build_data_context(df: pd.DataFrame, col_types: dict) -> str:
    """Build a text summary of the uploaded dataset for prompt injection."""
    rows, cols = df.shape
    lines = [
        f"Dataset: {rows} rows × {cols} columns",
        f"Numeric columns : {', '.join(col_types['numeric'])  or 'None'}",
        f"Categorical cols: {', '.join(col_types['categorical']) or 'None'}",
        f"Date columns    : {', '.join(col_types['date'])       or 'None'}",
    ]
    return "\n".join(lines)

# ─────────────────────────────────────────────
# DASHBOARD GENERATION ENGINE
# ─────────────────────────────────────────────
def detect_domain(prompt: str) -> str:
    """Detect dashboard domain from prompt keywords."""
    p = prompt.lower()
    for domain in DASHBOARD_KEYWORDS:
        if domain in p:
            return domain
    for domain, kpis in DASHBOARD_KEYWORDS.items():
        if any(k.lower() in p for k in kpis):
            return domain
    return "sales"  # sensible default


def pick_visuals(col_types: dict, domain: str) -> list:
    """Recommend visuals based on column types."""
    visuals = []
    nums  = col_types.get("numeric", [])
    cats  = col_types.get("categorical", [])
    dates = col_types.get("date", [])

    if dates and nums:
        visuals.append(f"Line Chart  : {dates[0]} vs {nums[0]}  — trend over time")
    if cats and nums:
        visuals.append(f"Bar Chart   : {cats[0]} vs {nums[0]}  — comparison")
    if len(cats) >= 2 and nums:
        visuals.append(f"Stacked Bar : {cats[0]} (stack: {cats[1]}) vs {nums[0]}")
    if nums:
        visuals.append(f"KPI Cards   : {', '.join(nums[:4])}")
    if cats and nums:
        visuals.append(f"Pie / Donut : {cats[0]} share of {nums[0]}")
    if len(nums) >= 2:
        visuals.append(f"Scatter Plot: {nums[0]} vs {nums[1]}")
    if "region" in [c.lower() for c in cats]:
        visuals.append("Map Visual  : Regional distribution")

    # Fallbacks
    if not visuals:
        domain_defaults = {
            "sales":     ["Line Chart: Date vs Revenue", "Bar Chart: Region vs Sales",
                          "KPI Cards: Revenue, Profit, Units", "Pie: Product Category split"],
            "finance":   ["Waterfall: Revenue → EBITDA", "Bar: Budget vs Actual by Dept",
                          "Line: Monthly Cash Flow", "KPI: Net Profit Margin"],
            "hr":        ["Bar: Headcount by Dept", "Line: Monthly Attrition",
                          "Pie: Gender split", "KPI: Total Headcount, Attrition %"],
            "inventory": ["Line: Stock Level over Time", "Bar: SKU vs Stock",
                          "Gauge: Stockout Rate", "Table: Reorder Alerts"],
            "ecommerce": ["Funnel: Sessions→Cart→Purchase", "Line: Daily Orders",
                          "Bar: Top Products", "KPI: CVR, AOV, Revenue"],
            "regional":  ["Map: Sales by Region", "Bar: Top 10 Regions",
                          "Line: Region Growth over Time", "KPI: Total Markets"],
        }
        visuals = domain_defaults.get(domain, domain_defaults["sales"])

    return visuals


def generate_dax(col_types: dict, domain: str) -> list:
    """Generate realistic DAX measures."""
    nums = col_types.get("numeric", [])
    dates = col_types.get("date", [])
    table = "Data"  # generic table name

    base_dax = []

    if nums:
        n = nums[0]
        base_dax += [
            f"Total {n} = SUM({table}[{n}])",
            f"Avg {n} = AVERAGE({table}[{n}])",
        ]
        if len(nums) >= 2:
            n2 = nums[1]
            base_dax.append(
                f"{n} Margin % = DIVIDE([Total {n}] - [Total {n2}], [Total {n}], 0)"
            )
    if dates and nums:
        n = nums[0]
        d = dates[0]
        base_dax += [
            f"YoY Growth % = "
            f"DIVIDE([Total {n}] - CALCULATE([Total {n}], SAMEPERIODLASTYEAR({table}[{d}])), "
            f"CALCULATE([Total {n}], SAMEPERIODLASTYEAR({table}[{d}])), 0)",
            f"MTD {n} = TOTALMTD([Total {n}], {table}[{d}])",
            f"QTD {n} = TOTALQTD([Total {n}], {table}[{d}])",
            f"YTD {n} = TOTALYTD([Total {n}], {table}[{d}])",
        ]
    if not base_dax:
        domain_dax = {
            "sales":   ["Total Sales = SUM(Sales[Amount])",
                        "Profit Margin = DIVIDE([Profit],[Total Sales],0)",
                        "YoY Growth % = DIVIDE([Total Sales]-CALCULATE([Total Sales],SAMEPERIODLASTYEAR(Calendar[Date])),CALCULATE([Total Sales],SAMEPERIODLASTYEAR(Calendar[Date])),0)",
                        "MTD Sales = TOTALMTD([Total Sales], Calendar[Date])"],
            "finance": ["Net Revenue = SUM(Finance[Revenue])",
                        "EBITDA Margin = DIVIDE([EBITDA],[Net Revenue],0)",
                        "Budget Variance = [Actual] - [Budget]",
                        "Variance % = DIVIDE([Budget Variance],[Budget],0)"],
            "hr":      ["Total Headcount = COUNTROWS(Employees)",
                        "Attrition Rate = DIVIDE([Exits],[Total Headcount],0)",
                        "Avg Tenure = AVERAGE(Employees[Tenure_Years])",
                        "New Hires = CALCULATE([Total Headcount], Employees[Status]=\"New\")"],
        }
        base_dax = domain_dax.get(domain, domain_dax["sales"])

    return base_dax


def generate_kpis(col_types: dict, domain: str) -> list:
    """Suggest KPI cards."""
    nums = col_types.get("numeric", [])
    if nums:
        return [f"Total {n}" for n in nums[:5]]
    defaults = {
        "sales":     ["Total Revenue", "Gross Profit", "Units Sold", "Profit Margin %", "YoY Growth %"],
        "finance":   ["Net Revenue", "EBITDA", "Net Profit", "Operating Cost", "Budget Variance"],
        "hr":        ["Total Headcount", "Attrition Rate", "New Hires", "Avg Tenure", "Open Positions"],
        "inventory": ["Total SKUs", "Stockout %", "Reorder Items", "Avg Lead Time", "Inventory Value"],
        "ecommerce": ["Total Orders", "Conversion Rate", "Avg Order Value", "Cart Abandonment", "Revenue"],
        "regional":  ["Total Regions", "Top Region Revenue", "Growth %", "Market Coverage", "Net Sales"],
    }
    return defaults.get(domain, defaults["sales"])


def generate_schema(col_types: dict, domain: str) -> list:
    """Generate recommended data model tables."""
    nums = col_types.get("numeric", [])
    cats = col_types.get("categorical", [])
    dates = col_types.get("date", [])

    tables = []
    if nums or cats or dates:
        tables.append(f"FactData ({', '.join((nums + cats + dates)[:6])})")
    else:
        domain_schema = {
            "sales":     ["FactSales (Date, ProductKey, CustomerKey, Amount, Qty, Discount)",
                          "DimProduct (ProductKey, Name, Category, Brand)",
                          "DimCustomer (CustomerKey, Name, Region, Segment)",
                          "DimDate (Date, Month, Quarter, Year, WeekNum)"],
            "finance":   ["FactFinance (Date, DeptKey, Revenue, Cost, Budget)",
                          "DimDepartment (DeptKey, Name, CostCenter, Manager)",
                          "DimDate (Date, Month, Quarter, Year, FY)"],
            "hr":        ["FactHR (EmployeeKey, Date, Status, Salary)",
                          "DimEmployee (EmployeeKey, Name, Dept, Grade, StartDate)",
                          "DimDepartment (DeptKey, Name, Location, Manager)"],
        }
        tables = domain_schema.get(domain, domain_schema["sales"])

    if dates:
        tables.append(f"DimDate ({dates[0]}, Month, Quarter, Year)")
    elif not any("Date" in t for t in tables):
        tables.append("DimDate (Date, Month, Quarter, Year, IsWeekday)")

    return tables


def build_dashboard_response(prompt: str, df: Optional[pd.DataFrame], col_types: dict) -> str:
    """
    Core engine: combine prompt + dataset context → structured dashboard spec.
    Replace the rule-based logic here with an OpenAI/Claude API call if desired.
    """
    domain = detect_domain(prompt)
    title  = prompt.strip().title() if len(prompt) < 60 else f"{domain.title()} Performance Dashboard"

    kpis    = generate_kpis(col_types, domain)
    visuals = pick_visuals(col_types, domain)
    schema  = generate_schema(col_types, domain)
    dax     = generate_dax(col_types, domain)

    data_note = ""
    if df is not None:
        rows, cols_n = df.shape
        data_note = (
            f"\n📂 Dataset context: {rows} rows × {cols_n} columns — "
            f"visuals and DAX measures are tailored to your uploaded data.\n"
        )

    layout = (
        "Top row    : KPI Summary Cards (full width)\n"
        "Middle row : Primary trend visual (60%) + donut/pie (40%)\n"
        "Bottom row : Categorical bar chart (50%) + supporting table (50%)\n"
        "Filters    : Date slicer, Category dropdown, Region slicer (top-right panel)"
    )

    response = f"""Dashboard Title: {title}
{data_note}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Key Metrics (KPI Cards)
   {'  '.join(f'▸ {k}' for k in kpis)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2. Recommended Visuals
{chr(10).join(f'   ▸ {v}' for v in visuals)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. Data Model (Tables)
{chr(10).join(f'   ▸ {s}' for s in schema)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4. DAX Measures
{chr(10).join(f'   {m}' for m in dax)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5. Dashboard Layout
   {layout}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Power BI Tips
   ▸ Import your data via "Get Data → Excel/CSV"
   ▸ Create a DimDate table using CALENDARAUTO()
   ▸ Mark DimDate as the date table for time-intelligence
   ▸ Enable "Row-level Security" for regional data

⚠️  Note: Direct .pbix generation is simulated via structured templates.
    Use the export buttons below to download your dashboard package.
"""
    return response

# ─────────────────────────────────────────────
# EXPORT BUILDERS
# ─────────────────────────────────────────────
def build_dax_file(messages: list) -> str:
    """Extract and compile all DAX from chat history."""
    lines = ["// ── DAX Measures — PowerBI AI Assistant ──\n"]
    for m in messages:
        if m["role"] == "assistant" and "DAX Measures" in m["content"]:
            block = m["content"]
            # Grab lines after "4. DAX Measures"
            capture = False
            for line in block.splitlines():
                if "4. DAX Measures" in line:
                    capture = True; continue
                if capture:
                    if line.startswith("━") or line.startswith("5."):
                        break
                    stripped = line.strip()
                    if stripped and not stripped.startswith("//"):
                        lines.append(stripped)
    return "\n".join(lines)


def build_json_spec(messages: list, df: Optional[pd.DataFrame], col_types: dict) -> str:
    """Build a structured JSON export of the latest dashboard spec."""
    last_bot = next(
        (m["content"] for m in reversed(messages) if m["role"] == "assistant"), ""
    )
    spec = {
        "generated_at": datetime.now().isoformat(),
        "tool": "PowerBI AI Assistant",
        "disclaimer": "Direct .pbix generation is simulated. Use this spec inside Power BI Desktop.",
        "dashboard_spec": last_bot,
        "dataset_summary": (
            build_data_context(df, col_types) if df is not None else "No dataset uploaded"
        ),
    }
    return json.dumps(spec, indent=2)


def build_zip_package(messages: list, df: Optional[pd.DataFrame], col_types: dict) -> bytes:
    """Bundle all exports into a downloadable ZIP."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        # Full chat transcript
        transcript = "\n\n".join(
            f"[{m['role'].upper()}]\n{m['content']}" for m in messages
        )
        zf.writestr("chat_transcript.txt", transcript)

        # DAX file
        zf.writestr("dax_measures.dax", build_dax_file(messages))

        # JSON spec
        zf.writestr("dashboard_spec.json", build_json_spec(messages, df, col_types))

        # README
        readme = (
            "PowerBI AI Assistant — Export Package\n"
            "══════════════════════════════════════\n\n"
            "Files included:\n"
            "  chat_transcript.txt  — Full conversation history\n"
            "  dax_measures.dax     — DAX measures to paste into Power BI\n"
            "  dashboard_spec.json  — Machine-readable dashboard specification\n\n"
            "How to use in Power BI Desktop:\n"
            "  1. Open Power BI Desktop\n"
            "  2. Load your data via 'Get Data'\n"
            "  3. Open 'New Measure' and paste from dax_measures.dax\n"
            "  4. Build visuals following the spec layout\n\n"
            "Note: Direct .pbix generation is simulated via structured outputs.\n"
        )
        zf.writestr("README.txt", readme)

    buf.seek(0)
    return buf.read()

# ─────────────────────────────────────────────
# CHAT RENDER
# ─────────────────────────────────────────────
def render_message(role: str, content: str, animate: bool = False):
    """Render a single chat bubble."""
    if role == "user":
        avatar = "🧑"
        cls    = "user"
    else:
        avatar = "📊"
        cls    = "bot"

    # Escape HTML in content for safe display
    safe_content = (
        content
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    html = f"""
    <div class="msg-row {cls}">
        <div class="avatar {cls}">{avatar}</div>
        <div class="bubble {cls}">{safe_content}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def stream_response(placeholder, text: str, delay: float = 0.006):
    """Typing animation: reveal text character by character."""
    displayed = ""
    for char in text:
        displayed += char
        safe = (
            displayed
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        placeholder.markdown(
            f"""
            <div class="msg-row bot">
                <div class="avatar bot">📊</div>
                <div class="bubble bot">{safe}<span class="cursor"></span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(delay)
    # Final render without cursor
    safe = (
        displayed
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    placeholder.markdown(
        f"""
        <div class="msg-row bot">
            <div class="avatar bot">📊</div>
            <div class="bubble bot">{safe}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:10px 0 4px">
        <div style="font-size:36px">📊</div>
        <div style="font-weight:700;font-size:17px;color:#2563EB">PowerBI AI</div>
        <div style="font-size:12px;color:#64748B">Dashboard Generator</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # New Chat
    if st.button("🆕  New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.df       = None
        st.session_state.file_name = None
        st.session_state.col_types = {}
        st.session_state.input_key += 1
        st.rerun()

    st.divider()

    # ── File Uploader ──
    st.markdown('<div class="section-badge">📂 Upload Data</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload Excel or CSV",
        type=["xlsx", "xls", "csv"],
        label_visibility="collapsed",
    )

    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)

            st.session_state.df        = df
            st.session_state.file_name = uploaded.name
            st.session_state.col_types = classify_columns(df)

            st.success(f"✅ {uploaded.name} loaded ({df.shape[0]} rows, {df.shape[1]} cols)")

            with st.expander("👁️ Preview", expanded=False):
                st.dataframe(df.head(5), use_container_width=True)

            with st.expander("📋 Column types", expanded=False):
                for kind, cols in st.session_state.col_types.items():
                    if cols:
                        st.markdown(f"**{kind.title()}**: {', '.join(cols)}")

        except Exception as e:
            st.error(f"Could not read file: {e}")

    elif st.session_state.file_name:
        st.info(f"📄 Active: {st.session_state.file_name}")

    st.divider()

    # ── Example Prompts ──
    st.markdown('<div class="section-badge">💡 Example Prompts</div>', unsafe_allow_html=True)
    for ep in EXAMPLE_PROMPTS:
        if st.button(ep, use_container_width=True, key=f"ep_{ep}"):
            st.session_state.pending_prompt = ep.split(" ", 1)[1]  # strip emoji

    st.divider()

    # ── About ──
    with st.expander("ℹ️ About this app", expanded=False):
        st.markdown("""
**PowerBI AI Assistant** generates structured Power BI dashboard specifications from natural language.

**Capabilities:**
- Dashboard structure & KPIs
- Visual recommendations
- DAX measure generation
- Data model schema
- Export package (DAX + JSON + transcript)

**Tip:** Upload your Excel/CSV for data-aware generation.

⚠️ *Direct .pbix generation is simulated via structured templates.*
        """)

# ─────────────────────────────────────────────
# MAIN AREA — Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="logo">📊</div>
    <div>
        <h1>Power BI Dashboard AI Assistant</h1>
        <p>Describe any dashboard — get structure, visuals, DAX measures & export package instantly</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHAT HISTORY
# ─────────────────────────────────────────────
chat_area = st.container()

with chat_area:
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:#94A3B8">
            <div style="font-size:52px;margin-bottom:12px">📊</div>
            <div style="font-size:18px;font-weight:600;color:#475569;margin-bottom:6px">
                Start by describing your dashboard
            </div>
            <div style="font-size:14px">
                Try: <em>"Create a sales performance dashboard"</em><br>
                or upload an Excel file and ask about your data
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            render_message(msg["role"], msg["content"])
        st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# EXPORT BUTTONS (show when there are bot messages)
# ─────────────────────────────────────────────
has_responses = any(m["role"] == "assistant" for m in st.session_state.messages)

if has_responses:
    st.markdown("---")
    ecol1, ecol2, ecol3 = st.columns([1, 1, 1])

    with ecol1:
        zip_bytes = build_zip_package(
            st.session_state.messages,
            st.session_state.df,
            st.session_state.col_types,
        )
        st.download_button(
            label="📦 Export Power BI Package (.zip)",
            data=zip_bytes,
            file_name="powerbi_dashboard_package.zip",
            mime="application/zip",
            use_container_width=True,
        )

    with ecol2:
        dax_text = build_dax_file(st.session_state.messages)
        st.download_button(
            label="📐 Download DAX Measures (.dax)",
            data=dax_text,
            file_name="dax_measures.dax",
            mime="text/plain",
            use_container_width=True,
        )

    with ecol3:
        json_text = build_json_spec(
            st.session_state.messages,
            st.session_state.df,
            st.session_state.col_types,
        )
        st.download_button(
            label="🗂️ Download Spec (.json)",
            data=json_text,
            file_name="dashboard_spec.json",
            mime="application/json",
            use_container_width=True,
        )

    st.markdown("""
    <div class="notice">
    ⚠️ <strong>Limitation:</strong> Direct <code>.pbix</code> file generation is not natively
    supported in Python. The export package contains structured templates, DAX measures,
    and a JSON specification — import these manually into Power BI Desktop.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHAT INPUT
# ─────────────────────────────────────────────
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

input_col, btn_col = st.columns([9, 1])

with input_col:
    user_input = st.text_input(
        "Message",
        placeholder="Describe your dashboard, e.g. 'Build a finance KPI dashboard with YoY growth'…",
        label_visibility="collapsed",
        key=f"chat_input_{st.session_state.input_key}",
        value=st.session_state.pending_prompt or "",
    )

with btn_col:
    send = st.button("Send ➤", use_container_width=True)

# Clear pending prompt after it populates the input
if st.session_state.pending_prompt:
    st.session_state.pending_prompt = None

# ─────────────────────────────────────────────
# PROCESS INPUT & GENERATE RESPONSE
# ─────────────────────────────────────────────
if send and user_input.strip():
    prompt = user_input.strip()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response
    response = build_dashboard_response(
        prompt,
        st.session_state.df,
        st.session_state.col_types,
    )

    # Animate the bot reply
    anim_placeholder = st.empty()
    stream_response(anim_placeholder, response, delay=0.004)

    # Persist to history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Bump input key to clear the text box
    st.session_state.input_key += 1
    st.rerun()

elif send and not user_input.strip():
    st.warning("Please enter a prompt before sending.", icon="⚠️")
