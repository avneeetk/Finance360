import os
from flask import Flask, request, render_template_string
import openai
from dotenv import load_dotenv
import pandas as pd
import styles.css

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

def generate_financial_report(user_data, market_data):
    prompt = f"""
    Create a personalized financial report for a user with the following data:
    - Monthly Income: ${user_data['income']}
    - Monthly Expenses: ${user_data['expenses']}
    - Total Investments: ${user_data['investments']}
    - Total Debts: ${user_data['debts']}
    - Total Savings: ${user_data['savings']}
    - Financial Goals: {user_data['financial_goals']}
    - Risk Tolerance: {user_data['risk_tolerance']}

    Current market trends:
    - S&P 500: {market_data['S&P 500']}
    - Interest rates: {market_data['interest rates']}
    - Inflation: {market_data['inflation']}

    Provide a summary, analysis, and recommendations based on this data.
    """

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=500
    )
    
    report = response.choices[0].text.strip()
    return report

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_data = {
            'income': request.form['income'],
            'expenses': request.form['expenses'],
            'investments': request.form['investments'],
            'debts': request.form['debts'],
            'savings': request.form['savings'],
            'financial_goals': request.form['financial_goals'],
            'risk_tolerance': request.form['risk_tolerance']
        }
        
        market_data = {
            'S&P 500': 'up 2%',
            'interest rates': 'steady at 3.5%',
            'inflation': 'rising 1.2%'
        }
        
        report = generate_financial_report(user_data, market_data)
        return render_template_string("""
            <h1>Personalized Financial Report</h1>
            <pre>{{ report }}</pre>
            <a href="/">Generate Another Report</a>
        """, report=report)
    
    return render_template_string("""
        <form method="post">
            <label>Monthly Income: <input type="text" name="income"></label><br>
            <label>Monthly Expenses: <input type="text" name="expenses"></label><br>
            <label>Total Investments: <input type="text" name="investments"></label><br>
            <label>Total Debts: <input type="text" name="debts"></label><br>
            <label>Total Savings: <input type="text" name="savings"></label><br>
            <label>Financial Goals: <input type="text" name="financial_goals"></label><br>
            <label>Risk Tolerance: <input type="text" name="risk_tolerance"></label><br>
            <button type="submit">Generate Report</button>
        </form>
    """)

if __name__ == '__main__':
    app.run(debug=True)
