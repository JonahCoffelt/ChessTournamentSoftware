import customtkinter as ctk

class loginWin():
    def __init__(self):
        
        root = ctk.CTk()
        root.geometry("500x350")

        def closeWindow():
            root.destroy()

        frame = ctk.CTkFrame(master=root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        label = ctk.CTkLabel(master=frame, text="Login System", font=("Arial", 24))
        label.pack(pady=12, padx=10)

        entry1 = ctk.CTkEntry(master=frame, placeholder_text="Username")
        entry1.pack(pady=12, padx=10)

        entry2 = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
        entry2.pack(pady=12, padx=10)

        button = ctk.CTkButton(master = frame, text="Login", command=closeWindow)
        button.pack(pady=12, padx=10)

        root.mainloop()