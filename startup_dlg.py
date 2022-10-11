import tkinter as tk
from tkinter import messagebox
from typing import Tuple

class StartupDlg:
    """A class which enables user to type in host information and user name.

    Attributes:
        host_name(str): The username of host.
        port(int): The number of port.
        user_name(str): The username of user.
        has_username(bool): The boolean variable that represents whether there is username.
        valid(bool): The boolean variable that represents whether it's valid.
    """
    def __init__(self, has_username: bool) -> None:
        """Initialize basic information of a dialog.
        
        Args:
            has_username: The boolean variable that represents whether there is username.
        """
        self.host_name = ''
        self.port = 0
        self.user_name = ''
        self.has_username = has_username
        self.valid = False
        self.create_widget()


    def create_widget(self) -> None:
        """Create the widget of the dialog."""
        self.window = tk.Tk()
        self.window.resizable(False, False)
        self.window.title("Tic Tac Toe")

        input_area = tk.Frame(self.window, padx=10, pady=10)
        input_area.pack()

        button_area = tk.Frame(self.window, padx=10, pady=10)
        button_area.pack()

        tk.Label(input_area, text="Host's name: ").grid(row=0, sticky="w")
        tk.Label(input_area, text="Host's port: ").grid(row=1, sticky="w")

        self.host_name_entry = tk.Entry(input_area)
        self.host_name_entry.grid(row=0, column=1, pady=5)

        self.port_entry = tk.Entry(input_area)
        self.port_entry.grid(row=1, column=1, pady=5)

        if self.has_username:
            tk.Label(input_area, text="User's name: ").grid(row=2, sticky="w")
            self.user_name_entry = tk.Entry(input_area)
            self.user_name_entry.grid(row=2, column=1, pady=5)

        connect_button = tk.Button(button_area, text='Start', command=self.on_ok)
        connect_button.grid(row=0, column=0, sticky="w", padx=30)

        exit_button = tk.Button(button_area, text='Quit', command=self.window.quit)
        exit_button.grid(row=0, column=1, sticky="w", padx=30)

        self.window.geometry('+%d+%d' % ((self.window.winfo_screenwidth()-300)/2, (self.window.winfo_screenheight()-400)/2))


    def destroy(self) -> None:
        """Destroy this and all descendants widgets."""
        self.window.destroy()


    def get_host_info(self) -> Tuple[str, int]:
        """Get host information.
        
        Returns:
            host_name: The username of host.
            port: The port of host.
        """
        return self.host_name, int(self.port)


    def get_user_name(self) -> str:
        """Get username.
        
        Returns:
            user_name: The name of user.
        """
        return self.user_name


    def on_ok(self) -> None:
        """Check user inputs and close the dialog."""
        self.host_name = self.host_name_entry.get()
        self.port = self.port_entry.get()

        if len(self.host_name) == 0:
            messagebox.showwarning("Error", "Please input host name of ip address.")
            return

        if not self.port.isnumeric():
            messagebox.showwarning("Error", "Please input an invalid port.")
            return

        if self.has_username:
            self.user_name = self.user_name_entry.get()
            if len(self.user_name) == 0:
                messagebox.showwarning("Error", "Please input user's name.")
                return

        self.valid = True
        self.window.quit()


    def run(self) -> bool:
        """Run the dialog program.
        
        Returns:
            True represents start, otherwise False.
        """
        self.valid = False
        self.window.mainloop()
        return self.valid

