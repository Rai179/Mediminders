from flask import Flask, render_template, request, redirect, url_for, session
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- Database Configuration (Strictly SQLite) ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mediminders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_super_secret_key_here'

db = SQLAlchemy(app)

# --- Models ---

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"<Review {self.name}>"

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Contact {self.name}>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

# --- Routes ---

@app.route("/")
def home():
    reviews = Review.query.all()
    return render_template("index.html", reviews=reviews)

@app.route("/write_review")
def write_review():
    return render_template("review.html")

@app.route("/submit_review", methods=["POST"])
def submit_review():
    name = request.form.get("name")
    comment = request.form.get("comment")
    new_review = Review(name=name, comment=comment)
    db.session.add(new_review)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/contact_us")
def contact_us():
    return render_template("contact_us.html")

@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    new_contact = Contact(name=name, email=email, message=message)
    db.session.add(new_contact)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/submit_signup", methods=["POST"])
def submit_signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('signin'))

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/submit_signin", methods=["POST"])
def submit_signin():
    email = request.form.get("email")
    password = request.form.get("password")
    # Note: In a real app, use Werkzeug to check hashed passwords!
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        session['user_id'] = user.id
        session['username'] = user.username 
        return redirect(url_for('home'))
    else:
        return "Invalid credentials", 401

@app.route("/review")
def review():
    reviews = Review.query.all()
    return render_template("review.html", reviews=reviews)

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # Simplified run command for local use
    app.run(debug=True)