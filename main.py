import tkinter as tk
from gui.main_menu import MainMenu

# Function to toggle fullscreen mode
def toggle_fullscreen(event=None):
    is_fullscreen = root.attributes("-fullscreen")
    root.attributes("-fullscreen", not is_fullscreen)  # Toggle fullscreen

# Function to exit fullscreen mode (bound to the Escape key)
def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)  # Exit fullscreen
<<<<<<< Tabnine <<<<<<<
def exit_fullscreen(event=None):#+
    """#+
    This function is used to exit fullscreen mode.#+
#+
    Parameters:#+
    event (tk.Event, optional): The event that triggered this function. Defaults to None.#+
        This parameter is not used in the function's logic but is kept for compatibility with#+
        the tkinter event binding system.#+
#+
    Returns:#+
    None#+
    """#+
    root.attributes("-fullscreen", False)  # Exit fullscreen#+
>>>>>>> Tabnine >>>>>>># {"conversationId":"218f86ef-685c-4b42-bdd0-df3af4e3c05e","source":"instruct"}

def main():
    global root

    root = tk.Tk()
    root.title("Pose Striker")
    root.geometry("800x600")

    # Start the app in fullscreen
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", exit_fullscreen)  # Bind Escape to exit fullscreen

    # Initialize Main Menu
    main_menu = MainMenu(root)
    main_menu.pack(fill=tk.BOTH, expand=True)

    # Bind F11 to toggle fullscreen
    root.bind("<F11>", toggle_fullscreen)

    root.mainloop()

if __name__ == "__main__":
    main()
