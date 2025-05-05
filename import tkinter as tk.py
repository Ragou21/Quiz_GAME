import tkinter as tk
from tkinter import messagebox
import json
import random

# pour Charger les questions
with open("questions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu de Quiz")
        self.root.geometry("600x400")
        self.username = ""
        self.subject = ""
        self.level = ""
        self.score = 0
        self.current_question = 0
        self.questions = []
        
        self.create_start_screen()

    def create_start_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Bienvenue dans le jeu de Quiz !", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self.root, text="Entrez votre nom :").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()
        tk.Label(self.root, text="Choisissez une matière :").pack(pady=5)
        self.subject_var = tk.StringVar()
        for subject in data.keys():
            tk.Radiobutton(self.root, text=subject, variable=self.subject_var, value=subject).pack()
        tk.Label(self.root, text="Choisissez un niveau :").pack(pady=5)
        self.level_var = tk.StringVar()
        for level in ["facile", "moyen", "difficile"]:
            tk.Radiobutton(self.root, text=level.capitalize(), variable=self.level_var, value=level).pack()
        tk.Button(self.root, text="Commencer", command=self.start_quiz).pack(pady=10)

    def start_quiz(self):
        self.username = self.name_entry.get().strip()
        self.subject = self.subject_var.get()
        self.level = self.level_var.get()

        if not self.username or not self.subject or not self.level:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        self.questions = data[self.subject][self.level]
        random.shuffle(self.questions)
        self.score = 0
        self.current_question = 0
        self.show_question()

    def show_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            tk.Label(self.root, text=f"Question {self.current_question + 1}:", font=("Helvetica", 14)).pack(pady=10)
            tk.Label(self.root, text=q["question"], wraplength=500).pack(pady=5)
            self.answer_var = tk.StringVar()
            for option in q["options"]:
                tk.Radiobutton(self.root, text=option, variable=self.answer_var, value=option).pack(anchor="w", padx=100)
            tk.Button(self.root, text="Suivant", command=self.next_question).pack(pady=10)
        else:
            self.show_result()

    def next_question(self):
        if self.answer_var.get() == "":
            messagebox.showwarning("Attention", "Veuillez choisir une réponse.")
            return
        correct = self.questions[self.current_question]["answer"]
        if self.answer_var.get() == correct:
            self.score += 1
        self.current_question += 1
        self.show_question()

    def show_result(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text=f"Bravo {self.username} !", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self.root, text=f"Votre score : {self.score} / {len(self.questions)}", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(self.root, text="Rejouer", command=self.create_start_screen).pack(pady=5)
        tk.Button(self.root, text="Quitter", command=self.root.quit).pack()

#pour  Lancer le jeu
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizGame(root)
    root.mainloop()