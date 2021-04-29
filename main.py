import matplotlib
from matplotlib import style
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

import PIL
from PIL import ImageTk, Image

import os
import cv2

LARGE_FONT = ("Verdana", 24)
REGULAR_FONT = ("Verdana", 16)
original_img = ''
cv_img = ''
new_img = ''
img_path = ''
img_width = ''
img_height = ''
img = ''

# allow user to load an image and update global image variables
def browse_img():
    global original_img
    global cv_img
    global img_path
    global img_width
    global img_height
    filename = filedialog.askopenfilename(initialdir="Desktop", title="Select Image File", 
            filetypes=(("JPEG files", "*.jpeg"),("JPG files", "*.jpg"),("PNG files", "*.png"),("ICON files", "*.icon"), ("All Files", "*.*")))
    img_path = filename
    # original_img is created to keep a referene to the unmodified image
    original_img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    # this is the image we will modify
    cv_img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    img_width = int(original_img.shape[1])
    img_height = int(original_img.shape[0])

    # make sure image will fit in our workspace label frame
    check_img_dimension(img_height, img_width)
    

def check_img_dimension(height, width):
    global cv_img
    global img_width
    global img_height

    if (width > 1090):
        percent_decrease = 1090 / width
        img_height = img_height * percent_decrease
        img_width = 1090
        if (img_height > 700):
            percent_decrease = 700 / img_height
            img_width = img_width * percent_decrease
            img_height = 700
        cv_img = cv2.resize(cv_img, (int(img_width),int(img_height)), interpolation=cv2.INTER_AREA)

    elif (height > 700):
        percent_decrease = 700 / height
        img_width = img_width * percent_decrease
        img_height = 700
        if (img_width > 1090):
            percent_decrease = 1090 / img_width
            img_height = img_height * percent_decrease
            img_width = 1090
        cv_img = cv2.resize(cv_img, (int(img_width),int(img_height)), interpolation=cv2.INTER_AREA)

