import csv

FILE = "data/accounts.csv"

def create_account():
    acc_no = input("Enter account number: ")
    name = input("Enter name: ")
    balance = input("Enter initial balance: ")

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([acc_no, name, balance])

    print("Account created successfully!")

def view_accounts():
    with open(FILE, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

def deposit():
    acc_no = input("Enter account number: ")
    amount = float(input("Enter amount to deposit: "))

    rows = []
    with open(FILE, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == acc_no:
                row[2] = str(float(row[2]) + amount)
            rows.append(row)

    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print("Amount deposited successfully!")

def withdraw():
    acc_no = input("Enter account number: ")
    amount = float(input("Enter amount to withdraw: "))

    rows = []
    with open(FILE, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == acc_no:
                balance = float(row[2])
                if balance >= amount:
                    row[2] = str(balance - amount)
                else:
                    print("Insufficient balance!")
            rows.append(row)

    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print("Transaction completed!")

def menu():
    while True:
        print("\n--- Bank Management System ---")
        print("1. Create Account")
        print("2. View Accounts")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            view_accounts()
        elif choice == "3":
            deposit()
        elif choice == "4":
            withdraw()
        elif choice == "5":
            break
        else:
            print("Invalid choice!")

menu()
