import tkinter as tk

class client_ui(tk.Frame):
    submit_done = False;
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.text = tk.Label(self, text = "Please Enter your Username")
        self.text.pack()
        self.entry = tk.Entry(self, bd = 5)
        self.entry.pack()
        self.submit = tk.Button(self, text="Submit", fg="black")
        self.submit.pack(side="bottom")




root = tk.Tk()
app = client_ui(master=root)
app.mainloop()
