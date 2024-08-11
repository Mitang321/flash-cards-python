import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import json
import os


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
        self.root = root
        self.root.title("Flashcard App")
        self.user = None

        self.frame = ttk.Frame(root)
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

    def login(self):
        username = simpledialog.askstring("Login", "Enter username:")
        if username:
            self.user = username
            self.add_button.config(state='normal')
            self.view_button.config(state='normal')
            self.quiz_button.config(state='normal')
            self.save_button.config(state='normal')
            self.load_button.config(state='normal')
            self.stats_button.config(state='normal')
            messagebox.showinfo("Info", f"Welcome, {username}!")

    def add_flashcard(self):
        question = simpledialog.askstring("Input", "Enter the question:")
        answer = simpledialog.askstring("Input", "Enter the answer:")
        category = simpledialog.askstring(
            "Input", "Enter the category (default 'General'):") or "General"
        if question and answer:
            self.flashcards.append(Flashcard(question, answer, category))
            messagebox.showinfo("Info", "Flashcard added!")

    def view_flashcards(self):
        if not self.flashcards:
            messagebox.showinfo("Info", "No flashcards available.")
        else:
            text = ""
            for i, card in enumerate(self.flashcards, 1):
                text += f"Flashcard {i}:\nQuestion: {card.question}\nAnswer: {card.answer}\nCategory: {card.category}\n\n"
            messagebox.showinfo("Flashcards", text)

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


if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
