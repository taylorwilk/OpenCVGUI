import matplotlib
from matplotlib import style
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, font

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
            filetypes=(("JPEG files", "*.jpeg"),("JPG files", "*.jpg"),("PNG files", "*.png"),
                        ("GIF files", "*.gif"),("ICON files", "*.ico"), ("All Files", "*.*")))
    img_path = filename
    # original_img is created to keep a referene to the unmodified image
    original_img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    # this is the image we will modify
    cv_img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    img_width = int(original_img.shape[1])
    img_height = int(original_img.shape[0])

    # make sure image will fit in our workspace label frame
    check_img_dimension(img_height, img_width)
    
# checks to make sure the image dimensions are within our labelFrame size
# if not then the image dimensions are changed
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
            # once an image is loaded activate buttons
            resize_button.config(state="normal")
            rotate_button.config(state="normal")
            blur_button.config(state="normal")
            color_button.config(state="normal")
            edge_detect_button.config(state="normal")
            interest_point_button.config(state="normal")
            revert_button.config(state="normal")
            save_button.config(state="normal")
             
        def blur_img():
            global cv_img
            global img
            
            cv_img = cv2.blur(cv_img, (5,5))
            
            img = ImageTk.PhotoImage(image = Image.fromarray(cv_img))
            img_label = tk.Label(workspace, image=img)
            img_label.place(x = 0, y = 0)

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

            resize = tk.Button(top, text="Resize", width=15, state="disabled", command=resize_img)
            resize.pack(side=tk.TOP, padx=10, pady=10)


        def open_rotate_window():
            global cv_img
            global img_height
            global img_width
            
            top = tk.Toplevel()
            frame = tk.Frame(top, width=290, height=200)
            frame.pack()
            top.title("Rotate Image")

            def rotate_right():
                global cv_img
                global img
                
                cv_img = cv2.rotate(cv_img, cv2.ROTATE_90_CLOCKWISE)
                
                img = ImageTk.PhotoImage(image = Image.fromarray(cv_img))
                img_label = tk.Label(workspace, image=img)
                img_label.place(x=0, y=0) 

            def flip_vertical():
                global cv_img
                global img
                
                cv_img = cv2.flip(cv_img, 0)
                
                img = ImageTk.PhotoImage(image = Image.fromarray(cv_img))
                img_label = tk.Label(workspace, image=img)
                img_label.place(x=0, y=0) 
            
            def flip_horizontal():
                global cv_img
                global img
                
                cv_img = cv2.flip(cv_img, 1)
                
                img = ImageTk.PhotoImage(image = Image.fromarray(cv_img))
                img_label = tk.Label(workspace, image=img)
                img_label.place(x=0, y=0) 

            def rotate_left():
                global cv_img
                global img
                
                cv_img = cv2.rotate(cv_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                
                img = ImageTk.PhotoImage(image = Image.fromarray(cv_img))
                img_label = tk.Label(workspace, image=img)
                img_label.place(x=0, y=0) 

            def back():
                top.destroy()
            
            rotate_label = ttk.Label(frame, text="Rotate 90 Degrees")
            rotate_label.place(x=90,y=18)

            rotate_l_button = ttk.Button(frame, text="Left", width=8, command=rotate_left)
            rotate_l_button.place(x=30,y=38)
            
            rotate_r_button = ttk.Button(frame, text="Right", width=8, command=rotate_right)
            rotate_r_button.place(x=150,y=38)

            flip_label = ttk.Label(frame, text="Flip")
            flip_label.place(x=132,y=80)

            flip_button = ttk.Button(frame, text="Vertical", width=8, command=flip_vertical)
            flip_button.place(x=30,y=100)  

            flip_button = ttk.Button(frame, text="Horizontal", width=8, command=flip_horizontal)
            flip_button.place(x=150,y=100)

            back_button = ttk.Button(frame, text="Back", width=4, command=back)
            back_button.place(x=106,y=155)
        
        def open_edge_detection():
            global cv_img
            global img

            top = tk.Toplevel()
            frame = tk.Frame(top, width=400, height=400)
            frame.pack()
            top.title("Rotate Image")

            options = [
                "Sobel Edge Detection"
                "Canny Edge Detection"
                "Laplacian Edge Detection"
            ]
            clicked = tk.StringVar()
            drop = tk.OptionMenu(top, clicked, options)
            drop.pack()

            but = ttk.Button(top, text="Show selection", command=show.pack())


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
                    filetypes=(("JPEG files", "*.jpeg"),("JPG files", "*.jpg"),("PNG files", "*.png"),
                                ("GIF files", "*.gif"), ("All Files", "*.*")))
            cv2.imwrite(filename, cv_img)
            messagebox.showinfo("Image Saved", "Image has been saved as " + os.path.basename(filename) + " successfully")

        pathName = tk.StringVar()
        
        main_background = tk.Frame(self)
        main_background.pack(expand=True, fill="both")

        label = tk.Label(main_background, text="OpenCV Image Editor", font = LARGE_FONT)  
        label.grid(row=0, column=0, columnspan=20, pady=10, padx=10, sticky="WE")

        getting_started= tk.LabelFrame(main_background, text="Getting Started", borderwidth=3, relief= tk.SUNKEN)
        getting_started.grid(row=1, column=0, columnspan=10, ipadx=30, padx=20, pady=20, sticky="NSEW")
        
        open_button = ttk.Button(getting_started, text="Open A New Image", width=15,
                            command=open_img)
        open_button.pack(anchor="center", pady=5)

        image_ops = tk.LabelFrame(main_background, text="Image Operations", borderwidth=3, relief= tk.SUNKEN)
        image_ops.grid(row=2, rowspan=39, column=0, columnspan=10, ipadx=30, ipady=200, padx=20, pady=20, stick="NSEW")

        resize_button = ttk.Button(image_ops, text="Resize Image", width=15, state="disabled",
                            command=open_resize_window)
        resize_button.pack()

        rotate_button = ttk.Button(image_ops, text="Rotate Image", width=15, state="disabled",
                            command=open_rotate_window)
        rotate_button.pack()
        
        blur_button = ttk.Button(image_ops, text="Blur Image", width=15, state="disabled",
                            command=blur_img)
        blur_button.pack()

        color_button = ttk.Button(image_ops, text="Change Image Color", width=15, state="disabled",)
        color_button.pack()

        edge_detect_button = ttk.Button(image_ops, text="Edge Detection", width=15, state="disabled",
                                command=open_edge_detection)
        edge_detect_button.pack()

        interest_point_button = ttk.Button(image_ops, text="Find Interest Points", width=15, state="disabled",)
        interest_point_button.pack()

        save_button = ttk.Button(image_ops, text="Save Image", width=15, state="disabled", 
                            command=save_img)
        save_button.pack(side=tk.BOTTOM)

        revert_button = ttk.Button(image_ops, text="Revert To Original", width=15, state="disabled", 
                            command=revert_img)
        revert_button.pack(side=tk.BOTTOM, pady=10)

        workspace = tk.LabelFrame(main_background, text="Workspace", borderwidth=3, relief= tk.SUNKEN)
        workspace.grid(row=1, rowspan=40, column=10, columnspan=10, ipadx=550, ipady=350, padx=20, pady=20, sticky="NSEW")
        workspace.grid_propagate(False)

class NewPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

app = OpenCVGUI()
app.main()