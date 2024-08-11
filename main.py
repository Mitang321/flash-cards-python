import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, colorchooser
from tkinter import ttk
import json
import os
import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Flashcard:
    def __init__(self, question, answer, category="General"):
        self.question = question
        self.answer = answer
        self.category = category
        self.review_date = None

    def to_dict(self):
        return {
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'review_date': self.review_date
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls(data['question'], data['answer'], data['category'])
        instance.review_date = data.get('review_date')
        return instance

    def schedule_review(self, days):
        self.review_date = (
            datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')


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
            'button_color': '#007bff'
        }
        self.initialize_ui()

    def initialize_ui(self):
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

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

        self.search_entry = ttk.Entry(self.frame)
        self.search_entry.grid(row=4, column=2, padx=5,
                               pady=5, sticky=tk.W+tk.E)

        self.search_button = ttk.Button(
            self.frame, text="Search", command=self.search_flashcards, state='disabled')
        self.search_button.grid(row=4, column=3, padx=5, pady=5)

        self.theme_button = ttk.Button(
            self.frame, text="Customize Theme", command=self.customize_theme, state='disabled')
        self.theme_button.grid(row=5, column=0, padx=5, pady=5)

        self.progress_button = ttk.Button(
            self.frame, text="View Progress", command=self.view_progress, state='disabled')
        self.progress_button.grid(row=5, column=1, padx=5, pady=5)

        self.profile_button = ttk.Button(
            self.frame, text="Manage Profile", command=self.manage_profile, state='disabled')
        self.profile_button.grid(row=5, column=2, padx=5, pady=5)

        self.flashcard_listbox = tk.Listbox(self.frame, width=50, height=15)
        self.flashcard_listbox.grid(
            row=6, column=0, columnspan=4, padx=5, pady=5)

        self.apply_theme()

    def apply_theme(self):
        self.frame.config(bg=self.theme['bg_color'])
        style = ttk.Style()
        style.configure('TButton', background=self.theme['button_color'])
        for widget in self.frame.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.config(style='TButton')
            elif isinstance(widget, tk.Listbox):
                widget.config(
                    bg=self.theme['card_color'], fg=self.theme['fg_color'])
            elif isinstance(widget, tk.Entry):
                widget.config(
                    bg=self.theme['card_color'], fg=self.theme['fg_color'])
            elif isinstance(widget, tk.Label):
                widget.config(bg=self.theme['bg_color'],
                              fg=self.theme['fg_color'])

    def login(self):
        username = simpledialog.askstring("Login", "Enter username:")
        if username:
            self.user = username
            self.update_ui_for_user()
            messagebox.showinfo("Info", f"Welcome, {username}!")

    def update_ui_for_user(self):
        for widget in [self.add_button, self.view_button, self.quiz_button, self.save_button,
                       self.load_button, self.stats_button, self.filter_button, self.edit_button,
                       self.delete_button, self.import_button, self.export_button, self.search_button,
                       self.theme_button, self.progress_button, self.profile_button]:
            widget.config(state='normal')

    def logout(self):
        self.user = None
        self.flashcards = []
        self.flashcard_listbox.delete(0, tk.END)
        self.reset_ui_for_logout()
        messagebox.showinfo("Info", "Logged out successfully!")

    def reset_ui_for_logout(self):
        for widget in [self.add_button, self.view_button, self.quiz_button, self.save_button,
                       self.load_button, self.stats_button, self.filter_button, self.edit_button,
                       self.delete_button, self.import_button, self.export_button, self.search_button,
                       self.theme_button, self.progress_button, self.profile_button]:
            widget.config(state='disabled')

    def add_flashcard(self):
        question = simpledialog.askstring("Question", "Enter the question:")
        answer = simpledialog.askstring("Answer", "Enter the answer:")
        category = simpledialog.askstring(
            "Category", "Enter the category (optional):") or "General"
        if question and answer:
            flashcard = Flashcard(question, answer, category)
            self.flashcards.append(flashcard)
            self.flashcard_listbox.insert(
                tk.END, f"{question} - {category}")
            self.categories.add(category)

            schedule_days = simpledialog.askinteger(
                "Review", "Schedule review after how many days?", initialvalue=1)
            if schedule_days:
                flashcard.schedule_review(schedule_days)

    def view_flashcards(self):
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
        search_term = self.search_entry.get().lower()
        self.flashcard_listbox.delete(0, tk.END)
        for flashcard in self.flashcards:
            if (search_term in flashcard.question.lower() or
                search_term in flashcard.answer.lower() or
                    search_term in flashcard.category.lower()):
                self.flashcard_listbox.insert(
                    tk.END, f"{flashcard.question} - {flashcard.category} (Review on: {flashcard.review_date})")

    def filter_flashcards(self):
        categories = set(card.category for card in self.flashcards)
        selected_category = simpledialog.askstring(
            "Filter", f"Choose category ({', '.join(categories)}):")
        if selected_category in categories:
            self.flashcard_listbox.delete(0, tk.END)
            for flashcard in self.flashcards:
                if flashcard.category == selected_category:
                    self.flashcard_listbox.insert(
                        tk.END, f"{flashcard.question} - {flashcard.category} (Review on: {flashcard.review_date})")

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
            self.view_flashcards()
            messagebox.showinfo("Info", f"Flashcards loaded from '{filename}'")
        else:
            messagebox.showinfo("Error", "No saved flashcards found.")

    def import_flashcards(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv")])
        if not file_path:
            return

        _, ext = os.path.splitext(file_path)
        if ext == '.json':
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.flashcards.extend(
                    [Flashcard.from_dict(item) for item in data])
        elif ext == '.csv':
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.flashcards.append(
                        Flashcard(row['question'], row['answer'], row['category']))
        self.view_flashcards()
        messagebox.showinfo("Info", f"Flashcards imported from '{file_path}'")

    def export_flashcards(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv")])
        if not file_path:
            return

        _, ext = os.path.splitext(file_path)
        if ext == '.json':
            with open(file_path, 'w') as f:
                json.dump([card.to_dict() for card in self.flashcards], f)
        elif ext == '.csv':
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['question', 'answer', 'category'])
                for card in self.flashcards:
                    writer.writerow(
                        [card.question, card.answer, card.category])
        messagebox.showinfo("Info", f"Flashcards exported to '{file_path}'")

    def customize_theme(self):
        bg_color = colorchooser.askcolor(title="Choose Background Color")[1]
        fg_color = colorchooser.askcolor(title="Choose Text Color")[1]
        card_color = colorchooser.askcolor(title="Choose Card Color")[1]
        button_color = colorchooser.askcolor(title="Choose Button Color")[1]

        if bg_color:
            self.theme['bg_color'] = bg_color
        if fg_color:
            self.theme['fg_color'] = fg_color
        if card_color:
            self.theme['card_color'] = card_color
        if button_color:
            self.theme['button_color'] = button_color

        self.apply_theme()
        messagebox.showinfo("Theme", "Theme updated!")

    def view_progress(self):
        stats_file = f'{self.user}_stats.json'
        if os.path.exists(stats_file):
            with open(stats_file, 'r') as f:
                stats = json.load(f)
            dates = [datetime.strptime(entry['date'], '%Y-%m-%d')
                     for entry in stats]
            scores = [entry['score'] for entry in stats]

            fig, ax = plt.subplots()
            ax.plot(dates, scores, marker='o')
            ax.set_xlabel('Date')
            ax.set_ylabel('Score')
            ax.set_title('Quiz Score Progress')

            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        else:
            messagebox.showinfo("Error", "No progress data found.")

    def save_stats(self, score, total):
        stats_file = f'{self.user}_stats.json'
        stats = {'score': score, 'total': total,
                 'date': datetime.now().strftime('%Y-%m-%d')}
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

    def manage_profile(self):
        action = simpledialog.askstring(
            "Manage Profile", "Enter 'view' to view profile or 'edit' to edit profile:")
        if action.lower() == 'view':
            self.view_profile()
        elif action.lower() == 'edit':
            self.edit_profile()
        else:
            messagebox.showinfo("Error", "Invalid action.")

    def view_profile(self):
        profile_file = f'{self.user}_profile.json'
        if os.path.exists(profile_file):
            with open(profile_file, 'r') as f:
                profile = json.load(f)
            messagebox.showinfo("Profile", json.dumps(profile, indent=4))
        else:
            messagebox.showinfo("Error", "No profile found.")

    def edit_profile(self):
        profile_file = f'{self.user}_profile.json'
        name = simpledialog.askstring("Edit Profile", "Enter your name:")
        email = simpledialog.askstring("Edit Profile", "Enter your email:")
        if name and email:
            profile = {'name': name, 'email': email}
            with open(profile_file, 'w') as f:
                json.dump(profile, f)
            messagebox.showinfo("Profile", "Profile updated successfully!")
        else:
            messagebox.showinfo("Error", "Invalid profile data.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
