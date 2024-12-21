from flask import Flask, request, redirect, url_for, session
import random
import string

app = Flask(__name__)

app.secret_key = "your_secret_key"  # For session management

# Approval data (In-memory for this example, use a database in production)
approvals = {}
approved_users = {}

# Admin password
ADMIN_PASSWORD = "Thewardonhere"

# Function to generate unique key
def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# User approval request
@app.route("/", methods=["GET", "POST"])
def approval_request():
    if request.method == "POST":
        # Generate unique approval key
        key = generate_key()

        # Check if the key is already approved or pending
        if key in approvals and approvals[key]["status"] == "approved":
            return redirect(url_for("approved"))

        # Add key to approvals as pending
        approvals[key] = {"status": "pending"}

        return f'''
        <html>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>Your Approval Key</h1>
                <p>This is your approval key: <strong>{key}</strong></p>
                <p>Your approval request is now pending.</p>
                <p>Contact admin and send the key here: 
                    <a href="https://www.facebook.com/The.drugs.ft.chadwick.67" target="_blank" style="text-decoration: none; color: blue;">Click here to contact Admin</a>
                </p>
                <br>
                <p>Need help? <a href="https://www.facebook.com/The.drugs.ft.chadwick.67" target="_blank" style="text-decoration: none; color: blue;">Contact Admin</a></p>
            </body>
        </html>
        '''
    
    return '''
    <html>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>Approval System</h1>
            <form method="POST">
                <button type="submit">Get Approval Key</button>
            </form>
        </body>
    </html>
    '''

# Admin panel for approving keys
@app.route("/admin", methods=["GET", "POST"])
def admin_panel():
    if request.method == "POST":
        admin_password = request.form["password"]
        if admin_password != ADMIN_PASSWORD:
            return "Invalid password, try again."
        
        action = request.form["action"]
        key = request.form["key"]
        
        if action == "approve":
            approvals[key]["status"] = "approved"
            approved_users[key] = {"status": "approved"}
        elif action == "delete":
            if key in approved_users:
                del approved_users[key]
            if key in approvals:
                del approvals[key]
        
        return redirect(url_for("admin_panel"))

    # Display approval requests
    approval_requests = ""
    for key, value in approvals.items():
        if value["status"] == "pending":
            approval_requests += f'''
            <p>Key: {key} - Pending Approval</p>
            <form method="POST">
                <input type="hidden" name="key" value="{key}">
                <input type="password" name="password" placeholder="Enter Admin Password">
                <button type="submit" name="action" value="approve">Approve</button>
                <button type="submit" name="action" value="delete">Delete</button>
            </form>
            <br>
            '''

    approved_list = ""
    for key in approved_users:
        approved_list += f'<p>{key} - Approved</p>'

    return f'''
    <html>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>Admin Panel</h1>
            <h2>Approval Requests</h2>
            {approval_requests}
            <h2>Approved Users</h2>
            {approved_list}
        </body>
    </html>
    '''

# User approval success page
@app.route("/approved")
def approved():
    return '''
    <html>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>Your request has been approved!</h1>
            <p>Now you can use the APK.</p>
        </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
