import tkinter as tk
from tkinter import simpledialog, messagebox, ttk, filedialog, colorchooser
import json
import os
import csv
import sqlite3
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Flashcard:
    def __init__(self, question, answer, category="General", review_date="Not set"):
        self.question = question
        self.answer = answer
        self.category = category
        self.review_date = review_date

    def to_dict(self):
        return {
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'review_date': self.review_date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['question'], data['answer'], data['category'], data['review_date'])


class FlashcardApp:
    def __init__(self, root):
        self.flashcards = []
        self.root = root
        self.root.title("Flashcard App")
        self.user = None
        self.theme = {
            'bg_color': '#ffffff',
            'fg_color': '#000000',
            'card_color': '#f0f0f0',
            'button_color': '#cccccc'
        }

        self.initialize_ui()
        self.initialize_database()

    def initialize_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.login_button = ttk.Button(
            self.frame, text="Login", command=self.login)
        self.login_button.grid(row=0, column=0, padx=5, pady=5)

        self.add_button = ttk.Button(
            self.frame, text="Add Flashcard", command=self.add_flashcard, state='disabled')
        self.add_button.grid(row=1, column=0, padx=5, pady=5)

        self.view_button = ttk.Button(
            self.frame, text="View Flashcards", command=self.view_flashcards, state='disabled')
        self.view_button.grid(row=1, column=1, padx=5, pady=5)

        self.quiz_button = ttk.Button(
            self.frame, text="Quiz", command=self.quiz_user, state='disabled')
        self.quiz_button.grid(row=1, column=2, padx=5, pady=5)

        self.save_button = ttk.Button(
            self.frame, text="Save", command=self.save_flashcards, state='disabled')
        self.save_button.grid(row=2, column=0, padx=5, pady=5)

        self.load_button = ttk.Button(
            self.frame, text="Load", command=self.load_flashcards, state='disabled')
        self.load_button.grid(row=2, column=1, padx=5, pady=5)

        self.stats_button = ttk.Button(
            self.frame, text="Statistics", command=self.show_stats, state='disabled')
        self.stats_button.grid(row=2, column=2, padx=5, pady=5)

        self.filter_button = ttk.Button(
            self.frame, text="Filter", command=self.filter_flashcards, state='disabled')
        self.filter_button.grid(row=3, column=0, padx=5, pady=5)

        self.edit_button = ttk.Button(
            self.frame, text="Edit", command=self.edit_flashcard, state='disabled')
        self.edit_button.grid(row=3, column=1, padx=5, pady=5)

        self.delete_button = ttk.Button(
            self.frame, text="Delete", command=self.delete_flashcard, state='disabled')
        self.delete_button.grid(row=3, column=2, padx=5, pady=5)

        self.import_button = ttk.Button(
            self.frame, text="Import", command=self.import_flashcards, state='disabled')
        self.import_button.grid(row=4, column=0, padx=5, pady=5)

        self.export_button = ttk.Button(
            self.frame, text="Export", command=self.export_flashcards, state='disabled')
        self.export_button.grid(row=4, column=1, padx=5, pady=5)

        self.search_button = ttk.Button(
            self.frame, text="Search", command=self.search_flashcards, state='disabled')
        self.search_button.grid(row=4, column=2, padx=5, pady=5)

        self.theme_button = ttk.Button(
            self.frame, text="Customize Theme", command=self.customize_theme, state='disabled')
        self.theme_button.grid(row=4, column=3, padx=5, pady=5)

        self.progress_button = ttk.Button(
            self.frame, text="View Progress", command=self.view_progress, state='disabled')
        self.progress_button.grid(row=5, column=1, padx=5, pady=5)

        self.manage_profile_button = ttk.Button(
            self.frame, text="Manage Profile", command=self.manage_profile, state='disabled')
        self.manage_profile_button.grid(row=5, column=2, padx=5, pady=5)

        self.leaderboard_button = ttk.Button(
            self.frame, text="Leaderboard", command=self.show_leaderboard, state='disabled')
        self.leaderboard_button.grid(row=5, column=3, padx=5, pady=5)

        self.export_stats_button = ttk.Button(
            self.frame, text="Export Stats", command=self.export_stats_to_csv, state='disabled')
        self.export_stats_button.grid(row=6, column=0, padx=5, pady=5)

        self.flashcard_listbox = tk.Listbox(self.frame, width=60, height=15)
        self.flashcard_listbox.grid(
            row=7, column=0, columnspan=4, padx=5, pady=5)

    def initialize_database(self):
        self.conn = sqlite3.connect('flashcards.db')
        self.c = self.conn.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
                username TEXT PRIMARY KEY,
                score INTEGER
            )
        ''')
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                username TEXT,
                score INTEGER,
                date TEXT,
                FOREIGN KEY (username) REFERENCES leaderboard (username)
            )
        ''')
        self.conn.commit()

    def login(self):
        username = simpledialog.askstring("Login", "Enter username:")
        if username:
            self.user = username
            self.enable_buttons()
            messagebox.showinfo("Info", f"Welcome, {username}!")

    def enable_buttons(self):
        for button in [self.add_button, self.view_button, self.quiz_button, self.save_button,
                       self.load_button, self.stats_button, self.filter_button, self.edit_button,
                       self.delete_button, self.import_button, self.export_button, self.search_button,
                       self.theme_button, self.progress_button, self.manage_profile_button,
                       self.leaderboard_button, self.export_stats_button]:
            button.config(state='normal')

    def add_flashcard(self):
        question = simpledialog.askstring("Input", "Enter the question:")
        answer = simpledialog.askstring("Input", "Enter the answer:")
        category = simpledialog.askstring(
            "Input", "Enter the category (default 'General'):") or "General"
        if question and answer:
            flashcard = Flashcard(question, answer, category)
            self.flashcards.append(flashcard)
            self.flashcard_listbox.insert(
                tk.END, f"{flashcard.question} - {flashcard.category} (Review on: {flashcard.review_date})")
            messagebox.showinfo("Info", "Flashcard added!")

    def view_flashcards(self):
        if not self.flashcards:
            messagebox.showinfo("Info", "No flashcards available.")
        else:
            self.flashcard_listbox.delete(0, tk.END)
            for flashcard in self.flashcards:
                self.flashcard_listbox.insert(
                    tk.END, f"{flashcard.question} - {flashcard.category} (Review on: {flashcard.review_date})")

    def edit_flashcard(self):
        selected_index = self.flashcard_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Info", "No flashcard selected.")
            return

        index = selected_index[0]
        flashcard = self.flashcards[index]
        new_question = simpledialog.askstring(
            "Edit", "Edit the question:", initialvalue=flashcard.question)
        new_answer = simpledialog.askstring(
            "Edit", "Edit the answer:", initialvalue=flashcard.answer)
        new_category = simpledialog.askstring(
            "Edit", "Edit the category:", initialvalue=flashcard.category) or "General"

        if new_question and new_answer:
            flashcard.question = new_question
            flashcard.answer = new_answer
            flashcard.category = new_category
            self.flashcard_listbox.delete(index)
            self.flashcard_listbox.insert(
                index, f"{new_question} - {new_category} (Review on: {flashcard.review_date})")
            messagebox.showinfo("Info", "Flashcard updated!")

    def delete_flashcard(self):
        selected_index = self.flashcard_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Info", "No flashcard selected.")
            return

        index = selected_index[0]
        self.flashcards.pop(index)
        self.flashcard_listbox.delete(index)
        messagebox.showinfo("Info", "Flashcard deleted!")

    def search_flashcards(self):
        search_term = simpledialog.askstring("Search", "Enter search term:")
        if search_term:
            results = [flashcard for flashcard in self.flashcards if search_term.lower(
            ) in flashcard.question.lower()]
            if results:
                self.flashcard_listbox.delete(0, tk.END)
                for flashcard in results:
                    self.flashcard_listbox.insert(
                        tk.END, f"{flashcard.question} - {flashcard.category} (Review on: {flashcard.review_date})")
            else:
                messagebox.showinfo("Info", "No flashcards found.")

    def filter_flashcards(self):
        category = simpledialog.askstring(
            "Filter", "Enter category to filter by:")
        if category:
            results = [flashcard for flashcard in self.flashcards if flashcard.category.lower(
            ) == category.lower()]
            if results:
                self.flashcard_listbox.delete(0, tk.END)
                for flashcard in results:
                    self.flashcard_listbox.insert(
                        tk.END, f"{flashcard.question} - {flashcard.category} (Review on: {flashcard.review_date})")
            else:
                messagebox.showinfo(
                    "Info", "No flashcards found for this category.")

    def import_flashcards(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.flashcards = [Flashcard.from_dict(item) for item in data]
                self.view_flashcards()
                messagebox.showinfo("Info", "Flashcards imported!")

    def export_flashcards(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump([card.to_dict() for card in self.flashcards], f)
            messagebox.showinfo(
                "Info", f"Flashcards exported to '{file_path}'")

    def customize_theme(self):
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            self.theme['bg_color'] = color
            self.apply_theme()

    def apply_theme(self):
        self.frame.config(bg=self.theme['bg_color'])
        self.flashcard_listbox.config(bg=self.theme['card_color'])
        for button in [self.add_button, self.view_button, self.quiz_button, self.save_button,
                       self.load_button, self.stats_button, self.filter_button, self.edit_button,
                       self.delete_button, self.import_button, self.export_button, self.search_button,
                       self.theme_button, self.progress_button, self.manage_profile_button,
                       self.leaderboard_button, self.export_stats_button]:
            button.config(bg=self.theme['button_color'],
                          fg=self.theme['fg_color'])

    def quiz_user(self):
        if not self.flashcards:
            messagebox.showinfo("Info", "No flashcards available for quiz.")
            return

        import random
        random.shuffle(self.flashcards)
        score = 0
        total = len(self.flashcards)

        for card in self.flashcards:
            answer = simpledialog.askstring(
                "Quiz", f"Question: {card.question}")
            if answer and answer.strip().lower() == card.answer.strip().lower():
                messagebox.showinfo("Quiz", "Correct!")
                score += 1
            else:
                messagebox.showinfo(
                    "Quiz", f"Incorrect! The correct answer was: {card.answer}")

        messagebox.showinfo("Quiz Finished", f"Your score: {score}/{total}")

        self.save_stats(score, total)

    def save_flashcards(self):
        filename = f'{self.user}_flashcards.json'
        with open(filename, 'w') as f:
            json.dump([card.to_dict() for card in self.flashcards], f)
        messagebox.showinfo("Info", f"Flashcards saved to '{filename}'")

    def load_flashcards(self):
        filename = f'{self.user}_flashcards.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                self.flashcards = [Flashcard.from_dict(item) for item in data]
            messagebox.showinfo("Info", f"Flashcards loaded from '{filename}'")
        else:
            messagebox.showinfo(
                "Error", f"No saved flashcards found for user '{self.user}'.")

    def save_stats(self, score, total):
        stats_file = f'{self.user}_stats.json'
        stats = {'score': score, 'total': total}
        if os.path.exists(stats_file):
            with open(stats_file, 'r') as f:
                existing_stats = json.load(f)
            existing_stats.append(stats)
            with open(stats_file, 'w') as f:
                json.dump(existing_stats, f)
        else:
            with open(stats_file, 'w') as f:
                json.dump([stats], f)

    def show_stats(self):
        stats_file = f'{self.user}_stats.json'
        if os.path.exists(stats_file):
            with open(stats_file, 'r') as f:
                stats = json.load(f)
            total_score = sum(entry['score'] for entry in stats)
            total_quizzes = len(stats)
            average_score = total_score / total_quizzes if total_quizzes > 0 else 0
            messagebox.showinfo(
                "Statistics", f"Total Quizzes: {total_quizzes}\nAverage Score: {average_score:.2f}")
        else:
            messagebox.showinfo("Error", "No statistics found.")

    def view_progress(self):
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Progress")

        self.c.execute(
            'SELECT * FROM achievements WHERE username=?', (self.user,))
        rows = self.c.fetchall()

        progress_label = tk.Label(
            progress_window, text=f"Achievements:\n{', '.join(f'{row[1]} on {row[2]}' for row in rows)}")
        progress_label.pack(padx=10, pady=10)

    def manage_profile(self):
        profile_window = tk.Toplevel(self.root)
        profile_window.title("Manage Profile")

        new_score = simpledialog.askinteger(
            "Manage Profile", "Enter new score:")
        if new_score is not None:
            self.c.execute(
                'INSERT OR REPLACE INTO leaderboard (username, score) VALUES (?, ?)', (self.user, new_score))
            self.conn.commit()
            messagebox.showinfo("Info", "Profile updated!")

    def show_leaderboard(self):
        leaderboard_window = tk.Toplevel(self.root)
        leaderboard_window.title("Leaderboard")

        self.c.execute('SELECT * FROM leaderboard ORDER BY score DESC')
        rows = self.c.fetchall()

        leaderboard_text = "\n".join(f"{row[0]}: {row[1]}" for row in rows)
        leaderboard_label = tk.Label(
            leaderboard_window, text=f"Leaderboard:\n{leaderboard_text}")
        leaderboard_label.pack(padx=10, pady=10)

    def export_stats_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Username', 'Score', 'Date'])
                self.c.execute(
                    'SELECT * FROM achievements WHERE username=?', (self.user,))
                rows = self.c.fetchall()
                for row in rows:
                    writer.writerow([self.user, row[1], row[2]])
            messagebox.showinfo(
                "Info", f"Statistics exported to '{file_path}'")


if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
