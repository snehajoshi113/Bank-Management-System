# bank_web_app.py
# Run: python bank_web_app.py
# Open: http://127.0.0.1:5000

from flask import Flask, request, render_template_string
import csv
import os

app = Flask(__name__)

DATA_DIR = "data"
FILE = os.path.join(DATA_DIR, "accounts.csv")

# Create data folder and CSV if not exists
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(FILE):
    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["AccountNumber", "Name", "Balance"])

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Bank Management System</title>
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
                        url('https://images.unsplash.com/photo-1601597111158-2fceff292cdc?auto=format&fit=crop&w=1600&q=80');
            background-size: cover;
            min-height: 100vh;
        }
        .container {
            width: 85%;
            max-width: 1100px;
            margin: 40px auto;
            background: rgba(255,255,255,0.95);
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        h1 { text-align: center; font-size: 38px; }
        .subtitle { text-align: center; color: #555; margin-bottom: 25px; }
        .menu {
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
        }
        .menu a {
            text-decoration: none;
            padding: 12px 22px;
            background: #007bff;
            color: white;
            border-radius: 30px;
            font-weight: bold;
        }
        hr { margin: 25px 0; }
        input, button {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            font-size: 16px;
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        button {
            background: #28a745;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 12px;
            text-align: center;
        }
        th { background: #007bff; color: white; }
        .msg { color: green; font-weight: bold; }
        .err { color: red; font-weight: bold; }
    </style>
</head>
<body>
<div class="container">
    <h1>🏦 Bank Management System</h1>
    <p class="subtitle">Secure • Simple • Smart Banking</p>

    <div class="menu">
        <a href="/">Home</a>
        <a href="/create">Create Account</a>
        <a href="/deposit">Deposit</a>
        <a href="/withdraw">Withdraw</a>
        <a href="/accounts">View Accounts</a>
    </div>

    <hr>
    {{ content | safe }}
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, content="""
        <p>Welcome to the Bank Management System Web Application.</p>
        <p>Use the menu buttons above to manage accounts.</p>
    """)

@app.route("/create", methods=["GET", "POST"])
def create():
    msg = ""
    if request.method == "POST":
        acc = request.form["acc"]
        name = request.form["name"]
        bal = request.form["bal"]

        with open(FILE, "a", newline="") as f:
            csv.writer(f).writerow([acc, name, bal])

        msg = "<p class='msg'>Account created successfully!</p>"

    return render_template_string(HTML, content=f"""
        {msg}
        <form method="post">
            <input name="acc" placeholder="Account Number" required>
            <input name="name" placeholder="Account Holder Name" required>
            <input name="bal" placeholder="Initial Balance" required>
            <button>Create Account</button>
        </form>
    """)

@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    msg = ""
    if request.method == "POST":
        acc = request.form["acc"]
        amt = float(request.form["amt"])

        rows = []
        with open(FILE) as f:
            for r in csv.reader(f):
                if r and r[0] == acc and r[0] != "AccountNumber":
                    r[2] = str(float(r[2]) + amt)
                rows.append(r)

        with open(FILE, "w", newline="") as f:
            csv.writer(f).writerows(rows)

        msg = "<p class='msg'>Deposit successful!</p>"

    return render_template_string(HTML, content=f"""
        {msg}
        <form method="post">
            <input name="acc" placeholder="Account Number" required>
            <input name="amt" placeholder="Deposit Amount" required>
            <button>Deposit</button>
        </form>
    """)

@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():
    msg = ""
    if request.method == "POST":
        acc = request.form["acc"]
        amt = float(request.form["amt"])

        rows = []
        for r in csv.reader(open(FILE)):
            if r and r[0] == acc and r[0] != "AccountNumber":
                bal = float(r[2])
                if bal >= amt:
                    r[2] = str(bal - amt)
                    msg = "<p class='msg'>Withdrawal successful!</p>"
                else:
                    msg = "<p class='err'>Insufficient balance!</p>"
            rows.append(r)

        with open(FILE, "w", newline="") as f:
            csv.writer(f).writerows(rows)

    return render_template_string(HTML, content=f"""
        {msg}
        <form method="post">
            <input name="acc" placeholder="Account Number" required>
            <input name="amt" placeholder="Withdraw Amount" required>
            <button>Withdraw</button>
        </form>
    """)

@app.route("/accounts")
def accounts():
    rows = list(csv.reader(open(FILE)))

    table = "<table><tr><th>Account No</th><th>Name</th><th>Balance</th></tr>"
    for r in rows[1:]:
        table += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
    table += "</table>"

    return render_template_string(HTML, content=table)

if __name__ == "__main__":
    app.run(debug=True)
