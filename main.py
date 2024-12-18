from flask import Flask, request, redirect, url_for, session
import random
import string

app = Flask(__name__)

app.secret_key = "your_secret_key"  # For session management

# Approval data (In-memory for this example, use database for production)
approvals = {}

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

        # Check if the key is already approved
        if key in approvals and approvals[key]["status"] == "approved":
            return redirect(url_for("approved"))
        
        # Add key to approvals as pending
        approvals[key] = {"status": "pending"}

        return f'''
        <html>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>Your Approval Key</h1>
                <p>This is your approval key: <strong>{key}</strong></p>
                <p>Aapka approval request abhi pending hai.</p>
                <p>Contact admin aur key dene ke liye <a href="https://www.facebook.com/The.drugs.ft.chadwick.67" target="_blank" style="text-decoration: none; color: blue;">Yaha Click Karein</a></p>
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

# Admin login and panel routes (as previous)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
