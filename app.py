from flask import Flask, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mediminders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_super_secret_key_here'
db = SQLAlchemy(app)

# Review Model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"<Review {self.name}>"

# Contact Us Model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Contact {self.name}>"

# User Model (for Sign Up/Sign In)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

# Home Route
@app.route("/")
def home():
    reviews = Review.query.all()
    return render_template("index.html", reviews=reviews)

# Write Review Page
@app.route("/write_review")
def write_review():
    return render_template("review.html")

# Submit Review
@app.route("/submit_review", methods=["POST"])
def submit_review():
    name = request.form.get("name")
    comment = request.form.get("comment")
    new_review = Review(name=name, comment=comment)
    db.session.add(new_review)
    db.session.commit()
    return redirect(url_for('home'))

# Contact Us Page
@app.route("/contact_us")
def contact_us():
    return render_template("contact_us.html")

# Submit Contact
@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    new_contact = Contact(name=name, email=email, message=message)
    db.session.add(new_contact)
    db.session.commit()
    return redirect(url_for('home'))

# Sign Up Page
@app.route("/signup")
def signup():
    return render_template("signup.html")

# Submit Sign Up
@app.route("/submit_signup", methods=["POST"])
def submit_signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('signin'))

# Sign In Page
@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/submit_signin", methods=["POST"])
def submit_signin():
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        session['user_id'] = user.id
        session['username'] = user.username 
        return redirect(url_for('home'))
    else:
        return "Invalid credentials", 401
# Review Page (shows all reviews)
@app.route("/review")
def review():
    reviews = Review.query.all()
    return render_template("review.html", reviews=reviews)

@app.route("/logout")
def logout():
    # Remove the user information from the session if it's there
    session.pop('user_id', None)
    session.pop('username', None) # Clear any other relevant session data
    return redirect(url_for('home')) # Redirect to the home page after logout

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)