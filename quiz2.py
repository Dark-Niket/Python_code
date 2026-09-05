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
        self.geometry("800x600")
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)
        self.fullscreen = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        self.current_user = None
        self.frames = {}
        for F in (LoginFrame, RegisterFrame, HomeFrame, QuizFrame, LeaderboardFrame):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.show_frame(LoginFrame)

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)

    def end_fullscreen(self, event=None):
        self.fullscreen = False
        self.attributes("-fullscreen", False)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class LoginFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        container = tk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(container, text="Login", font=("Arial", 24, "bold")).pack(pady=20)
        tk.Label(container, text="Username", font=("Arial", 12)).pack()
        self.user_entry = tk.Entry(container, font=("Arial", 12))
        self.user_entry.pack(pady=5)
        tk.Label(container, text="Password", font=("Arial", 12)).pack()
        self.pass_entry = tk.Entry(container, show="*", font=("Arial", 12))
        self.pass_entry.pack(pady=5)
        tk.Button(container, text="Login", command=self.login, font=("Arial", 12), width=20).pack(pady=10)
        tk.Button(container, text="Register", command=lambda: parent.show_frame(RegisterFrame), font=("Arial", 12), width=20).pack()

    def login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        if login_user(username, password):
            self.master.current_user = username
            messagebox.showinfo("Success", "Login successful!")
            self.master.show_frame(HomeFrame)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

class RegisterFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        container = tk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(container, text="Register", font=("Arial", 24, "bold")).pack(pady=20)
        tk.Label(container, text="Username", font=("Arial", 12)).pack()
        self.user_entry = tk.Entry(container, font=("Arial", 12))
        self.user_entry.pack(pady=5)
        tk.Label(container, text="Password", font=("Arial", 12)).pack()
        self.pass_entry = tk.Entry(container, show="*", font=("Arial", 12))
        self.pass_entry.pack(pady=5)
        tk.Button(container, text="Register", command=self.register, font=("Arial", 12), width=20).pack(pady=10)
        tk.Button(container, text="Back to Login", command=lambda: parent.show_frame(LoginFrame), font=("Arial", 12), width=20).pack()

    def register(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
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
        container = tk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(container, text="Welcome to Quiztastic", font=("Arial", 24, "bold")).pack(pady=20)
        tk.Button(container, text="Take Quiz", command=self.setup_quiz, font=("Arial", 12), width=20).pack(pady=10)
        tk.Button(container, text="Leaderboard", command=lambda: parent.show_frame(LeaderboardFrame), font=("Arial", 12), width=20).pack(pady=10)
        tk.Button(container, text="Logout", command=self.logout, font=("Arial", 12), width=20).pack(pady=10)
        self.category_var = tk.StringVar()
        self.difficulty_var = tk.StringVar()
        self.type_var = tk.StringVar()
        self.amount_var = tk.IntVar(value=5)

    def setup_quiz(self):
        popup = tk.Toplevel(self)
        popup.title("Quiz Settings")
        popup.geometry("400x500")  # Increase height to ensure all widgets fit
        popup.transient(self)
        popup.grab_set()
        container = tk.Frame(popup, padx=20, pady=20)
        container.pack(expand=True, fill="both")
        tk.Label(container, text="Quiz Settings", font=("Arial", 20, "bold")).pack(pady=10)
        tk.Label(container, text="Select Category", font=("Arial", 12)).pack(pady=5)
        categories = get_categories()
        cat_dict = {c["name"]: c["id"] for c in categories}
        category_cb = ttk.Combobox(container, values=list(cat_dict.keys()), textvariable=self.category_var, font=("Arial", 12))
        category_cb.pack(pady=5)
        category_cb.current(0) if categories else None
        tk.Label(container, text="Select Difficulty", font=("Arial", 12)).pack(pady=5)
        self.difficulty_var.set("easy")
        ttk.Combobox(container, values=["easy", "medium", "hard"], textvariable=self.difficulty_var, font=("Arial", 12)).pack(pady=5)
        tk.Label(container, text="Select Type", font=("Arial", 12)).pack(pady=5)
        self.type_var.set("multiple")
        ttk.Combobox(container, values=["multiple", "boolean"], textvariable=self.type_var, font=("Arial", 12)).pack(pady=5)
        tk.Label(container, text="Number of Questions", font=("Arial", 12)).pack(pady=5)
        tk.Spinbox(container, from_=1, to=20, textvariable=self.amount_var, font=("Arial", 12)).pack(pady=5)
        tk.Button(container, text="Start Quiz", command=lambda: self.start_quiz(cat_dict, popup), font=("Arial", 12), width=20).pack(pady=20)

    def start_quiz(self, cat_dict, popup):
        cat_name = self.category_var.get()
        cat_id = cat_dict.get(cat_name, 9)
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
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.q_data = []
        self.q_index = 0
        self.score = 0
        self.selected = tk.StringVar()
        self.question_container = ttk.Frame(self.scrollable_frame)
        self.question_container.pack(expand=True, fill="both", padx=20, pady=20)

    def load_quiz(self, questions):
        self.q_data = questions
        self.q_index = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        for widget in self.question_container.winfo_children():
            widget.destroy()
        if self.q_index < len(self.q_data):
            q = self.q_data[self.q_index]
            tk.Label(self.question_container, text=f"Question {self.q_index+1} of {len(self.q_data)}", font=("Arial", 16, "bold")).pack(pady=10)
            qtext = html.unescape(q["question"])
            tk.Label(self.question_container, text=qtext, wraplength=600, font=("Arial", 14)).pack(pady=10)
            options = q["incorrect_answers"] + [q["correct_answer"]]
            options = [html.unescape(opt) for opt in options]
            random.shuffle(options)
            option_frame = ttk.Frame(self.question_container)
            option_frame.pack(pady=20, fill="x")
            self.selected.set(None)
            for opt in options:
                ttk.Radiobutton(option_frame, text=opt, value=opt, variable=self.selected).pack(anchor="w", padx=40, pady=5)
            ttk.Button(self.question_container, text="Submit", command=self.submit_answer).pack(pady=10)
            self.feedback_label = tk.Label(self.question_container, text="", font=("Arial", 12))
            self.feedback_label.pack(pady=5)
        else:
            self.finish_quiz()

    def submit_answer(self):
        if not self.selected.get():
            messagebox.showwarning("Warning", "Please select an answer!")
            return
        user_ans = self.selected.get()
        correct_ans = html.unescape(self.q_data[self.q_index]["correct_answer"])
        if user_ans == correct_ans:
            self.score += 1
            self.feedback_label.config(text="Correct!", fg="green")
        else:
            self.feedback_label.config(text=f"Wrong! Correct answer: {correct_ans}", fg="red")
        self.q_index += 1
        self.after(1500, self.show_question)

    def finish_quiz(self):
        username = self.master.current_user
        update_score(username, self.score)
        for widget in self.question_container.winfo_children():
            widget.destroy()
        tk.Label(self.question_container, text="Quiz Completed!", font=("Arial", 24, "bold")).pack(pady=20)
        tk.Label(self.question_container, text=f"Your Score: {self.score}/{len(self.q_data)}", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.question_container, text="Back to Home", command=lambda: self.master.show_frame(HomeFrame), font=("Arial", 12)).pack(pady=20)

class LeaderboardFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        container = tk.Frame(self)
        container.pack(expand=True, fill="both")
        tk.Label(container, text="Leaderboard", font=("Arial", 24, "bold")).pack(pady=20)
        columns = ("Rank", "Username", "Score")
        self.tree = ttk.Treeview(container, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)
        self.tree.pack(pady=20, fill="both", expand=True)
        tk.Button(container, text="Back to Home", command=lambda: parent.show_frame(HomeFrame), font=("Arial", 12)).pack(pady=10)
        self.bind("<Visibility>", lambda e: self.update_leaderboard())

    def update_leaderboard(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data = get_leaderboard()
        for idx, (user, score) in enumerate(data, 1):
            self.tree.insert("", "end", values=(idx, user, score))

# --- MAIN ---
if __name__ == "__main__":
    init_db()
    app = QuiztasticApp()
    app.mainloop()