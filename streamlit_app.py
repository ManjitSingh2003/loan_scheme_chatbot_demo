
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Loan Scheme Recommender (Demo)", layout="centered")

DATA_PATH = Path(__file__).parent / "loan_schemes.csv"

@st.cache_data
def load_schemes(path):
    return pd.read_csv(path)

# Simple recommendation function
def recommend(answers, loan_df):
    purpose = str(answers.get('purpose','')).strip().lower()
    try:
        loan_amount = float(str(answers.get('loan_amount','0')).replace(',','').strip())
    except:
        loan_amount = 0.0
    try:
        monthly_income = float(str(answers.get('monthly_income','0')).replace(',','').strip())
    except:
        monthly_income = 0.0
    try:
        tenure = int(str(answers.get('tenure','0')).strip())
    except:
        tenure = 0

    df = loan_df.copy()

    # Purpose matching (simple)
    def purpose_match(purpose_tags):
        tags = [t.strip().lower() for t in str(purpose_tags).split(';') if t.strip()!='']
        if not tags:
            return True
        if purpose=='' or purpose is None:
            return True
        return (purpose in tags) or any(p in purpose for p in tags) or any(p in tags for p in purpose.split()) or ('any' in tags)

    df['purpose_ok'] = df['purpose_tags'].apply(purpose_match)
    df = df[df['purpose_ok']]

    # Income filter
    def income_ok(row):
        min_inc = row.get('eligibility_income_min_monthly', 0)
        max_inc = row.get('eligibility_income_max_monthly', None)
        if pd.isna(min_inc):
            min_inc = 0
        if pd.isna(max_inc):
            max_inc = 1e18
        return (monthly_income >= float(min_inc)) and (monthly_income <= float(max_inc))

    df = df[df.apply(income_ok, axis=1)]

    # Loan amount filter
    def loan_ok(row):
        min_l = row.get('loan_amount_min', 0)
        max_l = row.get('loan_amount_max', None)
        if pd.isna(min_l):
            min_l = 0
        if pd.isna(max_l):
            max_l = 1e18
        return (loan_amount >= float(min_l)) and (loan_amount <= float(max_l))

    df = df[df.apply(loan_ok, axis=1)]

    # Tenure filter (if provided)
    if tenure > 0 and 'tenure_min_months' in df.columns:
        def tenure_ok(row):
            min_t = row.get('tenure_min_months', None)
            max_t = row.get('tenure_max_months', None)
            if pd.isna(min_t) and pd.isna(max_t):
                return True
            if pd.isna(min_t):
                min_t = 0
            if pd.isna(max_t):
                max_t = 1e9
            return (tenure >= float(min_t)) and (tenure <= float(max_t))
        df = df[df.apply(tenure_ok, axis=1)]

    if df.empty:
        return []

    # Scoring function (prefer closer loan amount and lower interest)
    def score(row):
        score = 0.0
        min_l = row.get('loan_amount_min', 0) if not pd.isna(row.get('loan_amount_min', None)) else 0
        max_l = row.get('loan_amount_max', 1e9) if not pd.isna(row.get('loan_amount_max', None)) else 1e9
        # loan amount proximity: smaller deviation is better
        if loan_amount < min_l:
            dev = (min_l - loan_amount) / (min_l + 1)
            score -= dev * 10
        elif loan_amount > max_l:
            dev = (loan_amount - max_l) / (max_l + 1)
            score -= dev * 10
        # interest penalty (lower interest better)
        ir = row.get('interest_rate_annual_percent', 100)
        if pd.isna(ir):
            ir = 100
        score -= float(ir) / 100.0
        return score

    df['score'] = df.apply(score, axis=1)
    df = df.sort_values('score', ascending=False)
    return df.head(3).to_dict('records')


def main():
    st.title("Loan Scheme Recommender — Demo")
    st.write("A simple rule-based demo to show the pipeline. Fill the short form to get recommendations. (Demo only)")

    # Load schemes (file must be next to this script)
    if not DATA_PATH.exists():
        st.error(f"Could not find loan_schemes.csv next to the app. Please place the CSV file at: {DATA_PATH}")
        return
    loan_df = load_schemes(DATA_PATH)

    # Simple form-based conversation
    with st.form("loan_form"):
        purpose = st.text_input("Purpose of loan (e.g., business, education, personal, agriculture)")
        loan_amount = st.text_input("Loan amount you're looking for (INR)")
        monthly_income = st.text_input("Your monthly income (INR)")
        tenure = st.number_input("Preferred tenure (months). Enter 0 to skip", min_value=0, value=0, step=1)
        submitted = st.form_submit_button("Get recommendations")
    if submitted:
        answers = {'purpose': purpose, 'loan_amount': loan_amount, 'monthly_income': monthly_income, 'tenure': int(tenure)}
        st.write("**Your answers:**")
        st.write(answers)
        st.write("**Top recommendations:**")
        recs = recommend(answers, loan_df)
        if not recs:
            st.info("No matching schemes found for the provided inputs. Try widening loan amount/income/tenure or check CSV entries.")
        else:
            for r in recs:
                st.markdown(f"### {r.get('scheme_name','Unnamed Scheme')}")
                st.markdown(f"- **Purpose tags:** {r.get('purpose_tags','')}")
                try:
                    lam = int(r.get('loan_amount_min',0))
                    maxl = int(r.get('loan_amount_max',0))
                    st.markdown(f"- **Loan range:** ₹{lam:,} — ₹{maxl:,}")
                except:
                    st.markdown(f"- **Loan range:** {r.get('loan_amount_min','')} — {r.get('loan_amount_max','')}")
                st.markdown(f"- **Tenure (months):** {int(r.get('tenure_min_months',0))} — {int(r.get('tenure_max_months',0))}")
                st.markdown(f"- **Interest (annual):** {r.get('interest_rate_annual_percent','')}%")
                st.markdown(f"- **Notes:** {r.get('notes','')}")
                st.write("---")

    st.sidebar.header("About (Demo)")
    st.sidebar.write("This is a lightweight demo to show the idea. It's rule-based and intended as a concept proof to take to stakeholders.")

if __name__ == '__main__':
    main()
