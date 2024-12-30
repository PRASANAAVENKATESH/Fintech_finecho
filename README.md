# Customized GPT Interface for Data Interaction, Analysis, and Visualization

## Overview
This project aims to make data interaction, analysis, and visualization more intuitive and efficient. By integrating a customized GPT interface, users can ask questions directly about their datasets and receive accurate, context-aware responses. The interface also supports dynamic visualizations to enhance the data exploration experience.

## Features
- *Natural Language Querying*: Interact with your dataset using natural language questions.
- *Context-Aware Responses*: Get precise and relevant answers tailored to your data.
- *Dynamic Visualizations*: Generate visualizations like bar charts, line graphs, and heatmaps dynamically based on your queries.
- *Seamless Integration*: Combines GPT's language capabilities with data analysis and visualization libraries.

## Technology Stack
- *Backend*: Python, Flask
- *Frontend*: Streamlit, HTML, CSS
- *Data Analysis*: Pandas, NumPy
- *Visualization*: Matplotlib, Seaborn
- *AI Integration*: OpenAI GPT, Google Generative AI

## Installation

### Prerequisites
- Python 3.8+
- Virtual Environment (recommended)
- Internet connection for API access

### Steps
1. Clone the repository:
   bash
   git clone https://github.com/your-repo/custom-gpt-interface.git
   cd custom-gpt-interface
   

2. Create and activate a virtual environment:
   bash
   python -m venv myenv
   source myenv/bin/activate  # macOS/Linux
   .\myenv\Scripts\activate  # Windows
   

3. Install dependencies:
   bash
   pip install -r requirements.txt
   

4. Set up API keys for OpenAI and Google Generative AI:
   - Create a .env file in the root directory.
   - Add the following keys:
     env
     GOOGLE_GENERATIVE_AI_KEY=your_google_api_key
     

5. Run the application:
   bash
   python main.py
   

6. Access the interface in your browser at:
   
http://localhost:5000
   

## Usage
1. Upload your dataset in CSV format.
2. Ask questions about your data in natural language.
3. View responses and dynamically generated visualizations.

## Example Queries
- "What is the average loan amount by year?"
- "Show a bar chart of loan counts by purpose."
- "What percentage of loans are considered high risk?"

## Folder Structure

custom-gpt-interface/
├── src/
│   ├── preprocess.py       # Handles data preprocessing
│   ├── datavisualizer.py   # Generates visualizations
│   ├── risk.py             # Performs risk analysis
├── templates/
│   ├── gpt.html            # Frontend for GPT interface
├── app.py                  # Visualization entry point
├── main.py                 # Flask application
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation


## Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.
