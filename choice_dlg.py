import tkinter as tk


class ChoiceDlg:
    """A class to ask
     the user if they want to play again.
    
    Attributes: 
        choice: The choice made for game.
    """
    def __init__(self, msg: str) -> None:
        """Initialize the choice.
        
        Args:
            msg: A string that shows message.
        """
        self.choice = 'n'
        self.create(msg)


    def create(self, msg: str) -> None:
        """Initialize the choice.
        
        Args:
            msg: A string that shows message.
        """
        self.window = tk.Tk()
        self.window.resizable(False, False)
        self.window.title("Tic Tac Toe")

        tk.Label(self.window, text=msg).pack()

        button_area = tk.Frame(self.window, padx=10, pady=10)
        button_area.pack()

        yes_button = tk.Button(button_area, text='Yes', command=self.on_yes)
        yes_button.grid(row=0, column=0, sticky="w", padx=30)

        no_button = tk.Button(button_area, text='No', command=self.window.quit)
        no_button.grid(row=0, column=1, sticky="w", padx=30)

    def destroy(self) -> None:
        """Destroy the window when finishing."""
        self.window.destroy()

    def on_yes(self):
        """Quit when the user choice is yes. """
        self.choice = 'y'
        self.window.quit()


    def run(self) -> bool:
        """Run the program"""
        self.window.geometry('+%d+%d' % ((self.window.winfo_screenwidth()-300)/2, (self.window.winfo_screenheight()-400)/2))
        self.window.mainloop()
        return self.choice

