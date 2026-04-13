import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from groq import Groq
import plotly.express as px
import plotly.graph_objects as go
import os
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}",
    connect_args={"sslmode": "require"},
)
st.set_page_config(
    page_title="QueryMind — AI Sales Intelligence", page_icon="⚡", layout="wide"
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

* { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: #080c14;
    color: #e2e8f0;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 2rem 2.5rem; max-width: 1400px; }

.hero {
    background: linear-gradient(135deg, #0d1f3c 0%, #0a1628 50%, #060d1a 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(59,130,246,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-tag {
    display: inline-block;
    background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.3);
    color: #60a5fa;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 1rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.hero h1 {
    font-family: 'Space Mono', monospace !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: #f1f5f9 !important;
    margin: 0 0 0.5rem 0 !important;
    letter-spacing: -1px;
}
.hero h1 span { color: #3b82f6; }
.hero p {
    color: #64748b;
    font-size: 1rem;
    margin: 0;
    font-weight: 300;
}
.hero-stats {
    display: flex;
    gap: 2rem;
    margin-top: 1.5rem;
}
.hero-stat { text-align: left; }
.hero-stat-num {
    font-family: 'Space Mono', monospace;
    font-size: 1.3rem;
    font-weight: 700;
    color: #3b82f6;
}
.hero-stat-label {
    font-size: 0.75rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.input-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #3b82f6;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 0.75rem;
}

.stTextInput > div > div > input {
    background: #060d1a !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    font-size: 1.05rem !important;
    padding: 14px 18px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
}
.stTextInput > div > div > input::placeholder { color: #334155 !important; }
.stTextInput label { display: none !important; }

.section-card {
    background: #0d1420;
    border: 1px solid #1a2d4a;
    border-radius: 14px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
}
.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #3b82f6;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, #1e3a5f, transparent);
}

.metric-big {
    background: linear-gradient(135deg, #0d1f3c, #091628);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
}
.metric-big-value {
    font-family: 'Space Mono', monospace;
    font-size: 3rem;
    font-weight: 700;
    color: #3b82f6;
}
.metric-big-label {
    color: #64748b;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.5rem;
}

.thinking-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(59,130,246,0.1);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 20px;
    padding: 6px 16px;
    color: #60a5fa;
    font-size: 0.85rem;
    margin-bottom: 1.5rem;
}

section[data-testid="stSidebar"] {
    background: #060d1a !important;
    border-right: 1px solid #0f1e33 !important;
}
section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem;
}

div.stButton > button {
    width: 100% !important;
    background: #0d1f3c !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
    padding: 8px 12px !important;
    margin-bottom: 6px !important;
    text-align: left !important;
    transition: all 0.2s ease !important;
    font-family: 'DM Sans', sans-serif !important;
}
div.stButton > button:hover {
    background: #1e3a5f !important;
    border-color: #3b82f6 !important;
    color: #e2e8f0 !important;
}

.stSpinner > div { border-top-color: #3b82f6 !important; }
.stDataFrame { border-radius: 10px; overflow: hidden; }
hr { border-color: #0f1e33 !important; }

.sidebar-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #334155;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 1rem 0 0.5rem 0;
}
</style>
""",
    unsafe_allow_html=True,
)

# ── SCHEMA ───────────────────────────────────────
SCHEMA = """
Table: sales (PostgreSQL)
Columns:
- order_id VARCHAR
- order_date DATE
- city VARCHAR (Mumbai, Pune, Ahmedabad, Surat, Delhi, Jaipur, Lucknow, Chandigarh, Bangalore, Chennai, Hyderabad, Kochi, Kolkata, Bhubaneswar, Patna, Guwahati)
- region VARCHAR (West, North, South, East)
- category VARCHAR (Electronics, Fashion, Home & Kitchen, Sports, Books, Beauty, Toys, Grocery)
- subcategory VARCHAR
- segment VARCHAR (Retail, Wholesale, Corporate)
- payment_method VARCHAR (UPI, Credit Card, Debit Card, Net Banking, Cash on Delivery, EMI)
- quantity INT
- unit_price DECIMAL
- discount_pct INT
- discount_amount DECIMAL
- sales DECIMAL
- profit DECIMAL
- order_status VARCHAR (Delivered, Returned, Cancelled, Pending)
"""


# ── SQL GENERATION ───────────────────────────────
def generate_sql(question):
    prompt = f"""You are a senior PostgreSQL data analyst with 10+ years of experience. Write a precise PostgreSQL query to answer the question.

Schema:
{SCHEMA}

You MUST use advanced SQL when appropriate:
- Window functions: ROW_NUMBER(), RANK(), DENSE_RANK(), LAG(), LEAD(), SUM() OVER(), AVG() OVER(), NTILE(), PERCENT_RANK()
- CTEs: WITH clause for multi-step analysis
- Subqueries: for filtering, aggregation, comparisons
- CASE WHEN: for conditional logic and bucketing
- Date functions: EXTRACT(YEAR FROM ...), EXTRACT(MONTH FROM ...), TO_CHAR(date, 'YYYY-MM'), DATE_TRUNC(), AGE()
- String functions: CONCAT(), STRING_AGG()
- Advanced aggregations: ROLLUP, HAVING, multiple GROUP BY

Examples of advanced queries:
- "Rank cities by sales" → use DENSE_RANK() OVER (ORDER BY ...)
- "Month over month growth" → use LAG() OVER (ORDER BY month)
- "Running total of sales" → use SUM(sales) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING)
- "Top product in each region" → use ROW_NUMBER() OVER (PARTITION BY region ORDER BY sales DESC)
- "Categories above average profit" → use subquery with AVG()
- "Percentile of each city" → use NTILE() or PERCENT_RANK()

Rules:
- Return ONLY the raw SQL query, absolutely nothing else
- No markdown, no backticks, no explanation, no comments
- Use LIMIT 20 unless user asks for more or it is a window function query
- Use ROUND() for all decimals to 2 places
- Use clear descriptive column aliases with AS
- NEVER use reserved words as aliases — never use: rank, order, group, row, index, key, select, where, value
- Instead use suffixed aliases: city_rank, sales_order, profit_group, row_num
- For window functions always wrap in a subquery or CTE for clean output

Question: {question}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    sql = response.choices[0].message.content.strip()
    sql = re.sub(r"```sql|```", "", sql).strip()
    return sql


def fix_sql(sql):
    reserved = [
        "rank",
        "order",
        "group",
        "select",
        "where",
        "index",
        "key",
        "value",
        "row",
        "rows",
    ]
    for word in reserved:
        sql = re.sub(rf"\bAS\s+{word}\b", f"AS {word}_val", sql, flags=re.IGNORECASE)
        sql = re.sub(
            rf",\s*{word}\b(\s+FROM)", rf", {word}_val\1", sql, flags=re.IGNORECASE
        )
        sql = re.sub(
            rf"ORDER BY\s+{word}\b", f"ORDER BY {word}_val", sql, flags=re.IGNORECASE
        )
    return sql


def run_query(sql):
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn)


# ── CHART LOGIC ──────────────────────────────────
def suggest_chart(df):
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols = df.select_dtypes(include="object").columns.tolist()
    if len(df) == 1 and len(numeric_cols) == 1:
        return "metric"
    elif len(text_cols) >= 1 and len(numeric_cols) >= 1 and len(df) <= 15:
        return "bar"
    elif len(text_cols) >= 1 and len(numeric_cols) >= 1:
        return "line"
    elif len(numeric_cols) >= 2:
        return "scatter"
    return "table"


def render_chart(df, chart_type, question):
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols = df.select_dtypes(include="object").columns.tolist()
    date_cols = df.select_dtypes(include="datetime").columns.tolist()

    layout_base = dict(
        height=420,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#94a3b8", size=12),
        xaxis=dict(
            gridcolor="#0f1e33", linecolor="#1e3a5f", tickfont=dict(color="#64748b")
        ),
        yaxis=dict(
            gridcolor="#0f1e33", linecolor="#1e3a5f", tickfont=dict(color="#64748b")
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        title=dict(font=dict(family="Space Mono", color="#e2e8f0", size=13), x=0),
    )

    if chart_type == "metric":
        val = df[numeric_cols[0]].iloc[0]
        label = numeric_cols[0].replace("_", " ").title()
        formatted = (
            f"₹{val:,.0f}"
            if any(
                k in numeric_cols[0].lower()
                for k in ["sales", "profit", "price", "amount", "revenue"]
            )
            else f"{val:,.2f}"
        )
        st.markdown(
            f"""
        <div class="metric-big">
            <div class="metric-big-value">{formatted}</div>
            <div class="metric-big-label">{label}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    elif chart_type == "bar":
        x = text_cols[0] if text_cols else df.columns[0]
        y = numeric_cols[0]
        fig = go.Figure(
            go.Bar(
                x=df[x],
                y=df[y],
                marker=dict(
                    color=df[y],
                    colorscale=[[0, "#1d4ed8"], [0.5, "#3b82f6"], [1, "#93c5fd"]],
                    line=dict(width=0),
                ),
                text=df[y].apply(
                    lambda v: f"₹{v/1e6:.1f}M" if v > 1e5 else f"{v:,.0f}"
                ),
                textposition="outside",
                textfont=dict(color="#94a3b8", size=11),
            )
        )
        fig.update_layout(
            **layout_base, title_text=question.title(), bargap=0.3, showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "line":
        x = date_cols[0] if date_cols else df.columns[0]
        y = numeric_cols[0]
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df[x],
                y=df[y],
                mode="lines+markers",
                line=dict(color="#3b82f6", width=2.5),
                marker=dict(
                    color="#60a5fa", size=7, line=dict(color="#1d4ed8", width=2)
                ),
                fill="tozeroy",
                fillcolor="rgba(59,130,246,0.05)",
            )
        )
        fig.update_layout(**layout_base, title_text=question.title(), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "scatter":
        fig = go.Figure(
            go.Scatter(
                x=df[numeric_cols[0]],
                y=df[numeric_cols[1]],
                mode="markers",
                marker=dict(
                    color="#3b82f6",
                    size=9,
                    opacity=0.7,
                    line=dict(color="#60a5fa", width=1),
                ),
            )
        )
        fig.update_layout(**layout_base, title_text=question.title(), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.dataframe(df, use_container_width=True, hide_index=True)


# ── SIDEBAR ──────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-label">⚡ QueryMind</div>', unsafe_allow_html=True)
    st.markdown("### Try These")

    examples = [
        "Show top 5 cities by total sales",
        "Which category has the highest profit?",
        "Show monthly sales trend in 2024",
        "Total revenue by region",
        "Most popular payment method",
        "Top 5 subcategories by quantity",
        "Average order value by segment",
        "Cancelled orders by city",
        "Highest sales month in 2023",
        "Profit across all categories",
        "Rank cities by profit within each region",
        "Show month over month sales growth in 2024",
        "Running total of sales by month",
        "Top subcategory in each category",
        "Categories above average profit",
        "Return rate by category",
    ]

    for ex in examples:
        if st.button(ex, key=ex):
            st.session_state["input_question"] = ex

    st.markdown("---")
    st.markdown(
        '<div class="sidebar-label">Database Info</div>', unsafe_allow_html=True
    )
    st.markdown("🗄️ **50,000** records")
    st.markdown("📅 Jan 2023 – Dec 2024")
    st.markdown("🏙️ 16 Indian cities")
    st.markdown("📦 8 categories")
    st.markdown("---")
    st.markdown('<div class="sidebar-label">Built by</div>', unsafe_allow_html=True)
    st.markdown("**Manav Kumar**")
    st.markdown("*Data Analyst*")

# ── MAIN ─────────────────────────────────────────
st.markdown(
    """
<div class="hero">
    <div class="hero-tag">⚡ Powered by Llama 3.3 + Groq</div>
    <h1>Query<span>Mind</span></h1>
    <p>Ask any business question in plain English. Get instant SQL, charts, and insights.</p>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-num">50K</div>
            <div class="hero-stat-label">Records</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-num">16</div>
            <div class="hero-stat-label">Cities</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-num">8</div>
            <div class="hero-stat-label">Categories</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-num">2yr</div>
            <div class="hero-stat-label">Data Range</div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="input-label">🔍 Ask your question</div>', unsafe_allow_html=True
)
question = st.text_input(
    "question_input",
    placeholder="e.g. Rank cities by profit within each region ",
    value=st.session_state.get("input_question", ""),
    label_visibility="collapsed",
)

if question:
    with st.spinner(""):
        st.markdown(
            '<div class="thinking-badge">⚡ Generating SQL & fetching results...</div>',
            unsafe_allow_html=True,
        )
        try:
            sql = generate_sql(question)
            sql = fix_sql(sql)
            df = run_query(sql)

            # Chart — full width on top
            st.markdown(
                '<div class="section-card"><div class="section-title">📈 Visualisation</div>',
                unsafe_allow_html=True,
            )
            chart_type = suggest_chart(df)
            render_chart(df, chart_type, question)
            st.markdown("</div>", unsafe_allow_html=True)

            # SQL + Data — side by side below
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown(
                    '<div class="section-card"><div class="section-title">🔎 Generated SQL QUERY</div>',
                    unsafe_allow_html=True,
                )
                st.code(sql, language="sql")
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown(
                    '<div class="section-card"><div class="section-title">📋 Raw Data</div>',
                    unsafe_allow_html=True,
                )
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ {str(e)}")
            st.info("💡 Try rephrasing your question.")
