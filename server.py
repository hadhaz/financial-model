from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def calculate_years_to_target(monthly_salary, salary_growth_rate, investment_return, inflation_rate, target_savings,
                              saving_percentage, custom_expenses):
    saving_with_investment = 0
    years = 0

    while saving_with_investment < target_savings:
        years += 1
        for _ in range(12):
            target_savings *= (1 + inflation_rate / 12)  # Adjust for inflation
            saving_with_investment *= (1 + investment_return / 12)  # Apply investment return

            # Get expenses for the current year range
            current_expense = custom_expenses.get(years, custom_expenses[max(custom_expenses.keys())])

            # Deduct expenses and apply savings
            monthly_savings = max(0, (monthly_salary - current_expense) * saving_percentage)
            saving_with_investment += monthly_savings

            # Increase salary based on growth rate
            monthly_salary *= (1 + salary_growth_rate / 12)

        if years > 100:  # Prevent infinite loop
            return "Target savings may not be reachable within a reasonable timeframe."

    return f"You will reach your target savings in approximately {years} years."


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        monthly_salary = float(data['monthly_salary'])
        salary_growth_rate = float(data['salary_growth_rate']) / 100
        investment_return = float(data['investment_return']) / 100
        inflation_rate = float(data['inflation_rate']) / 100
        target_savings = float(data['target_savings'])
        saving_percentage = float(data['saving_percentage']) / 100
        custom_expenses = {int(k): float(v) for k, v in data['custom_expenses'].items()}  # Convert keys to int

        result = calculate_years_to_target(monthly_salary, salary_growth_rate, investment_return, inflation_rate,
                                           target_savings, saving_percentage, custom_expenses)
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Invalid input. Please enter numerical values.'})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)