<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg">
  <img alt="Pavel Chirkin — Machine Learning & AI Research" src="assets/hero-dark.svg" width="100%">
</picture>

I build **credit-risk models** at Bank ZENIT and research **stereo-EEG signals** at the AI Lab of Plekhanov Russian University of Economics, together with clinicians from the Pirogov National Medical and Surgical Center. I care about leakage-free validation, calibrated probabilities and pipelines that re-run end to end.

[Selected work](#selected-work) · [Code](https://github.com/pv-afk/pv_afk) · [Telegram](https://t.me/pv_chirkin) · [Email](mailto:p.chirkin07@gmail.com)

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/section-01-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/section-01-light.svg">
  <img alt="01 — Focus" src="assets/section-01-dark.svg" width="100%">
</picture>

**Credit risk · Bank ZENIT** — Risk Analyst / Developer, IFRS 9 & Modelling · *Apr 2026 – now*<br>
PD model development and recalibration · a reproducible pipeline for credit-history predictors · monitoring of internal and external scores, including on the reject sample.

**Computational neuroscience · AI Lab, Plekhanov University** — Research Assistant · *Mar 2026 – now*<br>
Machine learning for localizing the epileptogenic zone from stereo-EEG. Co-author of a paper at **Neuro AI 2026**.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/research-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/research-light.svg">
  <img alt="Research pipeline: EDF → bipolar montage → windows & QC → DFA / HFO features → PyTorch model → per-channel output" src="assets/research-dark.svg" width="100%">
</picture>

<br><br>

<a id="selected-work"></a>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/section-02-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/section-02-light.svg">
  <img alt="02 — Selected Work" src="assets/section-02-dark.svg" width="100%">
</picture>

<a href="https://github.com/pv-afk/pv_afk/tree/main/projects/credit-scoring"><img alt="Credit Scoring — XGBoost macro-F1 0.71 vs 0.50 for Logistic Regression" src="assets/card-credit-scoring-dark.svg#gh-dark-mode-only" width="100%"></a>
<a href="https://github.com/pv-afk/pv_afk/tree/main/projects/credit-scoring"><img alt="Credit Scoring — XGBoost macro-F1 0.71 vs 0.50 for Logistic Regression" src="assets/card-credit-scoring-light.svg#gh-light-mode-only" width="100%"></a>

Two joined credit-bureau tables → stratified split, imputation and one-hot encoding, class rebalancing, `RandomizedSearchCV` for Logistic Regression vs XGBoost. XGBoost reaches **macro-F1 0.71 / accuracy 0.80** on 10,268 held-out applicants (LogReg: 0.50 / 0.56). → [notebook](https://github.com/pv-afk/pv_afk/tree/main/projects/credit-scoring)

<a href="https://github.com/pv-afk/pv_afk/tree/main/projects/lead-prioritization"><img alt="Lead Prioritization — Daily Average Precision 0.760 vs 0.740 baseline on a local temporal holdout" src="assets/card-lead-prioritization-dark.svg#gh-dark-mode-only" width="100%"></a>
<a href="https://github.com/pv-afk/pv_afk/tree/main/projects/lead-prioritization"><img alt="Lead Prioritization — Daily Average Precision 0.760 vs 0.740 baseline on a local temporal holdout" src="assets/card-lead-prioritization-light.svg#gh-light-mode-only" width="100%"></a>

Avito DS Bootcamp. Only events before assignment time (`event_ts < assignment_ts`), recency and multi-window activity features (6 h – 60 d), a blend of two LightGBM variants, CatBoost and the base ensemble. **Daily AP 0.739 / 0.760** vs 0.714 / 0.740 baseline on two sequential local holdouts; the hidden test score is not known. → [code](https://github.com/pv-afk/pv_afk/tree/main/projects/lead-prioritization)

<a href="https://github.com/pv-afk/pv_afk/tree/main/projects/pharmacy-analysis"><img alt="Product Matching — best F1 0.69 with character 5-grams and Jaccard threshold 0.50" src="assets/card-product-matching-dark.svg#gh-dark-mode-only" width="100%"></a>
<a href="https://github.com/pv-afk/pv_afk/tree/main/projects/pharmacy-analysis"><img alt="Product Matching — best F1 0.69 with character 5-grams and Jaccard threshold 0.50" src="assets/card-product-matching-light.svg#gh-light-mode-only" width="100%"></a>

Parametric keys (dose, volume, pack size via regex) vs character n-gram Jaccard similarity, with the threshold tuned on precision / recall / F1. Best: **F1 0.69** (n = 5, threshold 0.50); the write-up argues for a hybrid of both. → [notebook](https://github.com/pv-afk/pv_afk/tree/main/projects/pharmacy-analysis)

<a href="https://github.com/pv-afk/pv_afk/tree/main/projects/average-salary"><img alt="Salary Forecast — SARIMAX on 399 monthly observations with a 36-month horizon" src="assets/card-salary-forecast-dark.svg#gh-dark-mode-only" width="100%"></a>
<a href="https://github.com/pv-afk/pv_afk/tree/main/projects/average-salary"><img alt="Salary Forecast — SARIMAX on 399 monthly observations with a 36-month horizon" src="assets/card-salary-forecast-light.svg#gh-light-mode-only" width="100%"></a>

Full statistical cycle: Box-Cox, seasonal differencing, `auto_arima` search, SARIMAX(6,1,2)(0,1,0)[12], inverse transform and a 36-month forecast. → [notebook](https://github.com/pv-afk/pv_afk/tree/main/projects/average-salary)

<sub>Also in the repo: [IT budget forecasting](https://github.com/pv-afk/pv_afk/tree/main/projects/cost-prediction) · [IT portfolio optimisation](https://github.com/pv-afk/pv_afk/tree/main/projects/it-portfolio) · [digital maturity analysis](https://github.com/pv-afk/pv_afk/tree/main/projects/it-strategy) · [ML foundations notebooks](https://github.com/pv-afk/pv_afk/tree/main/ML-AI). In progress: a local RAG copilot for credit analysts (hybrid FAISS + BM25 retrieval, cited answers) — code will be published when it is ready.</sub>

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/section-03-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/section-03-light.svg">
  <img alt="03 — Toolkit" src="assets/section-03-dark.svg" width="100%">
</picture>

**Modeling** — scikit-learn · XGBoost · CatBoost · LightGBM · imbalanced-learn · statsmodels · pmdarima<br>
**Signals** — MNE · pyEDFlib · SciPy · PyTorch (inference)<br>
**Data** — Python · SQL (PostgreSQL, MySQL, SQLite) · pandas · NumPy · Matplotlib<br>
**Familiar with** — Docker · MLflow · Airflow · PySpark · FastAPI · Streamlit · FAISS · Sentence Transformers

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/section-04-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/section-04-light.svg">
  <img alt="04 — Background" src="assets/section-04-dark.svg" width="100%">
</picture>

**BSc, Artificial Intelligence Systems & Technologies** — Plekhanov Russian University of Economics, 2024 – 2028<br>
Finalist, Plekhanov Case Club × Alfa-Bank case championship, 2026 · REA Data Science club, 2025 – 2026

**Contact** — [Telegram @pv_chirkin](https://t.me/pv_chirkin) · [p.chirkin07@gmail.com](mailto:p.chirkin07@gmail.com)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/footer-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/footer-light.svg">
  <img alt="" src="assets/footer-dark.svg" width="100%">
</picture>
