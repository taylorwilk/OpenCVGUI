import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)

class View(tk.Tk):

    # Basic view initialization
    def __init__(self, controller):
        
        super().__init__()

        self.controller = controller

        # Setup container for all views
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to store mutliple frames
        self.frames = {}
        # For loop to initialize all pages and add to frames dictionary
        for Frame in (StartPage, PageOne, PageTwo):

            frame = Frame(container, self)

            self.frames[Frame] = frame

            frame.grid(row=0, column=0, sticky = "nsew")

        self.show_frame(StartPage)

        
    # Bring whatever frame 'cont' is to the front of the window so it is visible
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def main(self):
        # Infinite loop to run tkinter until window is closed
        self.mainloop()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Start Page", font = LARGE_FONT)  
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button1.pack()

        button2 = tk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)       

        label = tk.Label(self, text="Page One", font = LARGE_FONT)  
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)       

        label = tk.Label(self, text="Page Two", font = LARGE_FONT)  
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page one",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()
  