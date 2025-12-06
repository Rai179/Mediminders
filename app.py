# app.py
from flask import Flask, render_template

# Create the Flask application instance
app = Flask(__name__)

# 1. Main Route (The home page)
@app.route('/')
def index():
    # Flask automatically looks in the 'templates' folder for index.html
    return render_template('index.html')

# 2. Add placeholder routes for the other pages
# These correspond to the links we updated in index.html (e.g., {{ url_for('review') }})
@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/contact')
def contact_us():
    return render_template('contact_us.html')

@app.route('/signup')
def signup():
    return render_template('signup.html') # Assuming you have a signup.html

@app.route('/signin')
def signin():
    return render_template('signin.html') # Assuming you have a signin.html

# This allows you to run the app directly
if __name__ == '__main__':
    app.run(debug=True)