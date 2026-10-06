from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import logging
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'capstone_secret_key_2025'

# Logging Setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATABASE = 'expenses.db'

def init_db():
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS expenses
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      amount REAL NOT NULL,
                      category TEXT NOT NULL,
                      date TEXT NOT NULL,
                      notes TEXT)''')
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database init error: {e}")

@app.route('/')
def index():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM expenses ORDER BY date DESC")
        expenses = c.fetchall()

        c.execute("SELECT SUM(amount) FROM expenses")
        total = c.fetchone()[0] or 0

        c.execute("SELECT category, SUM(amount) as total FROM expenses GROUP BY category")
        by_category = c.fetchall()
        conn.close()
        return render_template('index.html', expenses=expenses, total=total, by_category=by_category)
    except Exception as e:
        logger.error(f"Error fetching expenses: {e}")
        flash("Error loading data", "error")
        return render_template('index.html', expenses=[], total=0, by_category=[])

@app.route('/add', methods=['POST'])
def add_expense():
    try:
        title = request.form.get('title', '').strip()
        amount = float(request.form.get('amount', 0))
        category = request.form.get('category', '').strip()
        date = request.form.get('date') or datetime.now().strftime('%Y-%m-%d')
        notes = request.form.get('notes', '').strip()

        if not title or amount <= 0 or not category:
            flash("Please fill all required fields correctly!", "error")
            return redirect(url_for('index'))

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO expenses (title, amount, category, date, notes) VALUES (?,?,?,?,?)",
                  (title, amount, category, date, notes))
        conn.commit()
        conn.close()
        logger.info(f"Expense added: {title} - {amount}")
        flash("Expense added successfully!", "success")
    except ValueError:
        flash("Invalid amount entered!", "error")
    except Exception as e:
        logger.error(f"Error adding expense: {e}")
        flash("Failed to add expense", "error")
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_expense(id):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("DELETE FROM expenses WHERE id =?", (id,))
        conn.commit()
        conn.close()
        flash("Expense deleted!", "success")
        logger.info(f"Expense deleted: ID {id}")
    except Exception as e:
        logger.error(f"Error deleting expense: {e}")
        flash("Failed to delete", "error")
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()Python-capstone-expense-tracker>public>creat
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
