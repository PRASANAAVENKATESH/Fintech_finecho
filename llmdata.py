"""
import pandas as pd
import os
from num2words import num2words
def perform_eda(file_path):
    # Load the data from file
    df = pd.read_csv(file_path)

    # Preprocess the data if needed (e.g., handle missing values)
    df = preprocess_data(df)

    # Convert numerical columns to words
    df = convert_numerical_to_words(df)

    # Perform any additional EDA tasks (if needed)
    return df

def preprocess_data(df):
    # Example preprocessing steps (e.g., imputation)
    df.fillna(0, inplace=True)  # Replace NaN values with 0
    return df

def convert_numerical_to_words(df):
    for col in df.select_dtypes(include=['float', 'int']).columns:
        try:
            # Convert column values to numeric type, handling errors
            numeric_values = pd.to_numeric(df[col], errors='coerce')
            # Apply num2words to valid numeric values
            df[col] = numeric_values.apply(lambda x: num2words(x) if pd.notnull(x) else x)
        except ValueError:
            print(f"Error converting values in column '{col}' to numeric type")

    return df

# Example usage:
upload_folder = "uploads"
files = os.listdir(upload_folder)

if len(files) > 0:
    file_path = os.path.join(upload_folder, files[0])  # Assuming only one file is present
    eda_result = perform_eda(file_path)
    eda_result_str = eda_result.to_string(index=False)
    print(eda_result_str)  # Print the processed DataFrame to console
    # Write processed data to a text file
    with open('llmdata.txt', 'w') as f:
        f.write(eda_result_str)
    print("Processed data has been written to llmdata.txt")
else:
    print("No data available in the 'uploads' folder.")
"""
