import datetime
import tkinter as tk
from tkinter import ttk


class FAQChatbotApp:

    def __init__(self, root):
        self.root = root
        self.root.title("CodeAlpha - FAQ Support Chatbot")
        self.root.geometry("450x600")
        self.root.configure(bg="#f1f5f9")

        # --- Pre-defined FAQ Knowledge Base ---
        self.faq_database = {
            "greetings": {
                "keywords": ["hello", "hi", "hey", "morning", "afternoon"],
                "answer": "Hello! Welcome to CodeAlpha Support. How can I help you today?"
            },
            "internship_duration": {
                "keywords": ["duration", "long", "month", "weeks", "period"],
                "answer": "The CodeAlpha internship program typically lasts for 4 weeks (1 month)."
            },
            "tasks_required": {
                "keywords": ["task", "tasks", "project", "projects", "many"],
                "answer": "You must complete any 2 or 3 out of the 4 assigned tasks from your domain."
            },
            "github_name": {
                "keywords": ["github", "repository", "repo", "name", "naming"],
                "answer": "Name your GitHub repository exactly: CodeAlpha_ProjectName."
            },
            "perks": {
                "keywords": ["perk", "perks", "certificate", "lor", "benefits"],
                "answer": "You receive an Offer Letter, QR-verified Certificate, and an LOR."
            },
            "linkedin_video": {
                "keywords": ["video", "linkedin", "post", "explain", "tag"],
                "answer": "Yes! You must post a video explanation of your project on LinkedIn."
            },
            "submission_form": {
                "keywords": ["form", "link", "where", "submit", "google"],
                "answer": "Submit your finalized project URLs using the CodeAlpha Submission Form."
            }
        }

        self.setup_ui()
        self.display_bot_message("Hello! I am AlphaBot. Ask me anything about your internship!")

    def setup_ui(self):
        header = tk.Frame(self.root, bg="#0f172a", height=60)
        header.pack(fill="x")
        header_title = tk.Label(header, text="🤖 CodeAlpha Support Bot", fg="white", bg="#0f172a", font=("Arial", 12, "bold"))
        header_title.pack(pady=15)

        self.chat_frame = tk.Frame(self.root, bg="#f1f5f9")
        self.chat_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.chat_canvas = tk.Canvas(self.chat_frame, bg="#ffffff", bd=1, relief="solid", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.chat_canvas.yview)

        self.scrollable_frame = tk.Frame(self.chat_canvas, bg="#ffffff")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        )

        self.chat_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.chat_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        input_frame = tk.Frame(self.root, bg="#f1f5f9")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.entry_box = tk.Entry(input_frame, font=("Arial", 11), bd=1, relief="solid")
        self.entry_box.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 5))
        self.entry_box.bind("<Return>", lambda event: self.handle_user_send())

        send_btn = tk.Button(input_frame, text="Send", bg="#2563eb", fg="white", font=("Arial", 10, "bold"),
                             activebackground="#1d4ed8", activeforeground="white", bd=0, padx=15, command=self.handle_user_send)
        send_btn.pack(side="right", ipady=6)

    def handle_user_send(self):
        user_text = self.entry_box.get().strip()
        if not user_text:
            return

        self.display_user_message(user_text)
        self.entry_box.delete(0, tk.END)

        bot_response = self.match_faq_intent(user_text)
        self.root.after(300, lambda: self.display_bot_message(bot_response))

    def match_faq_intent(self, text):
        clean_text = text.lower().replace("?", "").replace("!", "").replace(".", "").replace(",", "")
        user_words = clean_text.split()

        best_match = None
        max_score = 0

        for intent, data in self.faq_database.items():
            score = 0
            for keyword in data["keywords"]:
                if keyword in user_words or keyword in clean_text:
                    score += 1

            if score > max_score:
                max_score = score
                best_match = intent

        if max_score > 0 and best_match:
            return self.faq_database[best_match]["answer"]
        else:
            return "I couldn't find an answer. Ask about: perks, tasks, github, or forms!"

    def display_user_message(self, text):
        timestamp = datetime.datetime.now().strftime("%H:%M")
        msg_text = f"You ({timestamp}):\n{text}\n"
        lbl = tk.Label(self.scrollable_frame, text=msg_text, font=("Arial", 10), bg="#e2e8f0", fg="#0f172a",
                      justify="right", anchor="e", wraplength=350, padx=8, pady=5, bd=0)
        lbl.pack(fill="x", anchor="e", pady=4, padx=(50, 5))
        self.auto_scroll()

    def display_bot_message(self, text):
        timestamp = datetime.datetime.now().strftime("%H:%M")
        msg_text = f"AlphaBot ({timestamp}):\n{text}\n"
        lbl = tk.Label(self.scrollable_frame, text=msg_text, font=("Arial", 10), bg="#f8fafc", fg="#2563eb",
                      justify="left", anchor="w", wraplength=350, padx=8, pady=5, bd=0)
        lbl.pack(fill="x", anchor="w", pady=4, padx=(5, 50))
        self.auto_scroll()

    def auto_scroll(self):
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)


if __name__ == "__main__":
    root = tk.Tk()
    app = FAQChatbotApp(root)
    root.mainloop()
