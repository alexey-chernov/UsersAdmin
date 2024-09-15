from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, User, Transaction

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Міграції бази даних
from flask_migrate import Migrate
migrate = Migrate(app, db)

# Головна сторінка з навігацією
@app.route('/')
def index():
    return render_template('base.html')

# Додати користувача
@app.route('/add_user_form')
def add_user_form():
    return render_template('add_user.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    if username:
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return "Ім'я користувача обов'язкове", 400

# Редагувати користувача
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.username = request.form['username']
        
        try:
            db.session.commit()
            return redirect('/get_users_form')
        except:
            return "Помилка при редагуванні користувача"
    
    return render_template('edit_user.html', user=user)

# Видалення користувача
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    try:
        # Видаляємо всі транзакції користувача
        Transaction.query.filter_by(user_id=user_id).delete()

        # Тепер видаляємо самого користувача
        db.session.delete(user)
        db.session.commit()
        return redirect('/get_users_form')
    except:
        db.session.rollback()
        return "Помилка при видаленні користувача та його транзакцій"

# Додати транзакцію
@app.route('/add_transaction_form')
def add_transaction_form():
    return render_template('add_transaction.html')

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    user_id = request.form.get('user_id')
    transaction_type = request.form.get('transaction_type')
    amount = request.form.get('amount')

    user = User.query.get(user_id)
    if user:
        new_transaction = Transaction(user_id=user.id, transaction_type=transaction_type, amount=float(amount))
        db.session.add(new_transaction)
        db.session.commit()
        return redirect(url_for('index'))
    return "Користувач не знайдений", 404

# Отримати користувача за ID
@app.route('/get_user_form')
def get_user_form():
    return render_template('get_user.html')

@app.route('/get_user', methods=['GET'])
def get_user():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if user:
        transactions = user.transactions
        return render_template('get_user.html', user=user, transactions=transactions)
    return "Користувач не знайдений", 404

# Отримати всіх користувачів
@app.route('/get_users_form')
def get_all_users_form():
    users = User.query.all()
    return render_template('get_all_users.html', users=users)

# Статистика
@app.route('/statistics_form')
def statistics_form():
    total_transactions = db.session.query(db.func.count(Transaction.id)).scalar()
    total_amount = db.session.query(db.func.sum(Transaction.amount)).scalar()
    return render_template('statistics.html', total_transactions=total_transactions, total_amount=total_amount)


if __name__ == '__main__':
    app.run(debug=True)
