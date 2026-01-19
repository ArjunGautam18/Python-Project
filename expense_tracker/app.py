from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(10), nullable=False)

# Routes
@app.route('/')
def index():
    # Fetch all expenses to display on the home page
    expenses = Expense.query.all()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add_expense():
    # We only need to check if it's POST since that's the only method allowed for this route
    description = request.form.get('description')
    amount = float(request.form.get('amount', 0))
    date = request.form.get('date')
    
    if description and date:
        new_expense = Expense(description=description, amount=amount, date=date)
        db.session.add(new_expense)
        db.session.commit()
    
    return redirect('/')

if __name__ == '__main__':
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)