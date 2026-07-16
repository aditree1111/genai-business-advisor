
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from dotenv import load_dotenv
from google import genai
import os
import re

# ==========================
# Page Configuration
# ==========================

st.set_page_config(
    page_title="GenAI Business Advisor",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("📊 Project Overview")

st.sidebar.markdown("""
### Tech Stack

- Python
- Pandas
- Streamlit
- Google Gemini 3.5
- RAG
- Matplotlib

---

### Dataset

- Sample Superstore
- Apple 2025 Annual Report

---

### Project

GenAI Business Advisor

Built using:

- Python
- Streamlit
- Gemini 3.5 Flash
- Pandas
- Matplotlib
""")

# ==========================
# Project Paths
# ==========================

project_root = Path(__file__).resolve().parent.parent

# ==========================
# Load API Key
# ==========================

load_dotenv(project_root / ".env")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ==========================
# Load Business Dataset
# ==========================

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data(project_root / "data" / "SampleSuperstore.csv")

# ==========================
# KPI Calculations
# ==========================

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df.shape[0]

top_category = (
    df.groupby("Category")["Sales"]
    .sum()
    .idxmax()
)

top_region = (
    df.groupby("Region")["Sales"]
    .sum()
    .idxmax()
)

# ==========================
# Header
# ==========================

st.title("📊 GenAI Business Advisor")
st.success("🚀 AI-powered dashboard for business analytics and annual report analysis.")

st.write(
    "Analyze business data and ask questions about Apple's 2025 Annual Report using Gemini AI."
)
st.info("""
This application combines traditional business analytics with Retrieval-Augmented Generation (RAG).

Features:
- 📊 Sales KPI Dashboard
- 📈 Business Visualizations
- 🤖 AI Business Advisor powered by Gemini 3.5
- 📄 Apple 2025 Annual Report Question Answering
""")

# ==========================
# KPI Cards
# ==========================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("💰 Sales", f"${total_sales:,.2f}")

with col2:
    st.metric("📈 Profit", f"${total_profit:,.2f}")

with col3:
    st.metric("📦 Orders", total_orders)

with col4:
    st.metric("🏷️ Top Category", top_category)

with col5:
    st.metric("🌍 Top Region", top_region)

st.divider()

# ==========================
# Load Apple Report
# ==========================

@st.cache_data
def load_report():

    text_path = project_root / "documents" / "apple_report.txt"

    with open(text_path, "r", encoding="utf-8") as f:
        report_text = f.read()

    chunk_size = 1000

    return [
        report_text[i:i + chunk_size]
        for i in range(0, len(report_text), chunk_size)
    ]

chunks = load_report()

# ==========================
# Search Function
# ==========================

def search_chunks(query, chunks, top_k=3):

    query_words = re.findall(r"\w+", query.lower())

    scores = []

    for chunk in chunks:

        score = 0

        chunk_lower = chunk.lower()

        for word in query_words:
            score += chunk_lower.count(word)

        scores.append(score)

    ranked = sorted(
        zip(scores, chunks),
        reverse=True,
        key=lambda x: x[0]
    )

    return [
        chunk
        for score, chunk in ranked[:top_k]
        if score > 0
    ]

# ==========================
# AI Section
# ==========================

st.subheader("🤖 AI Business Advisor")

st.markdown("""
### Example Questions

- What are Apple's biggest risks?
- How does Apple generate revenue?
- What are Apple's growth opportunities?
- What challenges does Apple face?
""")

question = st.text_input(
    "Ask a question about Apple's Annual Report",
    placeholder="Example: What are Apple's biggest risks?"
)

if st.button("Generate Answer"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("Analyzing report..."):

            results = search_chunks(question, chunks)

            context = "\n\n".join(results)

            prompt = f"""
You are an experienced business strategy consultant.

Answer ONLY using the information below.

Context:
{context}

Question:
{question}

Please provide:

1. Executive Summary

2. Business Insight

3. Strategic Recommendation
"""

            try:

                response = client.models.generate_content(
                    model="models/gemini-3.5-flash",
                    contents=prompt
                )

                st.success("Analysis Complete!")
                st.subheader("🤖 AI Recommendation")
                st.write(response.text)

            except Exception as e:
                st.error(f"Error: {e}")


# ==========================
# Business Dashboard
# ==========================

st.divider()

st.header("📊 Business Dashboard")

col1, col2, col3 = st.columns(3)

# ----------------------------
# Sales by Category
# ----------------------------

category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

fig1, ax1 = plt.subplots(figsize=(5,4))
ax1.bar(category_sales.index, category_sales.values)
ax1.set_title("Sales by Category")
ax1.tick_params(axis="x", rotation=20)

with col1:
    st.pyplot(fig1)

# ----------------------------
# Profit by Region
# ----------------------------

region_profit = (
    df.groupby("Region")["Profit"]
    .sum()
)

fig2, ax2 = plt.subplots(figsize=(5,4))
ax2.bar(region_profit.index, region_profit.values)
ax2.set_title("Profit by Region")
ax2.tick_params(axis="x", rotation=20)

with col2:
    st.pyplot(fig2)

# ----------------------------
# Sales by Segment
# ----------------------------

segment_sales = (
    df.groupby("Segment")["Sales"]
    .sum()
)

fig3, ax3 = plt.subplots(figsize=(5,4))
ax3.pie(
    segment_sales.values,
    labels=segment_sales.index,
    autopct="%1.1f%%"
)
ax3.set_title("Sales by Segment")

with col3:
    st.pyplot(fig3)

st.divider()

st.header("📌 Key Business Insights")

st.success(f"""
• Highest Sales Category: **{top_category}**

• Highest Sales Region: **{top_region}**

• Total Sales: **${total_sales:,.2f}**

• Total Profit: **${total_profit:,.2f}**
""")
st.divider()

st.caption(
    "Built with Python, Pandas, Streamlit, Google Gemini 3.5 Flash and Matplotlib."
)