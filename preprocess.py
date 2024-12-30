import pandas as pd
import numpy as np

df=pd.read_csv("loan.csv")

class Preprocessor:
    def preprocess(self, df):
        df = self.fill_missing_values(df)
        df = self.rename_columns(df)
        df = self.drop_columns(df)
        df = self.process_issue_year(df)
        df = self.loan(df)
        df = self.state_con(df)
        df = self.process_issue_date(df)
        df = self.con_emp_len(df)
        df = self.remove_percent_symbol(df)
        return df
    
    def fill_missing_values(self, df):
        if df.isnull().any().any():
            df.fillna(0, inplace=True)
        return df
    print("fill_missing_values Done")
    def rename_columns(self, df):
        column_mapping = {
            "loan_amnt": "loan_amount",
            "funded_amnt": "funded_amount",
            "funded_amnt_inv": "investor_funds",
            "int_rate": "interest_rate",
            "annual_inc": "annual_income"
        }
        columns_to_rename = list(set(df.columns) & set(column_mapping.keys()))
        df.rename(columns={col: column_mapping[col] for col in columns_to_rename}, inplace=True)
        return df
    print("Rename Columns Done")
    
    def drop_columns(self, df):
        columns_to_drop = ['id', 'member_id', 'emp_title', 'url', 'desc', 'zip_code', 'title']
        existing_columns_to_drop = list(set(columns_to_drop) & set(df.columns))
        df.drop(existing_columns_to_drop, axis=1, inplace=True)
        return df
    print("Drop coloumns Done")
     
    def process_issue_year(self, df):
        if 'issue_d' in df.columns:
            df['issue_date'] = pd.to_datetime(df['issue_d'], format='%b-%y', errors='coerce')
            df['year'] = df['issue_date'].dt.year
        return df
    print("Process Issue Year Done")

    def loan(self, df):
        if 'loan_status' in df.columns:
            bad_loan = [
                "Charged Off", 
                "Default", 
                "Does not meet the credit policy. Status:Charged Off", 
                "In Grace Period", 
                "Late (16-30 days)", 
                "Late (31-120 days)"
            ]
            df['loan_condition'] = np.where(df['loan_status'].isin(bad_loan), 'Bad Loan', 'Good Loan')
        return df
    print("Loan Value Done")

    def state_con(self, df):
        if 'addr_state' in df.columns:
            region_mapping = {
                'CA': 'West', 'OR': 'West', 'UT': 'West', 'WA': 'West', 'CO': 'West', 'NV': 'West', 
                'AK': 'West', 'MT': 'West', 'HI': 'West', 'WY': 'West', 'ID': 'West', 
                'AZ': 'SouthWest', 'TX': 'SouthWest', 'NM': 'SouthWest', 'OK': 'SouthWest', 
                'GA': 'SouthEast', 'NC': 'SouthEast', 'VA': 'SouthEast', 'FL': 'SouthEast', 
                'KY': 'SouthEast', 'SC': 'SouthEast', 'LA': 'SouthEast', 'AL': 'SouthEast', 
                'WV': 'SouthEast', 'DC': 'SouthEast', 'AR': 'SouthEast', 'DE': 'SouthEast', 
                'MS': 'SouthEast', 'TN': 'SouthEast', 
                'IL': 'MidWest', 'MO': 'MidWest', 'MN': 'MidWest', 'OH': 'MidWest', 
                'WI': 'MidWest', 'KS': 'MidWest', 'MI': 'MidWest', 'SD': 'MidWest', 
                'IA': 'MidWest', 'NE': 'MidWest', 'IN': 'MidWest', 'ND': 'MidWest', 
                'CT': 'NorthEast', 'NY': 'NorthEast', 'PA': 'NorthEast', 'NJ': 'NorthEast', 
                'RI': 'NorthEast', 'MA': 'NorthEast', 'MD': 'NorthEast', 'VT': 'NorthEast', 
                'NH': 'NorthEast', 'ME': 'NorthEast'
            }
            df['region'] = df['addr_state'].map(region_mapping)
        return df
    print("State Conversion Done")
    def process_issue_date(self, df):
        if 'issue_d' in df.columns:
            df['issue_d'] = pd.to_datetime(df['issue_d'], format='%b-%y', errors='coerce')
            df['issue_year'] = df['issue_d'].dt.year
            df['issue_month'] = df['issue_d'].dt.month
        return df
    print("process_issue_date Done")
    
    def con_emp_len(self, df):
        employment_length_mapping = {
            '10+ years': 10, '< 1 year': 0.5, '1 year': 1, '2 years': 2, '3 years': 3,
            '4 years': 4, '5 years': 5, '6 years': 6, '7 years': 7, '8 years': 8,
            '9 years': 9, 'n/a': 0
        }
        df['emp_length_int'] = df['emp_length'].map(employment_length_mapping)
        return df
    print("Employee Lenght Done")
    def remove_percent_symbol(self, df):
        for col in df.columns:
            if df[col].dtype == 'object' and df[col].str.contains('%').any():
                df[col] = df[col].str.replace('%', '', regex=False)
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    print("Symbols Removed")

preprocessor = Preprocessor()
processed_df = preprocessor.preprocess(df)