class OpenCVGUI(tk.Tk):

    # Basic view initialization
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "OpenCV Image Editor")

        # Setup container for all views
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to store mutliple frames
        self.frames = {}
        # For loop to initialize all pages and add to frames dictionary
        for Frame in (MainPage, NewPage):

            frame = Frame(container, self)

            self.frames[Frame] = frame

            frame.grid(row=0, column=0, sticky = "nsew")

        self.show_frame(MainPage)

    # Functions that the controller can use:
        
    # Bring whatever frame 'cont' is to the front of the window so it is visible
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def main(self):
        # Infinite loop to run tkinter until window is closed
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry("%dx%d" %(screen_width, screen_height))
        self.mainloop()


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def open_img():
            global cv_img
            global img
            browse_img()
            
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image = Image.fromarray(cv_img))
            img_label = tk.Label(workspace, image=img)
            img_label.place(x = 0, y = 0)
            
             
        def blur_img():
            global cv_img
            global img
            
            cv_img = cv2.blur(cv_img, (5,5))
            
            img = ImageTk.PhotoImage(image = Image.fromarray(cv_img))
            img_label = tk.Label(workspace, image=img)
            img_label.grid(row=0, column=0)

        # opens a new window for resizing image
        def open_resize_window():
            global img_width
            global img_height
            
            def recalculate():
                global img_width
                global img_height
                p = int(percent.get())
                img_width = img_width * p / 100
                img_height = img_height * p / 100
                resize.config(state="normal")
            
            def set_new_size():
                global img_width
                global img_height
                img_width = int(width.get())
                img_height = int(height.get())
                resize.config(state="normal")

            def resize_img():
                global cv_img
                global img

                cv_img = cv2.resize(cv_img, (int(img_width),int(img_height)), interpolation=cv2.INTER_AREA)
                
                img = ImageTk.PhotoImage(image = Image.fromarray(cv_img))
                img_label = tk.Label(workspace, image=img)
                img_label.place(x=0, y=0) 
                top.destroy()   

            top = tk.Toplevel()
            top.title("Resize Image")

            img_info = tk.Label(top, text="Image Dimensions\n Height: " + str(img_height) + "\nWidth: " + str(img_width))
            img_info.pack()

            pixel_safe = tk.LabelFrame(top, text="Pixel Safe", borderwidth=2, width = 100)
            pixel_safe.pack(fill="both", expand="yes", ipadx=30, ipady=20, padx=10, pady=5)

            label4 = tk.Label(pixel_safe, text="Percentage:")
            label4.pack(side=tk.LEFT, padx=10, pady=10)
            
            percent = tk.StringVar()
            ent = tk.Entry(pixel_safe, textvariable=percent)
            ent.pack(side=tk.LEFT, padx=10, pady=10)

            recalculate = ttk.Button(pixel_safe, text="Recalulate", width=15, command=recalculate)
            recalculate.pack(side=tk.LEFT, padx=10, pady=10)

            custom = tk.LabelFrame(top, text="Custom", borderwidth=2, width=100)
            custom.pack(fill="both", expand="yes", ipadx=30, padx=10, pady=5)

            new_h = tk.Label(custom, text="New Height:")
            new_h.grid(row=0, column=0, padx=10, pady=10)

            height = tk.StringVar()
            height_ent = tk.Entry(custom, textvariable=height)
            height_ent.grid(row=0, column=1, padx=10, pady=10)

            width = tk.StringVar()
            new_w = tk.Label(custom, text="New Width:")
            new_w.grid(row=1, column=0, padx=10, pady=10)

            width_ent = tk.Entry(custom, textvariable=width)
            width_ent.grid(row=1, column=1, padx=10, pady=10)

            set_size = ttk.Button(custom, text="Set New Dimensions", width=15, command=set_new_size)
            set_size.grid(row=1, column=2, padx=10, pady=10)

            resize = ttk.Button(top, text="Resize", width=15, state="disabled", command=resize_img)
            resize.pack(side=tk.TOP, padx=10, pady=10)
            resize.configure(disabledforeground="blue")

        def open_rotate_window():
            global cv_img
            global img_height
            global img_width

            top = tk.Toplevel()
            top.title("Rotate Image")

        def revert_img():
            global cv_img
            global img_height
            global img_width
            global img

            cv_img = original_img
            img_width = int(original_img.shape[1])
            img_height = int(original_img.shape[0])
            check_img_dimension(img_height, img_width)
            
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image = Image.fromarray(cv_img))
            img_label = tk.Label(workspace, image=img)
            img_label.place(x = 0, y = 0)
            
        def save_img():
            filename = filedialog.asksaveasfilename(initialdir="Desktop", title="Save Image", 
                    filetypes=(("JPEG files", "*.jpeg"),("JPG files", "*.jpg"),("PNG files", "*.png"),("ICON files", "*.icon"), ("All Files", "*.*")))
            cv2.imwrite(filename, cv_img)
            messagebox.showinfo("Image Saved", "Image has been saved as " + os.path.basename(filename) + " successfully")

        pathName = tk.StringVar()

        label = tk.Label(self, text="OpenCV Image Editor", font = LARGE_FONT)  
        label.grid(row=0, column=0, columnspan=20, pady=10, padx=10, sticky="WE")

        getting_started= tk.LabelFrame(self, text="Getting Started", borderwidth=3, relief= tk.SUNKEN)
        getting_started.grid(row=1, column=0, columnspan=10, ipadx=30, padx=20, pady=20, sticky="NSEW")
        
        open_button = ttk.Button(getting_started, text="Open A New Image", width=15,
                            command=open_img)
        open_button.pack(anchor="center", pady=5)

        image_ops = tk.LabelFrame(self, text="Image Operations", borderwidth=3, relief= tk.SUNKEN)
        image_ops.grid(row=2, rowspan=39, column=0, columnspan=10, ipadx=30, ipady=200, padx=20, pady=20, stick="NSEW")

        resize_button = ttk.Button(image_ops, text="Resize Image", width=15,
                            command=open_resize_window)
        resize_button.pack()

        rotate_button = ttk.Button(image_ops, text="Rotate Image", width=15)
        rotate_button.pack()

        blur_button = ttk.Button(image_ops, text="Blur Image", width=15,
                            command=blur_img)
        blur_button.pack()

        color_button = ttk.Button(image_ops, text="Change Image Color", width=15,)
        color_button.pack()

        edge_detect_button = ttk.Button(image_ops, text="Edge Detection", width=15,)
        edge_detect_button.pack()

        interest_point_button = ttk.Button(image_ops, text="Find Interest Points", width=15,)
        interest_point_button.pack()

        save_button = ttk.Button(image_ops, text="Save Image", width=15, 
                            command=save_img)
        save_button.pack(side=tk.BOTTOM)

        revert_button = ttk.Button(image_ops, text="Revert To Original", width=15, 
                            command=revert_img)
        revert_button.pack(side=tk.BOTTOM)

        workspace = tk.LabelFrame(self, text="Workspace", borderwidth=3, relief= tk.SUNKEN)
        workspace.grid(row=1, rowspan=40, column=10, columnspan=10, ipadx=550, ipady=350, padx=20, pady=20, sticky="NSEW")
        workspace.grid_propagate(False)

class NewPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

app = OpenCVGUI()
app.main()