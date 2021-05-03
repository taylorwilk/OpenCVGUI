# OpenCV Image Editor

## **Team Members**

Taylor Wilk, Enoch Ikunda

## **Project Description/aims**

OpenCV Image Editor is a basic graphical user interface that allows users to load images from their local computer and perform various OpenCV library functions on them.

The overall goal of this project was to create a desktop-based software that is simple in design and easy to use.  Our software can be run on Microsoft Windows, Apple macOS, and Linux operating systems.  We wanted to create a space for non-programmers with different levels of expertise to be able to utilize many of the great features that OpenCV offers. "OpenCV is an open-source computer vision and machine learning software library", (OpenCV, 2021).  This library has over 2,500 optimized algorithms that can be utilized with C++, Python, Java, and MATLAB interfaces.  We chose a small handful of these algorithms to help people get their feet wet with understanding with what OpenCV can do.  It is our hope that after people play around with our software, they will be enticed into wanting to learn some of the code that goes into making these algorithms work.  This is an ongoing project that will have an increased number of functions added to it over time.  Please check back here often for updates on release dates for patches and future versions of this software.

## **Materials and Methods**

This project is written in Python and utilizes the Tkinter GUI package.  Tkinter is a Python binding to the Tk GUI toolkit. It is the standard Python interface to the Tk GUI toolkit, and is Python's de facto standard GUI. Tkinter is included with standard Linux, Microsoft Windows and Mac OS X installs of Python.

Other Python packages that are used to assist in image augmentation are NumPy, OS, PIL (Python Imaging Library), and OpenCV.

### **Methods:**

* Open A New Image
    *  Prompts the user to open an image file from their local machine.
    *  Supported image formate include JPEG, JPG, GIF, ICON, and PNG.
    *  If the image is bigger than the workspace display window then it is resized to fit within the window size.  The original dimensions of the image are stored.  This can be used later when saving an edited image if the user wants it to be resized back to its original dimensions.
    *  An orignal copy of the image will also be stored in case the user wants to revert back to the orignal image at any time.
    *  All other buttons will be disabeled until an image is opened.
* Resize Image
    * Opens a new window that displays the current image dimensions.
    * The image can be reszied by either entering a percentage or a specific new height and new width.
    *  If a percentage is provided then the image will be resized in a pixel safe manor where the ratio of the width and height of the image is unchanged.
    *  Otherwise the image will be resized to the specified new height and new width.
    * This method uses OpenCV's *resize* method.

        ```
        cv_img = cv2.resize(cv_img, (int(img_width),int(img_height)), interpolation=cv2.INTER_AREA)
        ```
* Rotate Image
    * Opens a new window with rotation options.
    * The image can be rotated 90 degrees to the left of right
    * The image can be flipped horizontally or veritcally
    * This method uses OpenCV's *rotate* and *flip* methods.

        ```
        cv_img = cv2.rotate(cv_img, cv2.ROTATE_90_CLOCKWISE)
        cv_img = cv2.flip(cv_img, 0)
        ```
* Blur Image
    * Blurs the image each time the user clicks this button.
    * Uses OpenCV's *blur* method with a defualt kernel size of 5x5

        ```
        cv_img = cv2.blur(cv_img, (5,5))
        ```
* Change Colorspace
    * Opens a new window with colorspace changing options.
    * Users can click a button to convert their image to a verity of different colorspaces.
    * Options include: GRAY, LAB, LUV, HSV, HLS, and YUV. 
    * Uses OpenCV's *cvtColor* method.
        ```
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2LUV)
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        ```
    * Users can also enter minimum and maximum values for image thresholding.
    * If the image is not in the *GRAY* colorspace then it will be converted to *GRAY* for preprocessing purposes.
    * All pixels with a value bellow the minimum threshold will be converted to 0 (black).
    * All pixels with a value above the minimum threshold will be converted to the maximum threshold.  This maximum threshold has a limit of 255.

        ```
        cv_img = cv2.threshold(cv_img, min, max, cv2.THRESH_BINARY)
        ```
