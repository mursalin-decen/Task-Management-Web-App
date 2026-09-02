import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_super_secret_key_12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ================= DATABASE MODELS =================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    tasks = db.relationship('Task', backref='author', lazy=True)
    categories = db.relationship('Category', backref='author', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tasks = db.relationship('Task', backref='category_rel', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(20), default='Medium') # Low, Medium, High
    status = db.Column(db.String(20), default='Pending')  # Pending, Completed
    due_date = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ================= ROUTES =================

@app.route('/')
def splash():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        
        # Add default categories for new user
        default_cats = ['Work', 'Personal', 'Study']
        for cat in default_cats:
            db.session.add(Category(name=cat, user_id=new_user.id))
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Email or Password', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    category_filter = request.args.get('category', '')

    tasks_query = Task.query.filter_by(user_id=current_user.id)

    if search_query:
        tasks_query = tasks_query.filter(Task.title.contains(search_query))
    if status_filter:
        tasks_query = tasks_query.filter_by(status=status_filter)
    if priority_filter:
        tasks_query = tasks_query.filter_by(priority=priority_filter)
    if category_filter:
        tasks_query = tasks_query.filter_by(category_id=category_filter)

    all_user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    tasks = tasks_query.all()
    categories = Category.query.filter_by(user_id=current_user.id).all()

    # Overview Metrics
    total_tasks = len(all_user_tasks)
    completed_tasks = len([t for t in all_user_tasks if t.status == 'Completed'])
    pending_tasks = len([t for t in all_user_tasks if t.status == 'Pending'])

    return render_template('dashboard.html', 
                           tasks=tasks, 
                           categories=categories,
                           total_tasks=total_tasks,
                           completed_tasks=completed_tasks,
                           pending_tasks=pending_tasks)

@app.route('/add-task', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title')
    priority = request.form.get('priority')
    due_date = request.form.get('due_date')
    category_id = request.form.get('category_id')

    if title:
        new_task = Task(
            title=title, 
            priority=priority, 
            due_date=due_date, 
            category_id=category_id if category_id else None,
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/toggle-task/<int:task_id>')
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        task.status = 'Completed' if task.status == 'Pending' else 'Pending'
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete-task/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted!', 'warning')
    return redirect(url_for('dashboard'))

@app.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    if request.method == 'POST':
        cat_name = request.form.get('name')
        if cat_name:
            db.session.add(Category(name=cat_name, user_id=current_user.id))
            db.session.commit()
            flash('Category added!', 'success')

    user_categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('categories.html', categories=user_categories)

@app.route('/delete-category/<int:cat_id>')
@login_required
def delete_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    if cat.user_id == current_user.id:
        db.session.delete(cat)
        db.session.commit()
        flash('Category deleted!', 'warning')
    return redirect(url_for('categories'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_profile':
            current_user.username = request.form.get('username')
            db.session.commit()
            flash('Profile updated!', 'success')
        elif action == 'change_password':
            old_pass = request.form.get('old_password')
            new_pass = request.form.get('new_password')
            if bcrypt.checkpw(old_pass.encode('utf-8'), current_user.password.encode('utf-8')):
                current_user.password = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                db.session.commit()
                flash('Password changed successfully!', 'success')
            else:
                flash('Incorrect old password!', 'danger')
    return render_template('profile.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)