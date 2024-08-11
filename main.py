import tkinter as tk
from tkinter import simpledialog, messagebox, ttk, filedialog
import json
import os
import hashlib


class Flashcard:
    def __init__(self, question, answer, category="General"):
        self.question = question
        self.answer = answer
        self.category = category

    def to_dict(self):
        return {
            'question': self.question,
            'answer': self.answer,
            'category': self.category
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['question'], data['answer'], data['category'])


class FlashcardApp:
    def __init__(self, root):
        self.flashcards = []
        self.categories = set()
        self.root = root
        self.root.title("Flashcard App")
        self.user = None

        # Layout improvements
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        self.login_frame = ttk.Frame(self.main_frame)
        self.login_frame.grid(row=0, column=0, columnspan=4, pady=10)

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=1, column=0, columnspan=4, pady=10)

        self.listbox_frame = ttk.Frame(self.main_frame)
        self.listbox_frame.grid(row=2, column=0, columnspan=4, pady=10)

        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.grid(row=3, column=0, columnspan=4, pady=10)

        self.login_button = ttk.Button(
            self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=0, column=0, padx=5, pady=5)

        self.register_button = ttk.Button(
            self.login_frame, text="Register", command=self.register)
        self.register_button.grid(row=0, column=1, padx=5, pady=5)

        self.logout_button = ttk.Button(
            self.login_frame, text="Logout", command=self.logout, state='disabled')
        self.logout_button.grid(row=0, column=2, padx=5, pady=5)

        self.add_button = ttk.Button(
            self.button_frame, text="Add Flashcard", command=self.add_flashcard, state='disabled')
        self.add_button.grid(row=1, column=0, padx=5, pady=5)

        self.view_button = ttk.Button(
            self.button_frame, text="View Flashcards", command=self.view_flashcards, state='disabled')
        self.view_button.grid(row=1, column=1, padx=5, pady=5)

        self.quiz_button = ttk.Button(
            self.button_frame, text="Quiz", command=self.quiz_user, state='disabled')
        self.quiz_button.grid(row=1, column=2, padx=5, pady=5)

        self.save_button = ttk.Button(
            self.button_frame, text="Save", command=self.save_flashcards, state='disabled')
        self.save_button.grid(row=2, column=0, padx=5, pady=5)

        self.load_button = ttk.Button(
            self.button_frame, text="Load", command=self.load_flashcards, state='disabled')
        self.load_button.grid(row=2, column=1, padx=5, pady=5)

        self.stats_button = ttk.Button(
            self.button_frame, text="Statistics", command=self.show_stats, state='disabled')
        self.stats_button.grid(row=2, column=2, padx=5, pady=5)

        self.filter_button = ttk.Button(
            self.button_frame, text="Filter by Category", command=self.filter_flashcards, state='disabled')
        self.filter_button.grid(row=3, column=1, padx=5, pady=5)

        self.edit_button = ttk.Button(
            self.button_frame, text="Edit Flashcard", command=self.edit_flashcard, state='disabled')
        self.edit_button.grid(row=4, column=0, padx=5, pady=5)

        self.delete_button = ttk.Button(
            self.button_frame, text="Delete Flashcard", command=self.delete_flashcard, state='disabled')
        self.delete_button.grid(row=4, column=1, padx=5, pady=5)

        self.import_button = ttk.Button(
            self.button_frame, text="Import Flashcards", command=self.import_flashcards, state='disabled')
        self.import_button.grid(row=5, column=0, padx=5, pady=5)

        self.export_button = ttk.Button(
            self.button_frame, text="Export Flashcards", command=self.export_flashcards, state='disabled')
        self.export_button.grid(row=5, column=1, padx=5, pady=5)

        self.search_label = ttk.Label(self.search_frame, text="Search:")
        self.search_label.grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = ttk.Entry(self.search_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_button = ttk.Button(
            self.search_frame, text="Search", command=self.search_flashcards, state='disabled')
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        self.flashcard_listbox = tk.Listbox(
            self.listbox_frame, width=50, height=10)
        self.flashcard_listbox.grid(row=0, column=0, padx=5, pady=5)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self):
        username = simpledialog.askstring("Register", "Enter username:")
        password = simpledialog.askstring(
            "Register", "Enter password:", show='*')
        if username and password:
            hashed_password = self.hash_password(password)
            users = self.load_users()
            if username in users:
                messagebox.showinfo("Error", "Username already exists!")
            else:
                users[username] = hashed_password
                self.save_users(users)
                messagebox.showinfo("Info", "Registration successful!")

    def login(self):
        username = simpledialog.askstring("Login", "Enter username:")
        password = simpledialog.askstring(
            "Login", "Enter password:", show='*')
        if username and password:
            hashed_password = self.hash_password(password)
            users = self.load_users()
            if username in users and users[username] == hashed_password:
                self.user = username
                self.add_button.config(state='normal')
                self.view_button.config(state='normal')
                self.quiz_button.config(state='normal')
                self.save_button.config(state='normal')
                self.load_button.config(state='normal')
                self.stats_button.config(state='normal')
                self.filter_button.config(state='normal')
                self.edit_button.config(state='normal')
                self.delete_button.config(state='normal')
                self.import_button.config(state='normal')
                self.export_button.config(state='normal')
                self.search_button.config(state='normal')
                self.logout_button.config(state='normal')
                messagebox.showinfo("Info", f"Welcome, {username}!")
            else:
                messagebox.showinfo("Error", "Invalid username or password!")

    def logout(self):
        self.user = None
        self.flashcards.clear()
        self.categories.clear()
        self.flashcard_listbox.delete(0, tk.END)
        self.add_button.config(state='disabled')
        self.view_button.config(state='disabled')
        self.quiz_button.config(state='disabled')
        self.save_button.config(state='disabled')
        self.load_button.config(state='disabled')
        self.stats_button.config(state='disabled')
        self.filter_button.config(state='disabled')
        self.edit_button.config(state='disabled')
        self.delete_button.config(state='disabled')
        self.import_button.config(state='disabled')
        self.export_button.config(state='disabled')
        self.search_button.config(state='disabled')
        self.logout_button.config(state='disabled')
        messagebox.showinfo("Info", "Logged out successfully!")

    def load_users(self):
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                return json.load(f)
        return {}

    def save_users(self, users):
        with open("users.json", "w") as f:
            json.dump(users, f)

    def add_flashcard(self):
        question = simpledialog.askstring("Input", "Enter the question:")
        answer = simpledialog.askstring("Input", "Enter the answer:")
        category = simpledialog.askstring(
            "Input", "Enter the category (default 'General'):") or "General"
        if question and answer:
            flashcard = Flashcard(question, answer, category)
            self.flashcards.append(flashcard)
            self.categories.add(category)
            self.flashcard_listbox.insert(
                tk.END, f"{question} - {category}")
            messagebox.showinfo("Info", "Flashcard added!")

    def view_flashcards(self):
        if not self.flashcards:
            messagebox.showinfo("Info", "No flashcards available.")
        else:
            self.flashcard_listbox.delete(0, tk.END)
            for flashcard in self.flashcards:
                self.flashcard_listbox.insert(
                    tk.END, f"{flashcard.question} - {flashcard.category}")

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
            "Edit", "Edit the category:", initialvalue=flashcard.category)

        if new_question and new_answer and new_category:
            self.flashcards[index] = Flashcard(
                new_question, new_answer, new_category)
            self.flashcard_listbox.delete(index)
            self.flashcard_listbox.insert(
                index, f"{new_question} - {new_category}")
            messagebox.showinfo("Info", "Flashcard updated!")

    def delete_flashcard(self):
        selected_index = self.flashcard_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Info", "No flashcard selected.")
            return

        index = selected_index[0]
        del self.flashcards[index]
        self.flashcard_listbox.delete(index)
        messagebox.showinfo("Info", "Flashcard deleted!")

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
            self.flashcard_listbox.delete(0, tk.END)
            for card in self.flashcards:
                self.flashcard_listbox.insert(
                    tk.END, f"{card.question} - {card.category}")
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

    def filter_flashcards(self):
        category = simpledialog.askstring(
            "Filter", "Enter category to filter:")
        if category:
            filtered_flashcards = [
                card for card in self.flashcards if card.category == category]
            if filtered_flashcards:
                self.flashcard_listbox.delete(0, tk.END)
                for card in filtered_flashcards:
                    self.flashcard_listbox.insert(
                        tk.END, f"{card.question} - {card.category}")
            else:
                messagebox.showinfo(
                    "Info", "No flashcards found for that category.")

    def import_flashcards(self):
        file_path = filedialog.askopenfilename(
            title="Select file", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                data = json.load(f)
                imported_flashcards = [
                    Flashcard.from_dict(item) for item in data]
                self.flashcards.extend(imported_flashcards)
                self.flashcard_listbox.delete(0, tk.END)
                for card in self.flashcards:
                    self.flashcard_listbox.insert(
                        tk.END, f"{card.question} - {card.category}")
                messagebox.showinfo(
                    "Info", "Flashcards imported successfully!")

    def export_flashcards(self):
        file_path = filedialog.asksaveasfilename(
            title="Save file", defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump([card.to_dict() for card in self.flashcards], f)
            messagebox.showinfo("Info", "Flashcards exported successfully!")

    def search_flashcards(self):
        query = self.search_entry.get().strip().lower()
        if query:
            matching_flashcards = [card for card in self.flashcards if query in card.question.lower(
            ) or query in card.category.lower()]
            if matching_flashcards:
                self.flashcard_listbox.delete(0, tk.END)
                for card in matching_flashcards:
                    self.flashcard_listbox.insert(
                        tk.END, f"{card.question} - {card.category}")
            else:
                messagebox.showinfo(
                    "Info", "No flashcards found matching the search query.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
