import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
import numpy as np
import plotly.graph_objs as go
from plotly.offline import iplot
import pandas as pd

class Datavisualizer:
    def __init__(self, df):
        self.df = df
    
    def plot_average_loan_amount_by_year(self):
        # Check if necessary columns are present in the DataFrame
        required_columns = ['year', 'loan_amount']
        if all(col in self.df.columns for col in required_columns):
            plt.figure(figsize=(12, 8))

            # Use seaborn's barplot to visualize the average loan amount per year
            sns.barplot(x='year', y='loan_amount', data=self.df, palette='tab10')

            # Set plot title and axis labels
            plt.title('Issuance of Loans', fontsize=16)
            plt.xlabel('Year', fontsize=14)
            plt.ylabel('Average Loan Amount Issued', fontsize=14)

            # Show the plot
            plt.show()
        else:
            print("Error: Required columns ('year', 'loan_amount') not found in DataFrame.")
    def plot_loan_conditions(self):
        f, ax = plt.subplots(1, 2, figsize=(16, 8))
        colors = ["#3791D7", "#D72626"]
        labels = "Good Loans", "Bad Loans"
        plt.suptitle('Information on Loan Conditions', fontsize=20)
        required_columns = ['loan_condition', 'year', 'loan_amount']
        if all(col in self.df.columns for col in required_columns):

            self.df["loan_condition"].value_counts().plot.pie(explode=[0, 0.25], autopct='%1.2f%%', ax=ax[0],
                                                              shadow=True, colors=colors, labels=labels,
                                                              fontsize=12, startangle=70)
            ax[0].set_ylabel('% of Condition of Loans', fontsize=14)
            palette = ["#3791D7", "#E01E1B"]
            sns.barplot(x="year", y="loan_amount", hue="loan_condition", data=self.df, palette=palette,
                        estimator=lambda x: len(x) / len(self.df) * 100, ax=ax[1])
            ax[1].set_ylabel('(%)')

            plt.show()
        else:
            print("Error: Required columns ('loan_condition', 'year', 'loan_amount') not found in DataFrame.")
        
    def plot_loan_amount_over_time(self):
        required_columns = ['issue_year', 'region', 'loan_amount']
        if all(col in self.df.columns for col in required_columns):
            by_issued_amount = self.df.groupby(['issue_year', 'region'])['loan_amount'].sum()
            by_issued_amount.unstack().plot(kind='line', figsize=(15, 6))
            plt.title('Loans Issued by Region Over Time', fontsize=16)
            plt.xlabel('Year', fontsize=14)
            plt.ylabel('Total Loan Amount (in thousands)', fontsize=14)
            plt.legend(title='Region', title_fontsize='large', fontsize='medium', loc='upper left')
            plt.grid(False) 
            plt.show()
        else:
            print("Error: Required columns ('issue_year', 'region', 'loan_amount') not found in DataFrame.")
    
    def plot_loan_type_by_grade_and_subgrade(self):
        required_columns = ['grade', 'sub_grade', 'loan_condition']
        
        # Validate if all required columns are present in the DataFrame
        if all(col in self.df.columns for col in required_columns):
            fig = plt.figure(figsize=(16, 12))
            ax1 = fig.add_subplot(221)
            ax2 = fig.add_subplot(222)
            cmap = plt.cm.coolwarm_r
            loans_by_grade = self.df.groupby(['grade', 'loan_condition']).size()
            loans_by_grade.unstack().plot(kind='bar', stacked=True, colormap=cmap, ax=ax1, grid=False)
            ax1.set_title('Type of Loans by Grade', fontsize=14)
            loans_by_subgrade = self.df.groupby(['sub_grade', 'loan_condition']).size()
            loans_by_subgrade.unstack().plot(kind='bar', stacked=True, colormap=cmap, ax=ax2, grid=False)
            ax2.set_title('Type of Loans by Sub-Grade', fontsize=14)

            plt.tight_layout()
            plt.show()
        else:
            print("Error: Required columns ('grade', 'sub_grade', 'loan_condition') not found in DataFrame.")
    
    def plot_loan_and_interest_by_credit_score(self):
        # Check if necessary columns are present in the DataFrame
        required_columns = ['year', 'grade', 'loan_amount', 'interest_rate']
        if all(col in self.df.columns for col in required_columns):
            f, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4))
            cmap = plt.cm.coolwarm

            # Group by 'year' and 'grade', then calculate mean loan amount and interest rate
            by_credit_score_loan = self.df.groupby(['year', 'grade'])['loan_amount'].mean().unstack()
            by_credit_score_loan.plot(legend=False, ax=ax1, colormap=cmap)
            ax1.set_title('Loans Issued by Credit Score', fontsize=14)

            by_credit_score_interest = self.df.groupby(['year', 'grade'])['interest_rate'].mean().unstack()
            by_credit_score_interest.plot(ax=ax2, colormap=cmap)
            ax2.set_title('Interest Rates by Credit Score', fontsize=14)

            # Adjust legend for better layout
            ax2.legend(bbox_to_anchor=(-1.0, -0.3, 1.7, 0.1), loc=5, prop={'size': 12},
                       ncol=7, mode="expand", borderaxespad=0.)

            plt.show()
        else:
            print("Error: Required columns ('year', 'grade', 'loan_amount', 'interest_rate') not found in DataFrame.")

    def plot_loan_impact_analysis(self):
        # Calculate interest_payments based on interest_rate
        self.df['interest_payments'] = np.where(self.df['interest_rate'] <= 13.23, 'Low', 'High')

        # Plot 1 - Impact of interest rate on loan condition
        plt.figure(figsize=(20, 10))
        palette = ['#009393', '#930000']
        
        plt.subplot(221)
        ax = sns.countplot(x='interest_payments', data=self.df, palette=palette, hue='loan_condition')
        ax.set_title('The impact of interest rate on the condition of the loan', fontsize=14)
        ax.set_xlabel('Level of Interest Payments', fontsize=12)
        ax.set_ylabel('Count')

        # Plot 2 - Impact of maturity date on interest rates
        plt.subplot(222)
        ax1 = sns.countplot(x='interest_payments', data=self.df, palette=palette, hue='term')
        ax1.set_title('The impact of maturity date on interest rates', fontsize=14)
        ax1.set_xlabel('Level of Interest Payments', fontsize=12)
        ax1.set_ylabel('Count')

        # Plot 3 - Distribution of loan amount based on interest payments
        plt.subplot(212)
        low = self.df['loan_amount'].loc[self.df['interest_payments'] == 'Low'].values
        high = self.df['loan_amount'].loc[self.df['interest_payments'] == 'High'].values
        ax2 = sns.distplot(low, color='#009393', label='Low Interest Payments', fit=norm, fit_kws={"color": "#483d8b"})
        ax3 = sns.distplot(high, color='#930000', label='High Interest Payments', fit=norm, fit_kws={"color": "#c71585"})
        plt.axis([0, 36000, 0, 0.00016])
        plt.legend()

        plt.show()

    def plot_loan_analysis(self,df):
        fig = plt.figure(figsize=(16, 12))

        ax1 = fig.add_subplot(221)
        ax2 = fig.add_subplot(222)
        ax3 = fig.add_subplot(212)

        cmap = plt.cm.coolwarm_r

        # Plot 1: Type of Loans by Grade
        loans_by_region = df.groupby(['grade', 'loan_condition']).size()
        loans_by_region.unstack().plot(kind='bar', stacked=True, colormap=cmap, ax=ax1, grid=False)
        ax1.set_title('Type of Loans by Grade', fontsize=14)

        # Plot 2: Type of Loans by Sub-Grade
        loans_by_grade = df.groupby(['sub_grade', 'loan_condition']).size()
        loans_by_grade.unstack().plot(kind='bar', stacked=True, colormap=cmap, ax=ax2, grid=False)
        ax2.set_title('Type of Loans by Sub-Grade', fontsize=14)

        # Plot 3: Average Interest rate by Loan Condition
        by_interest = df.groupby(['year', 'loan_condition'])['interest_rate'].mean()
        by_interest.unstack().plot(ax=ax3, colormap=cmap)
        ax3.set_title('Average Interest rate by Loan Condition', fontsize=14)
        ax3.set_ylabel('Interest Rate (%)', fontsize=12)

        plt.tight_layout()
        plt.show()
    def plot_condition_by_purpose(self):
        if 'purpose' not in self.df.columns:
            return "The 'purpose' column is not available in the dataframe."

        purpose_condition = round(pd.crosstab(self.df['loan_condition'], self.df['purpose']).apply(lambda x: x/x.sum() * 100), 2)

        purpose_bad_loans = purpose_condition.values[0].tolist()
        purpose_good_loans = purpose_condition.values[1].tolist()
        purpose = purpose_condition.columns

        bad_plot = go.Bar(
            x=purpose,
            y=purpose_bad_loans,
            name = 'Bad Loans',
            text='%',
            marker=dict(
                color='rgba(219, 64, 82, 0.7)',
                line = dict(
                    color='rgba(219, 64, 82, 1.0)',
                    width=2
                )
            )
        )

        good_plot = go.Bar(
            x=purpose,
            y=purpose_good_loans,
            name='Good Loans',
            text='%',
            marker=dict(
                color='rgba(50, 171, 96, 0.7)',
                line = dict(
                    color='rgba(50, 171, 96, 1.0)',
                    width=2
                )
            )
        )

        data = [bad_plot, good_plot]

        layout = go.Layout(
            title='Condition of Loan by Purpose',
            xaxis=dict(
                title=''
            ),
            yaxis=dict(
                title='% of the Loan',
            ),
            paper_bgcolor='#FFF8DC',
            plot_bgcolor='#FFF8DC',
            showlegend=True
        )

        fig = dict(data=data, layout=layout)
        iplot(fig, filename='condition_purposes')
        
    def plot_bad_loan_status_by_region(self):
        required_columns = ['region', 'loan_status']
        if not set(required_columns).issubset(self.df.columns):
            return f"The following columns are required but not available in the dataframe: {', '.join(set(required_columns) - set(self.df.columns))}"

        loan_status_cross = pd.crosstab(self.df['region'], self.df['loan_status'])
        charged_off = loan_status_cross['Charged Off'].values.tolist()
        default = loan_status_cross['Default'].values.tolist()
        not_meet_credit = loan_status_cross['Does not meet the credit policy. Status:Charged Off'].values.tolist()
        grace_period = loan_status_cross['In Grace Period'].values.tolist()
        short_pay = loan_status_cross['Late (16-30 days)'].values.tolist()
        long_pay = loan_status_cross['Late (31-120 days)'].values.tolist()

        charged = go.Bar(
            x=['MidWest', 'NorthEast', 'SouthEast', 'SouthWest', 'West'],
            y= charged_off,
            name='Charged Off',
            marker=dict(
                color='rgb(192, 148, 246)'
            ),
            text = '%'
        )

        defaults = go.Bar(
            x=['MidWest', 'NorthEast', 'SouthEast', 'SouthWest', 'West'],
            y=default,
            name='Defaults',
            marker=dict(
                color='rgb(176, 26, 26)'
            ),
            text = '%'
        )

        credit_policy = go.Bar(
            x=['MidWest', 'NorthEast', 'SouthEast', 'SouthWest', 'West'],
            y= not_meet_credit,
            name='Does not meet Credit Policy',
            marker = dict(
                color='rgb(229, 121, 36)'
            ),
            text = '%'
        )

        grace = go.Bar(
            x=['MidWest', 'NorthEast', 'SouthEast', 'SouthWest', 'West'],
            y= grace_period,
            name='Grace Period',
            marker = dict(
                color='rgb(147, 147, 147)'
            ),
            text = '%'
        )

        short_pays = go.Bar(
            x=['MidWest', 'NorthEast', 'SouthEast', 'SouthWest', 'West'],
            y= short_pay,
            name='Late Payment (16-30 days)', 
            marker = dict(
                color='rgb(246, 157, 135)'
            ),
            text = '%'
        )

        long_pays = go.Bar(
            x=['MidWest', 'NorthEast', 'SouthEast', 'SouthWest', 'West'],
            y= long_pay,
            name='Late Payment (31-120 days)',
            marker = dict(
                color = 'rgb(238, 76, 73)'
                ),
            text = '%'
        )

        data = [charged, defaults, credit_policy, grace, short_pays, long_pays]
        layout = go.Layout(
            barmode='stack',
            title = '% of Bad Loan Status by Region',
            xaxis=dict(title='US Regions')
        )

        fig = go.Figure(data=data, layout=layout)
        iplot(fig, filename='stacked-bar')
        
