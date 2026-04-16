# ⚖️ LexAI — Contract Clause Analyzer

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54-red?style=flat-square&logo=streamlit)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?style=flat-square&logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

> **AI-powered contract analysis system that detects 33 legal clause types and assesses contract risk instantly.**

---

## 🚀 Live Demo

🔗 (lexai-contract-analyzer-qmb2yfrwus8ryilmewbwtt.streamlit.app)

---

## 📌 Overview

LexAI is a capstone project that uses **Natural Language Processing** and **Multi-Label Classification** to automatically analyze legal contracts. Paste any contract text and the system will:

- ✅ Detect which of **33 legal clauses** are present or absent
- 🛡️ Assign a **Risk Score** (Low / Medium / High)
- 📊 Show a **visual risk meter** with missing clause details
- ⚡ Deliver results **instantly**

---

## 🎯 Features

| Feature | Description |
|---|---|
| **Clause Detection** | Detects 33 clause types using ML |
| **Risk Assessment** | Rule-based risk scoring system |
| **Visual Dashboard** | Clean dark UI with gold accents |
| **Risk Meter** | Color-coded bar (green/orange/red) |
| **Missing Clause List** | Shows exactly which risky clauses are absent |

---

## 🧠 How It Works

```
Contract Text (input)
        ↓
Text Cleaning & Preprocessing
        ↓
TF-IDF Vectorization (500 features)
        ↓
MultiOutputClassifier (Logistic Regression)
        ↓
33 Binary Predictions (Yes/No per clause)
        ↓
Risk Scoring Engine
        ↓
Results Dashboard
```

---

## 📊 Dataset

- **Name:** CUAD Master Clauses Dataset
- **Contracts:** 510 real commercial contracts
- **Columns:** 83 total (metadata + clause text + answers)
- **Clause Types:** 40 unique clauses (33 binary Yes/No)
- **Source:** [CUAD Dataset — Atticus Project](https://www.atticusprojectai.org/cuad)

---

## 🤖 Model Performance

| Model | Precision | Recall | F1 Score |
|---|---|---|---|
| Logistic Regression | 0.82 | 0.38 | 0.52 |
| LR + class_weight='balanced' ✅ | 0.55 | 0.80 | **0.65** |
| Random Forest + balanced | 0.89 | 0.54 | 0.67 |

**Selected Model:** Logistic Regression with `class_weight='balanced'` for best overall F1 and high recall.

---

## 🛡️ Risk Scoring Logic

| Missing High Risk Clauses | Risk Level |
|---|---|
| 0 — 3 | ✅ LOW RISK |
| 4 — 5 | ⚠️ MEDIUM RISK |
| 6 | 🔴 HIGH RISK |

**High Risk Clauses:** Cap On Liability, Anti-Assignment, Termination For Convenience, License Grant, Uncapped Liability, Governing Law

---

## 🗂️ Project Structure

```
lexai-contract-analyzer/
├── app.py                  # Streamlit web application
├── model.pkl               # Trained ML model
├── tfidf.pkl               # TF-IDF vectorizer
├── binary_cols.pkl         # Binary clause column names
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## ⚙️ Run Locally

```bash
# Clone the repository
git clone https://github.com/Jyoshith-22/lexai-contract-analyzer.git
cd lexai-contract-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

App will open at `http://localhost:8501`

---

## 📦 Requirements

```
streamlit
scikit-learn
pandas
numpy
```

---

## 🗺️ Project Phases

- ✅ **Phase 1** — Data Understanding & EDA
- ✅ **Phase 2** — Data Preprocessing & Feature Engineering
- ✅ **Phase 3** — Model Building & Evaluation
- ✅ **Phase 4** — Streamlit Web Application
- ✅ **Phase 5** — Capstone Paper Writing

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">
Built with ❤️ using Streamlit · CUAD Dataset · Scikit-learn
</div>
