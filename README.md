Loan Scheme Recommender — Demo

Files created in this folder:
- streamlit_app.py  (Streamlit demo app)
- loan_schemes.csv  (Sample schemes CSV)
- requirements.txt  (Python packages to install)

How to run locally:
1. (Optional) Create a virtual environment:
   python -m venv venv
   source venv/bin/activate   # linux / mac
   venv\Scripts\activate    # windows

2. Install dependencies:
   pip install -r requirements.txt

3. Run the Streamlit app (from this folder):
   streamlit run streamlit_app.py

Notes:
- Edit loan_schemes.csv to add your own schemes. Keep columns:
  scheme_id,scheme_name,purpose_tags,eligibility_income_min_monthly,eligibility_income_max_monthly,loan_amount_min,loan_amount_max,tenure_min_months,tenure_max_months,interest_rate_annual_percent,notes
- The demo uses simple rule-based filtering. After approval we can add NLP, embeddings, user history and a better ranking algorithm.
