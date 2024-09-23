import tkinter as tk
from tkinter import ttk, messagebox
from random import randint

clients = {
    "Joshua Ray": "2308070400",
    "Jason Mondo": "540192673",
    "Alicia kin": "157810241",
    "Max Armstrong": "782451231",
}

class Bank:
    def __init__(self, balance, account_number, name, overdraft_limit=100):
        self.balance = balance
        self.account_number = account_number
        self.name = name
        self.transactions = []
        self.overdraft_limit = overdraft_limit

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposited {amount} into your account")

    def withdraw(self, amount):
        if amount > self.balance:
            messagebox.showerror("Insufficient balance", "You don't have enough money in your account")
        else:
            self.balance -= amount
            self.transactions.append(f"Withdrew {amount} from your account")

    def get_balance(self):
        return self.balance

    def account_info(self):
        info = f"Account Number: {self.account_number}\nName: {self.name}\nBalance: {self.balance}\nTransactions:\n"
        for transaction in self.transactions:
            info += transaction + "\n"
        return info

    def transfer(self, amount, recipient):
        if amount > self.balance:
            messagebox.showerror("Insufficient balance", "You don't have enough money in your account")
        else:
            self.balance -= amount
            recipient.balance += amount
            self.transactions.append(f"Transferred {amount} to {recipient.name}")
            recipient.transactions.append(f"Received {amount} from {self.name}")

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Application")
        
        
        self.root.geometry("400x400")

        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", foreground="black", background="#D27D2D", font=("Arial", 10, "bold"),relief="flat")
        
        
       
        self.clients = {name: Bank(randint(0, 5000), acc_num, name) for name, acc_num in clients.items()}
        self.current_client = None

        self.login_screen()

    def login_screen(self):
        self.clear_screen()

        ttk.Label(self.root, text="Name:").pack(pady=5)
        self.name_entry = ttk.Entry(self.root)
        self.name_entry.pack(pady=5)

        ttk.Label(self.root, text="Account Number:").pack(pady=5)
        self.acc_num_entry = ttk.Entry(self.root)
        self.acc_num_entry.pack(pady=5)

        ttk.Button(self.root, text="Login", style="TButton", command=self.login).pack(pady=20)

    def login(self):
        name = self.name_entry.get()
        acc_num = self.acc_num_entry.get()

        if name in self.clients and self.clients[name].account_number == acc_num:
            self.current_client = self.clients[name]
            self.main_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid name or account number")

    def main_screen(self):
        self.clear_screen()

        ttk.Button(self.root, text="Deposit", style="TButton", command=self.deposit_screen).pack(pady=10)
        ttk.Button(self.root, text="Withdraw", style="TButton", command=self.withdraw_screen).pack(pady=10)
        ttk.Button(self.root, text="Transfer", style="TButton", command=self.transfer_screen).pack(pady=10)
        ttk.Button(self.root, text="Account Info", style="TButton", command=self.show_info).pack(pady=10)

        self.balance_label = ttk.Label(self.root, text=f"Total Balance: {self.current_client.get_balance()}")
        self.balance_label.pack(pady=20)

    def deposit_screen(self):
        self.clear_screen()

        ttk.Label(self.root, text="Deposit Amount:").pack(pady=5)
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.pack(pady=5)

        ttk.Button(self.root, text="Deposit", style="TButton", command=self.deposit).pack(pady=5)
        ttk.Button(self.root, text="Back", style="TButton", command=self.main_screen).pack(pady=5)

    def deposit(self):
        amount = float(self.amount_entry.get())
        self.current_client.deposit(amount)
        messagebox.showinfo("Success", "Deposit successful")
        self.update_balance()
        self.main_screen()

    def withdraw_screen(self):
        self.clear_screen()

        ttk.Label(self.root, text="Withdraw Amount:").pack(pady=5)
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.pack(pady=5)

        ttk.Button(self.root, text="Withdraw", style="TButton", command=self.withdraw).pack(pady=5)
        ttk.Button(self.root, text="Back", style="TButton", command=self.main_screen).pack(pady=5)

    def withdraw(self):
        amount = float(self.amount_entry.get())
        self.current_client.withdraw(amount)
        messagebox.showinfo("Success", "Withdrawal successful")
        self.update_balance()
        self.main_screen()

    def transfer_screen(self):
        self.clear_screen()

        ttk.Label(self.root, text="Transfer Amount:").pack(pady=5)
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.pack(pady=5)

        ttk.Label(self.root, text="Recipient Name:").pack(pady=5)
        self.recipient_entry = ttk.Entry(self.root)
        self.recipient_entry.pack(pady=5)

        ttk.Button(self.root, text="Transfer", style="TButton", command=self.transfer).pack(pady=5)
        ttk.Button(self.root, text="Back", style="TButton", command=self.main_screen).pack(pady=5)

    def transfer(self):
        amount = float(self.amount_entry.get())
        recipient_name = self.recipient_entry.get()

        if recipient_name in self.clients:
            recipient = self.clients[recipient_name]
            self.current_client.transfer(amount, recipient)
            messagebox.showinfo("Success", "Transfer successful")
            self.update_balance()
        else:
            messagebox.showerror("Error", "Recipient not found")
        self.main_screen()

    def show_info(self):
        info = self.current_client.account_info()
        messagebox.showinfo("Account Info", info)

    def update_balance(self):
        self.balance_label.config(text=f"Total Balance: {self.current_client.get_balance()}")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()

