import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import requests
import hashlib
import random
import html

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("quiztastic.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            score INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect("quiztastic.db")
    cur = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False
    conn.close()
    return True

def login_user(username, password):
    conn = sqlite3.connect("quiztastic.db")
    cur = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("SELECT password FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    if row and row[0] == hashed:
        return True
    return False

def get_score(username):
    conn = sqlite3.connect("quiztastic.db")
    cur = conn.cursor()
    cur.execute("SELECT score FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0

def update_score(username, score):
    conn = sqlite3.connect("quiztastic.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET score = score + ? WHERE username=?", (score, username))
    conn.commit()
    conn.close()

def get_leaderboard():
    conn = sqlite3.connect("quiztastic.db")
    cur = conn.cursor()
    cur.execute("SELECT username, score FROM users ORDER BY score DESC LIMIT 10")
    results = cur.fetchall()
    conn.close()
    return results

# --- API INTERACTION ---
def get_categories():
    url = "https://opentdb.com/api_category.php"
    try:
        r = requests.get(url)
        data = r.json()
        return data["trivia_categories"]
    except Exception:
        return []

def get_questions(amount, category, difficulty, qtype):
    url = f"https://opentdb.com/api.php?amount={amount}&category={category}&difficulty={difficulty}&type={qtype}"
    try:
        r = requests.get(url)
        data = r.json()
        if data["response_code"] == 0:
            return data["results"]
    except Exception:
        pass
    return []

# --- GUI ---
class QuiztasticApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiztastic")
        self.geometry("600x500")
        self.resizable(False, False)
        self.current_user = None
        self.frames = {}
        for F in (LoginFrame, RegisterFrame, HomeFrame, QuizFrame, LeaderboardFrame):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(LoginFrame)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class LoginFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Login", font=("Arial", 20)).pack(pady=20)
        tk.Label(self, text="Username").pack()
        self.user_entry = tk.Entry(self)
        self.user_entry.pack()
        tk.Label(self, text="Password").pack()
        self.pass_entry = tk.Entry(self, show="*")
        self.pass_entry.pack()
        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        tk.Button(self, text="Register", command=lambda: parent.show_frame(RegisterFrame)).pack()
    
    def login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get()
        if login_user(username, password):
            self.master.current_user = username
            messagebox.showinfo("Success", "Login successful!")
            self.master.show_frame(HomeFrame)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

class RegisterFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Register", font=("Arial", 20)).pack(pady=20)
        tk.Label(self, text="Username").pack()
        self.user_entry = tk.Entry(self)
        self.user_entry.pack()
        tk.Label(self, text="Password").pack()
        self.pass_entry = tk.Entry(self, show="*")
        self.pass_entry.pack()
        tk.Button(self, text="Register", command=self.register).pack(pady=10)
        tk.Button(self, text="Back to Login", command=lambda: parent.show_frame(LoginFrame)).pack()
    
    def register(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password.")
            return
        if register_user(username, password):
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            self.master.show_frame(LoginFrame)
        else:
            messagebox.showerror("Error", "Username already exists.")

class HomeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Welcome to Quiztastic", font=("Arial", 20)).pack(pady=20)
        tk.Button(self, text="Take Quiz", command=self.setup_quiz).pack(pady=10)
        tk.Button(self, text="Leaderboard", command=lambda: parent.show_frame(LeaderboardFrame)).pack(pady=10)
        tk.Button(self, text="Logout", command=self.logout).pack(pady=10)
        self.category_var = tk.StringVar()
        self.difficulty_var = tk.StringVar()
        self.type_var = tk.StringVar()
        self.amount_var = tk.IntVar(value=5)
        self.category_cb = None

    def setup_quiz(self):
        popup = tk.Toplevel(self)
        popup.title("Quiz Settings")
        popup.geometry("400x300")
        tk.Label(popup, text="Select Category").pack()
        categories = get_categories()
        cat_dict = {c["name"]: c["id"] for c in categories}
        self.category_cb = ttk.Combobox(popup, values=list(cat_dict.keys()), textvariable=self.category_var)
        self.category_cb.pack()
        tk.Label(popup, text="Select Difficulty").pack()
        self.difficulty_var.set("easy")
        ttk.Combobox(popup, values=["easy", "medium", "hard"], textvariable=self.difficulty_var).pack()
        tk.Label(popup, text="Select Type").pack()
        self.type_var.set("multiple")
        ttk.Combobox(popup, values=["multiple", "boolean"], textvariable=self.type_var).pack()
        tk.Label(popup, text="Number of Questions").pack()
        tk.Spinbox(popup, from_=1, to=20, textvariable=self.amount_var).pack()
        tk.Button(popup, text="Start Quiz", command=lambda: self.start_quiz(cat_dict, popup)).pack(pady=10)

    def start_quiz(self, cat_dict, popup):
        cat_name = self.category_var.get()
        cat_id = cat_dict.get(cat_name, 9)  # Default: General Knowledge
        difficulty = self.difficulty_var.get()
        qtype = self.type_var.get()
        amount = self.amount_var.get()
        questions = get_questions(amount, cat_id, difficulty, qtype)
        if not questions:
            messagebox.showerror("Error", "Failed to fetch questions. Try again later.")
            popup.destroy()
            return
        self.master.frames[QuizFrame].load_quiz(questions)
        popup.destroy()
        self.master.show_frame(QuizFrame)

    def logout(self):
        self.master.current_user = None
        self.master.show_frame(LoginFrame)

class QuizFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.q_data = []
        self.q_index = 0
        self.score = 0
        self.selected = tk.StringVar()
        self.widgets = []
        self.feedback_label = tk.Label(self, text="", font=("Arial", 12))
    
    def load_quiz(self, questions):
        self.q_data = questions
        self.q_index = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        for w in self.widgets:
            w.destroy()
        self.widgets = []
        self.feedback_label.config(text="")
        if self.q_index < len(self.q_data):
            q = self.q_data[self.q_index]
            tk.Label(self, text=f"Question {self.q_index+1} of {len(self.q_data)}", font=("Arial", 16)).pack(pady=10)
            qtext = html.unescape(q["question"])
            tk.Label(self, text=qtext, wraplength=500, font=("Arial", 14)).pack(pady=10)
            options = q["incorrect_answers"] + [q["correct_answer"]]
            options = [html.unescape(opt) for opt in options]
            random.shuffle(options)
            self.selected.set(None)
            for opt in options:
                rb = tk.Radiobutton(self, text=opt, value=opt, variable=self.selected, font=("Arial", 12))
                rb.pack(anchor="w", padx=40)
                self.widgets.append(rb)
            tk.Button(self, text="Submit", command=self.submit_answer).pack(pady=10)
            self.widgets.append(self.feedback_label)
            self.feedback_label.pack(pady=5)
        else:
            self.finish_quiz()

    def submit_answer(self):
        user_ans = self.selected.get()
        correct_ans = html.unescape(self.q_data[self.q_index]["correct_answer"])
        if user_ans == correct_ans:
            self.score += 1
            self.feedback_label.config(text="Correct!", fg="green")
        else:
            self.feedback_label.config(text=f"Wrong! Correct answer: {correct_ans}", fg="red")
        self.q_index += 1
        self.after(1000, self.show_question)

    def finish_quiz(self):
        username = self.master.current_user
        update_score(username, self.score)
        messagebox.showinfo("Quiz Finished", f"You scored {self.score}/{len(self.q_data)}")
        self.master.show_frame(HomeFrame)

class LeaderboardFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Leaderboard", font=("Arial", 20)).pack(pady=20)
        self.lb = tk.Listbox(self, width=50, height=10, font=("Arial", 12))
        self.lb.pack(pady=10)
        tk.Button(self, text="Back", command=lambda: parent.show_frame(HomeFrame)).pack(pady=10)
        self.bind("<Visibility>", lambda e: self.update_leaderboard())

    def update_leaderboard(self):
        self.lb.delete(0, tk.END)
        data = get_leaderboard()
        for idx, (user, score) in enumerate(data, 1):
            self.lb.insert(tk.END, f"{idx}. {user} - {score} points")

# --- MAIN ---
if __name__ == "__main__":
    init_db()
    app = QuiztasticApp()
    app.mainloop()