import random
import string
from flask import Flask, request, redirect, url_for, session, make_response

app = Flask(__name__)

app.secret_key = "your_secret_key"  # Session ka key

# Approval ki data (yahan in-memory rakh rahe hain, production mein DB use kar)
approvals = {}

# Admin ka password
ADMIN_PASSWORD = "Thewardonhere"

# Unique key generate karne ka function
def generate_unique_key():
    length = 10  # Key ka length
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# User ka approval request
@app.route("/", methods=["GET", "POST"])
def approval_request():
    # Check kar rahe hain agar user ke pass already ek key hai cookies mein
    user_key = request.cookies.get("user_key")

    if not user_key:  # Agar key nahi hai, nayi generate karo
        user_key = generate_unique_key()
        resp = make_response(f"This is your approval key: {user_key}. Aapka approval request bhej diya gaya hai! Admin ki approval ka intezaar karein.")
        resp.set_cookie("user_key", user_key)  # Cookies mein key store karo
        approvals[user_key] = {"status": "pending"}
        return resp
    else:  # Agar user ke pass key hai, toh uska status dikhao
        if user_key in approvals and approvals[user_key]["status"] == "approved":
            return redirect(url_for("approved"))
        return f"This is your approval key: {user_key}. Aapka approval request abhi pending hai."

    return '''
    <html>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>Approval System</h1>
        <p>Yoour Approval Key send me :V.</p>
        <br>
        <p>Send me key here<a href="https://www.facebook.com/The.drugs.ft.chadwick.67" target="_blank" style="text-decoration: none; color: blue;">Admin se Contact karein</a></p>
    </body>
    </html>
    '''

# Admin login
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_panel"))
        else:
            return "Password galat hai. Phir se try karo."
    
    return '''
    <html>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>Admin Login</h1>
        <form method="POST">
            <input type="password" name="password" placeholder="Admin Password daalein" required>
            <button type="submit">Login</button>
        </form>
        <br>
        <p>Contact? <a href="https://www.facebook.com/The.drugs.ft.chadwick.67" target="_blank" style="text-decoration: none; color: blue;">Admin se Contact karein</a></p>
    </body>
    </html>
    '''

# Admin panel
@app.route("/admin", methods=["GET", "POST"])
def admin_panel():
    if "admin_logged_in" not in session:
        return redirect(url_for("admin_login"))
    
    if request.method == "POST":
        key = request.form.get("approval_key")
        action = request.form.get("action")
        if key in approvals:
            if action == "approve":
                approvals[key]["status"] = "approved"
            elif action == "reject":
                approvals[key]["status"] = "rejected"
    
    pending = {k: v for k, v in approvals.items() if v["status"] == "pending"}
    approved = {k: v for k, v in approvals.items() if v["status"] == "approved"}
    
    return f'''
    <html>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>Admin Panel</h1>
        <h2>Pending Approvals</h2>
        <ul>
            {''.join(f"<li>{key} <form method='POST' style='display: inline;'><input type='hidden' name='approval_key' value='{key}'><button name='action' value='approve'>Approve</button><button name='action' value='reject'>Reject</button></form></li>" for key in pending)}
        </ul>
        <h2>Approved Keys</h2>
        <ul>
            {''.join(f"<li>{key}</li>" for key in approved)}
        </ul>
        <br>
        <p>Madad chahiye? <a href="https://www.facebook.com/The.drugs.ft.chadwick.67" target="_blank" style="text-decoration: none; color: blue;">Admin se Contact karein</a></p>
    </body>
    </html>
    '''

# Page for approved users
@app.route("/approved")
def approved():
    return '''
    <html>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>Welcome, Your Approval Was accepted</h1>
        <p>Now Open Your Apk and Read All Descriptions</p>
        <button onclick="window.location.href='http://faizuapk.kesug.com/?i=1'">Apna APK kholo</button>
        <br><br>
        <p>Madad chahiye? <a href="https://www.facebook.com/The.drugs.ft.chadwick.67" target="_blank" style="text-decoration: none; color: blue;">Admin se Contact karein</a></p>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
