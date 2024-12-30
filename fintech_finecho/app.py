import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from src.preprocess import Preprocessor
from src.datavisualizer import Datavisualizer
from src.risk import RiskAnalysis

# Configure Gemini AI
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-pro')

def generate_gemini_insights(dataframe):
    """
    Generate Gemini AI-based insights for the given dataframe.
    """
    data_summary = dataframe.describe(include='all').to_string()

    prompt = f"""
    Analyze the following dataset and provide key insights:
    
    Dataset Summary:
    {data_summary}
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating insights: {str(e)}"

def apply_gradient_color(series):
    max_val = series.max()
    second_max_val = series[series < max_val].max() if series.nunique() > 1 else max_val
    styles = []
    
    for val in series:
        if val == max_val:
            styles.append('color: red')
        elif val == second_max_val:
            styles.append('color: orange')
        else:
            styles.append('color: blue')
    
    return styles

def main():
    st.title("Data Visualization and Insights")

    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        file_path = os.path.join(upload_folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"File {uploaded_file.name} uploaded successfully!")

        df = pd.read_csv(file_path, low_memory=False)

        if df.shape[1] > 48 and df.iloc[:, 48].dtype == 'object':
            st.write(f"Column 49 has mixed types. Inspecting unique values:")
            st.write(df.iloc[:, 48].unique())
            df.iloc[:, 48] = df.iloc[:, 48].astype(str)

        st.write('Data in the uploaded CSV file:')
        st.dataframe(df.head())

        # Preprocess data
        preprocessor = Preprocessor()
        processed_df = preprocessor.preprocess(df)

        st.subheader("Sample of Preprocessed Data")
        st.dataframe(processed_df.head())

        st.header("Visualizations")
        datavisualizer = Datavisualizer(df)

        st.subheader("Average Loan Amount by Year")
        datavisualizer.plot_average_loan_amount_by_year()
        st.pyplot()

        st.subheader("Loan Conditions")
        datavisualizer.plot_loan_conditions()
        st.pyplot()

        st.subheader("Loan Amount Over Time")
        datavisualizer.plot_loan_amount_over_time()
        st.pyplot()

        st.subheader("Loan Type by Grade and Sub-Grade")
        datavisualizer.plot_loan_type_by_grade_and_subgrade()
        st.pyplot()

        st.subheader("Loan and Interest by Credit Score")
        datavisualizer.plot_loan_and_interest_by_credit_score()
        st.pyplot()

        st.subheader("Loan Impact Analysis")
        datavisualizer.plot_loan_impact_analysis()
        st.pyplot()

        st.subheader("Loan Analysis")
        datavisualizer.plot_loan_analysis(df)
        st.pyplot()

        st.header("Loan Risk Analysis")
        risk_analysis = RiskAnalysis(df)
        loan_risk_df = risk_analysis.calculate_loan_analysis()

        styled_loan_risk_df = loan_risk_df.style.apply(
            apply_gradient_color, subset=['Bad Loan', 'Good Loan', 'Risk (%)']
        )
        st.dataframe(styled_loan_risk_df)

        st.header("Insights with Gemini AI")
        if st.button("Generate Insights"):
            insights = generate_gemini_insights(processed_df)
            st.text_area("Generated Insights", value=insights, height=200)

    else:
        st.write("No CSV file uploaded. Please upload a CSV file to proceed.")

if __name__ == '__main__':  # Fixed: Changed _name to __name__
    main()
