# Loan Scheme Recommender — Demo

This is a **demo Streamlit app** to recommend loan schemes based on simple eligibility criteria. It uses a CSV of sample schemes and applies basic rule-based filtering. Future improvements can include NLP-based recommendations, embeddings, and user history for better ranking.

## Files in this Repo

* **`streamlit_app.py`** — The Streamlit demo application.
* **`loan_schemes.csv`** — Sample loan schemes CSV file. Edit to add your own schemes.
* **`requirements.txt`** — Python packages required to run the app.

## Getting Started (Local Setup)

1. **(Optional) Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux / macOS
   venv\Scripts\activate         # Windows
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**:

   ```bash
   streamlit run streamlit_app.py
   ```

4. Open the link provided in the terminal to access the app in your browser.

## Customizing Loan Schemes

Edit **`loan_schemes.csv`** to add your own schemes. Keep the following columns intact:

* `scheme_id`
* `scheme_name`
* `purpose_tags`
* `eligibility_income_min_monthly`
* `eligibility_income_max_monthly`
* `loan_amount_min`
* `loan_amount_max`
* `tenure_min_months`
* `tenure_max_months`
* `interest_rate_annual_percent`
* `notes`

## Notes

* This is a **rule-based demo** — users are matched to schemes based on the eligibility and loan criteria.
* Future versions can include advanced features like:

  * NLP-based scheme search
  * Embeddings for better similarity matching
  * Personalized recommendations based on user history
