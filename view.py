import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib import style
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox
import os
import cv2


LARGE_FONT = ("Verdana", 24)
REGULAR_FONT = ("Verdana", 16)
img = ''
original_img = ''

class View(tk.Tk):

    # Basic view initialization
    def __init__(self, controller):
        
        super().__init__()

        self.controller = controller

        tk.Tk.wm_title(self, "OpenCV Image Editor")

        # Setup container for all views
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to store mutliple frames
        self.frames = {}
        # For loop to initialize all pages and add to frames dictionary
        for Frame in (StartPage, ResizePage):

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
        self.geometry("1100x700")
        self.mainloop()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Welcome To OpenCV Image Editor", font = LARGE_FONT)  
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Resize an image",
                            command=lambda: controller.show_frame(ResizePage))
        button1.pack()

class ResizePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)       

        t1 = tk.StringVar()
        width = tk.StringVar()
        height = tk.StringVar()
        percent = tk.StringVar()

        def browse_img():
            global img
            filename = filedialog.askopenfilename(initialdir="Desktop", title="Select Image File", 
                    filetypes=(("JPEG files", "*.jpeg"),("JPG files", "*.jpg"),("PNG files", "*.png"),("ICON files", "*.icon"), ("All Files", "*.*")))
            t1.set(filename)
            img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
            width.set(img.shape[1])
            height.set(img.shape[0])

        def preview_img():
            cv2.imshow("Source Image",img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        def recalculate():
            p = int(percent.get())
            new_width = int(int(width.get()) * p / 100)
            new_height = int(int(height.get()) * p / 100)
            width.set(new_width)
            height.set(new_height)

        def preview_resized_img():
            new_width = int(width.get())
            new_height = int(height.get())
            resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
            cv2.imshow("Preview Resized Image", resized_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        def save_resized_img():
            filename = filedialog.asksaveasfilename(initialdir="Desktop", title="Save Image", 
                    filetypes=(("JPEG files", "*.jpeg"),("JPG files", "*.jpg"),("PNG files", "*.png"),("ICON files", "*.icon"), ("All Files", "*.*")))
            new_width = int(width.get())
            new_height = int(height.get())
            resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
            cv2.imwrite(filename, resized_img)
            messagebox.showinfo("Image Saved", "Image has been saved as " + os.path.basename(filename) + " successfully")

        def open():
            global original_img
            filename = filedialog.askopenfilename(initialdir="Desktop", title="Select Image File", 
                    filetypes=(("JPEG files", "*.jpeg"),("JPG files", "*.jpg"),("PNG files", "*.png"),("ICON files", "*.icon"), ("All Files", "*.*")))
            original_img = ImageTk.PhotoImage(Image.open(filename))
            label2 = tk.Label(wrapper4, image=original_img)
            label2.pack()

        label = tk.Label(self, text="Resize Image", font = REGULAR_FONT)  
        label.pack() 

        back_button = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage))
        back_button.pack(padx=10, pady=10)

        wrapper = tk.LabelFrame(self, text="Source File")
        wrapper.pack(fill="both", expand="yes", padx=20, pady=20)

        wrapper2 = tk.LabelFrame(self, text="Image Details")
        wrapper2.pack(fill="both", expand="yes", padx=20, pady=20)

        wrapper3 = tk.LabelFrame(self, text="Pixel Safe")
        wrapper3.pack(fill="both", expand="yes", padx=20, pady=20)

        wrapper4 = tk.LabelFrame(self, text="Actions")
        wrapper4.pack(fill="both", expand="yes", padx=20, pady=20)
        
        label= tk.Label(wrapper, text="Source File")
        label.pack(side=tk.LEFT, padx=10, pady=10)

        ent1 = tk.Entry(wrapper, textvariable=t1)
        ent1.pack(side=tk.LEFT, padx=10, pady=10)

        button1 = ttk.Button(wrapper, text="Browse", command=browse_img)
        button1.pack(side=tk.LEFT, padx=10, pady=10)

        button2 = ttk.Button(wrapper, text="Preview", command=preview_img)
        button2.pack(side=tk.LEFT, padx=10, pady=10)

        label2 = tk.Label(wrapper2, text="Dimension")
        label2.pack(side=tk.LEFT, padx=10, pady=10)

        ent2 = tk.Entry(wrapper2, textvariable=width)
        ent2.pack(side=tk.LEFT, padx=10, pady=10)

        label3 = tk.Label(wrapper2, text="X")
        label3.pack(side=tk.LEFT, padx=5, pady=10)

        ent3 = tk.Entry(wrapper2, textvariable=height)
        ent3.pack(side=tk.LEFT, padx=10, pady=10)

        label4 = tk.Label(wrapper3, text="Percentage")
        label4.pack(side=tk.LEFT, padx=10, pady=10)

        ent4 = tk.Entry(wrapper3, textvariable=percent)
        ent4.pack(side=tk.LEFT, padx=10, pady=10)

        button3 = ttk.Button(wrapper3, text="Recalculate Dimension", command=recalculate)
        button3.pack(side=tk.LEFT, padx=10, pady=10)

        open_image_button = tk.Button(self, text="Open A New File", command=open)
        open_image_button.pack()
        
        preview_button = tk.Button(wrapper4, text="Preview", command=preview_resized_img)
        preview_button.pack(side=tk.LEFT, padx=10, pady=10)

        save_button = ttk.Button(wrapper4, text="Save", command=save_resized_img)
        save_button.pack(side=tk.LEFT, padx=10, pady=10)       
