#from flask import Flask, render_template, request, redirect, session
#from routes.auth import auth
from flask import Flask, render_template, request, redirect, session
from db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# required for session
app.secret_key = "supersecretkey"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html', name='karan')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        print(username, password)
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return redirect("/")
        else:
            return "invalid username or password"
    return render_template('login.html')

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        hashed_password = generate_password_hash(request.form["password"])

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
        conn.commit()
        conn.close()
        return redirect("/login")
    return render_template('register.html')
    


if __name__ == "__main__":
    app.run(debug=True)