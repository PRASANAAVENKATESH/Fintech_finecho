import numpy as np
import pandas as pd
class RiskAnalysis:
    def __init__(self, df):
        self.df = df

    def calculate_loan_analysis(self):
        # Calculate loan counts based on income_category and purpose
        loan_count = self.df.groupby(['income_category', 'purpose'])['loan_condition'].value_counts().unstack(fill_value=0)

        # Rename columns for clarity
        loan_count.columns = ['Bad Loan', 'Good Loan']

        # Reset index to create a DataFrame
        loan_c_df = loan_count.reset_index()

        # Filter Good Loans and Bad Loans
        good_loans = loan_c_df.sort_values(by="income_category", ascending=True)  # Sorting is enough here
        bad_loans = loan_c_df.sort_values(by="income_category", ascending=True)  # Sorting is enough here

        # Merge good_loans and bad_loans based on income_category
        sort_group_income_purpose = pd.merge(good_loans[['income_category', 'purpose', 'Good Loan']],
                                             bad_loans[['income_category', 'purpose', 'Bad Loan']],
                                             on=['income_category', 'purpose'])

        # Calculate total loans issued and bad/good ratio (%)
        sort_group_income_purpose['total_loans_issued'] = sort_group_income_purpose['Good Loan'] + sort_group_income_purpose['Bad Loan']
        sort_group_income_purpose['Risk (%)'] = np.around((sort_group_income_purpose['Bad Loan'] / sort_group_income_purpose['total_loans_issued']) * 100, 2)

        # Sort by income_category
        final_df = sort_group_income_purpose.sort_values(by='income_category', ascending=True)

        return final_df