* Edge Detection
    * Prompts the user to enter minimum and maximum values for thresholding with Canny Edge Detection.
    * These values are used for Hysteresis Thresholding.
    *  This is the stage of the algorithm in which all edges that were found are examined to see if they are edges we want to keep or not.
    *  Any edge with an intensity gradient that is more than the max value are kept as real edges.
    * Any edge below the minimum value is discarded.
    * Edges that lie in between these two thresholds are classified edges or non-edges based on if they are connected to "sure-edge" pixels.
    * The image is converted to *GRAY* and then has a bilateral filter applied to it as a preproccesing step before OpenCV's *Canny* function is called.

        ```
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        gray_filtered = cv2.bilateralFilter(gray, 3, 30, 30)
        cv_img = cv2.Canny(gray_filtered, min, max)
        ```

* Find Interest Points
    * Opens a new window where users can choose between using *BRISK* or *ORB* interest point detection.
    * *BRISK*: (Binary robust invariant scalable keypoints) Used as a keypoint detector and descriptor extractor.
        * Users can enter a threshold value that is used as a score value.  If a keypoint is found that has a score bellow this threshold then it is discarded, otherwise it is kept.
        * Uses OpenCV's *BRISK_create* method with a *patternScale* value of 1.2 and defualt values for the other parameters.

        ```
        gray_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        brisk = cv2.BRISK_create(thresh=int(threshold.get()), patternScale=1.2) 
        brisk_img = brisk.detect(gray_img,None)
        cv_img = cv2.drawKeypoints(cv_img, brisk_img, cv_img)
        ```
    * *ORB*: (oriented *BRIEF*) Used as a keypoint detector and descriptor extractor
        * User enter the maximum number of features they would like to keep.
        * This value is used as the *nfeatures* parameter.
        * Uses OpenCV's *ORB_create* method with a *WTA_K* value of 3 and default values for the other parameters.

        ```
        gray_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        orb = cv2.ORB_create(nfeatures=int(number_features.get()), WTA_K=3) 
        orb_img = orb.detect(gray_img,None)
        cv_img = cv2.drawKeypoints(cv_img, orb_img, cv_img)
        ```

* Connected Components
    * Opens a new window where the user is prompted if they want to invert black and white color fields when finding connected components
    * The image is first converted to *GRAY* and then black and white by using image thresholding.
    * If the user choses *YES* then the image pixel values are first inverted using a bitwise not method. 

        ```
        bw_img = cv2.bitwise_not(bw_img)
        ```
    * If the user chooses *NO* then the method proceeds along with no changes.
    * Connected components computes the connected components labeled image of boolean image and also produces a statitics output for each label.  This function consideres all black pixels to be the background.

        ```
        (num_labels, labels, stats, centroids) = cv2.connectedComponentsWithStats(bw_img)
        ```
    * After an array of labels is generated, a function to apply different hue's to each label is applied.

        ```
        label_hue = np.uint8(179*labels/np.max(labels))
        blank_ch = 255*np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
        labeled_img[label_hue==0] = 0
        cv_img = cv2.cvtColor(labeled_img, cv2.COLOR_BGR2RGB)
        ```

* Undo Last Operation
    * Changes the image back to its previous state.

* Revert To Original
    * Changes the image back to its original state.

* Save Image
    * Opens a window that allows the user to choose where to save the image locally.
    * Users can save images in a variety of formats including JPEG, JPG, GIF, and PNG.

* Quit
    * Closes the application

## **Experimental Validation and Results**

What follows is one example of the process of opening an image and performing a sequence of different methods on it.  This is just one example as there are a large number of different combinations of image operations that can be performed.

![Open A New Image](images/Screen Shot 2021-05-03 at 3.15.13 PM.png)







