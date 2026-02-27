import customtkinter as ctk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from forum_app import ForumApp

class ForumView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        self.master = master
        self.forum_app = ForumApp(master=self)
        self.forum_app.build_ui()
    
    def run(self):
        self.pack(expand=True, fill="both")
        self.forum_app.run()