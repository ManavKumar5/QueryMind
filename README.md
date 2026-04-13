# QueryMind
# ⚡ QueryMind — AI Sales Intelligence

> Ask any business question in plain English. Get instant SQL, charts, and insights — powered by **Llama 3.3** via **Groq** and **Streamlit**.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=flat-square&logo=postgresql)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🧠 What is QueryMind?

QueryMind is an AI-powered sales analytics dashboard that converts plain English questions into PostgreSQL queries and renders the results as interactive charts — no SQL knowledge required.

**Example questions you can ask:**
- *"Which category has the highest profit?"*
- *"Show monthly sales trend in 2024"*
- *"Rank cities by profit within each region"*
- *"Show month over month sales growth"*

---

## 🚀 Live Demo

🔗 [querymind.streamlit.app](https://querymind-14.streamlit.app/)

---

## ✨ Features

- **Natural Language → SQL** — Llama 3.3 (70B) generates advanced PostgreSQL queries including CTEs, window functions, subqueries, and aggregations
- **Auto Visualization** — Automatically selects the best chart type (bar, line, scatter, or metric card) based on the result shape
- **Smart SQL Fixes** — Post-processes AI-generated SQL to fix common PostgreSQL type errors automatically
- **16 Example Queries** — Sidebar shortcuts for instant exploration
- **50,000 Sales Records** — 2 years of Indian e-commerce data across 16 cities, 8 categories

---

## 🗄️ Dataset Overview

| Property | Details |
|---|---|
| Records | 50,000 orders |
| Date Range | January 2023 – December 2024 |
| Cities | Mumbai, Delhi, Bangalore, Chennai, Hyderabad, Pune, Ahmedabad, Surat, Jaipur, Lucknow, Chandigarh, Kochi, Kolkata, Bhubaneswar, Patna, Guwahati |
| Categories | Electronics, Fashion, Home & Kitchen, Sports, Books, Beauty, Toys, Grocery |
| Segments | Retail, Wholesale, Corporate |
| Payment Methods | UPI, Credit Card, Debit Card, Net Banking, Cash on Delivery, EMI |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| AI Model | Llama 3.3 70B via Groq API |
| Database | PostgreSQL (Supabase / Neon / any cloud PG) |
| Charts | Plotly |
| ORM | SQLAlchemy + psycopg2 |
| Language | Python 3.12 |

---

## 📁 Project Structure

```
QueryMind/
├── app.py              # Main application — all logic in one file
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not committed)
├── .env.example        # Template for environment variables
└── README.md
```

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/ManavKumar5/QueryMind.git
cd QueryMind
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_NAME=your_db_name
```

> Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 5. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ☁️ Deploy on Streamlit Community Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"** → select your repo and `app.py`
4. Add your environment variables under **"Advanced settings → Secrets"**:

```toml
GROQ_API_KEY = "your_groq_api_key"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
DB_HOST = "your_db_host"
DB_NAME = "your_db_name"
```

5. Click **Deploy**

---

## 📦 requirements.txt

```
streamlit
sqlalchemy
psycopg2-binary
groq
plotly
pandas
python-dotenv
```

---

## 🧩 How It Works

```
User Question (English)
        ↓
  Groq API (Llama 3.3 70B)
        ↓
  Raw SQL Generated
        ↓
  fix_sql() — auto-patches type errors
        ↓
  PostgreSQL Query Executed
        ↓
  suggest_chart() — picks best chart type
        ↓
  Plotly Chart + Data Table rendered
```

---

## 🐛 Known Fixes Applied

| Issue | Fix |
|---|---|
| `ROUND(double precision, int)` not supported | Auto-casts to `ROUND(expr::NUMERIC, 2)` |
| `EXTRACT` fails on text date column | Auto-casts to `order_date::DATE` |
| Reserved words used as SQL aliases | Auto-renames to suffixed aliases (`rank_val`, etc.) |

---

## 👤 Author

**Manav Kumar** — Data Analyst

---

## 📄 License

This project is licensed under the MIT License.
