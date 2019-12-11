# Importing necessary packages
from tkinter import *
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import os, cv2, json, requests, urllib.request, tkinter as tk

# Defining CreateWidgets() function to create necessary tkinter widgets
def CreateWidgets():
    urlLabel = Label(root, text="INSTAGRAM URL : ", background = "deepskyblue4")
    urlLabel.grid(row=0, column=0, padx=5, pady=5)

    root.urlEntry = Entry(root, width=30, textvariable=instaURL)
    root.urlEntry.grid(row=0, column=1,columnspan=2, pady=5)

    dwldBTN = Button(root, text="DOWNLOAD", command=i_Downloader, highlightbackground = "green")
    dwldBTN.grid(row=0, column=3, padx=5, pady=5)

    root.resultsLabel = Label(root, text="RESULTS", background = "deepskyblue4")
    root.resultsLabel.grid(row=1, column=0, padx=5, pady=1)

    root.dwldLabel = Label(root, textvariable=dwldtxt, background = "deepskyblue4")
    root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    root.previewLabel = Label(root, text="PREVIEW", background = "deepskyblue4")
    root.previewLabel.grid(row=3, column=0, padx=5, pady=5)

# Defining i_Downloader() to download the INSTAGRAM POSTS
def i_Downloader():
    # Storing the path where to download the instagram posts in the download_path variable
    download_path = "YOUR DOWNLOAD PATH"
    # Sending request to the insta_url URL & storing the response in insta_Posts
    insta_Posts = requests.get(instaURL.get())
    # Specifying the desired format of the insta_Comments using html.parser
    # html.parser allows Python to read the components of the insta_Page
    soup = BeautifulSoup(insta_Posts.text, 'html.parser')
    # Finding <script> whose text matches with 'window._sharedData' using re.compile()
    script = soup.find('script', text=re.compile('window._sharedData'))
    # Splitting the text of <script>, 1 time at '=' and fetching the item at index 1
    # followed by removing the ';' from the string and storing the resulting string in page_json
    page_json = script.text.split(' = ', 1)[1].rstrip(';')
    # Parsing the above json page_json string using json_loads() and storing the resulting
    # dictionary in data variable which is a very long dictionary consisting of 19 items
    data = json.loads(page_json)
    # Storing the necessary part of the data dictionary in base_data
    base_data = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
    # Fetching the __typename of the POST from base_d dictionary and storing them in typename
    typename = base_data['__typename']


    # Checking if the typename is GraphImage meaning INSTAGRAM POST is a single image
    if typename == "GraphImage":
        # Fetching the Instagram Image URL from display_url of base_data dictionary
        display_url = base_data['display_url']
        # Fetching the taken_at_timestamp value from base_data dictionary and storing in filename
        file_name = base_data['taken_at_timestamp']
        # Concatenating download_path with filename and .jpg extension and storing in download_p
        download_p = download_path + str(file_name) + ".jpg"
        # Checking if the file already exists using the os.path.exists() method
        if not os.path.exists(download_p):
            # If not, then download the file using the urlretrieve() of the urlib.request module
            # which takes the url and download_path as the arguments
            urllib.request.urlretrieve(display_url, download_p)
            # Opening the download_p image using the open() method of the Image module
            image = Image.open(download_p)
            # Resizing the image using Image.resize()
            image = image.resize((90, 90), Image.ANTIALIAS)
            # Creating object of PhotoImage() class to display the frame
            image = ImageTk.PhotoImage(image)
            # Creating and configuring the label and displaying the image
            imageLabel = Label(root)
            imageLabel.grid(row=4, column=0, padx=1, pady=1)
            imageLabel.config(image=image)
            imageLabel.photo = image
            # Getting the text of the root.dwldLabel label and saving it in the prev_t
            prev_t = dwldtxt.get()
            # Concatenting thw prev_t with filename, message and saving in new_t
            new_t = prev_t + "\n" + str(file_name) + ".jpg DOWNLOADED"
            # Positioning the root.dwldLabel label
            root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
            # Displaying new_t in root.dwldLabel Label
            dwldtxt.set(new_t)
        else:
            # If the file is already present then displaying the appropriate message
            prev_t = dwldtxt.get()
            new_t = prev_t + "\n" + str(file_name) + ".jpg EXISTS"
            root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
            dwldtxt.set(new_t)

    # Checking if the typename is GraphVideo meaning INSTAGRAM POST is a video
    elif typename == "GraphVideo":
        # Fetching the Instagram Video URL from video_url of base_data dictionary
        video_url = base_data['video_url']
        # Fetching the taken_at_timestamp value from base_data dictionary and storing in filename
        file_name = base_data['taken_at_timestamp']
        # Concatenating download_path with filename and .mp4 extension and storing in download_p
        download_p = download_path + str(file_name) + ".mp4"
        # Checking if the file already exists using the os.path.exists() method
        if not os.path.exists(download_p):
            # If not present then download the file using the urlretrieve() of the urlib.request
            # module which takes the url and download_path as the arguments
            urllib.request.urlretrieve(video_url, download_p)
            # Instead of displaying video in GUI, a frame of the video will be displayed as an icon
            # Creating object of class VideoCapture with the video (download_p) as argument
            vid = cv2.VideoCapture(download_p)
            # Capturing frame by frame
            ret, frame = vid.read()
            # Setting the download path and a name for the frame and storing in video_icon
            video_icon = download_path + "/Video Icons/" + str(file_name) + ".jpg"
            # Saving the frame using the cv2.imwrite()
            cv2.imwrite(video_icon, frame)
            # Opening the video_icon, resizing it & creating PhotoImage() class object to display it
            icon = Image.open(video_icon)
            icon = icon.resize((90, 90), Image.ANTIALIAS)
            icon = ImageTk.PhotoImage(icon)
            # Creating and configuring the label and displaying the videoicon
            imageLabel = Label(root)
            imageLabel.grid(row=4, column=0, padx=1, pady=1)
            imageLabel.config(image=icon)
            imageLabel.photo = icon
            # Displaying the message
            prev_t = dwldtxt.get()
            new_t = prev_t + "\n" + str(file_name) + ".mp4 DOWNLOADED"
            root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
            dwldtxt.set(new_t)
        else:
            # If the file is already present then displaying the appropriate message
            prev_t = dwldtxt.get()
            new_t = prev_t + "\n" + str(file_name) + ".mp4 EXISTS"
            root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
            dwldtxt.set(new_t)
            root.dwldLabel.config(text=str(file_name) + ".mp4 HAS ALREADY BEEN DOWNLOADED")


    # Checking if typename is GraphSidecar meaning single POST consists of many images & videos
    elif typename == "GraphSidecar":
        # Fetching the value from shortcode of base_data dictionary
        shortcode = base_data['shortcode']
        # Sending request to INSTAGRAM URL with shortcode & converting the response to json and
        # storing the response in response
        response = requests.get(f"https://www.instagram.com/p/" + shortcode + "/?__a=1").json()
        # Declaring a variable named post_n and i and setting it to 1 and 0 respectively
        post_n = 1; i = 0
        # Interating through the edges present in the following location of response dictionary
        for edge in response['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']:
            # Fetching the taken_at_timestamp value from base_d dictionary and storing in filename
            file_name = response['graphql']['shortcode_media']['taken_at_timestamp']
            # Concatenating download_path with the filename & post_n value & storing in download_p
            download_p = download_path + str(file_name) + "-" + str(post_n)
            # Checking the value of is_video which will be either True or False
            is_video = edge['node']['is_video']

            # If is_video is False meaning single Instagram Post consists of only multiple Images
            if not is_video:
                # Fetching the Image URL from display_url of edge dictionary
                display_url = edge['node']['display_url']
                # Concatenating the download_p value with .jpg extension
                download_p += ".jpg"
                # Checking if the file already exists using the os.path.exists() method
                if not os.path.exists(download_p):
                    # If not present then download the file using the urlretrieve() of the
                    # urlib.request module which takes the url and download_path as the arguments
                    urllib.request.urlretrieve(display_url, download_p)
                    # Opening image, resizing it, & creating PhotoImage() class object to display it
                    image = Image.open(download_p)
                    image = image.resize((90, 90), Image.ANTIALIAS)
                    image = ImageTk.PhotoImage(image)
                    # Creating and configuring the label and displaying the image
                    imageLabel = Label(root)
                    imageLabel.grid(row=4, column=i, padx=1, pady=1)
                    imageLabel.config(image=image)
                    imageLabel.photo = image
                    # Displaying the message
                    prev_t = dwldtxt.get()
                    new_t = prev_t+"\n"+str(file_name) + "-" + str(post_n) + ".jpg DOWNLOADED"
                    root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
                    dwldtxt.set(new_t)
                    # Incrementing i by 1
                    i+=1
                else:
                    # If the file is already present then displaying the appropriate message
                    prev_t = dwldtxt.get()
                    new_t = prev_t+"\n"+str(file_name) + "-" + str(post_n) + ".jpg EXISTS"
                    root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
                    dwldtxt.set(new_t)

            # If is_video is True meaning Instagram Post consists of VIDEO along with the image
            else:
                # Fetching the Video URL from video_url of edge dictionary
                video_url = edge['node']['video_url']
                # Concatenating the download_p value with .mp4 extension
                download_p += ".mp4"
                # Checking if the file already exists using the os.path.exists() method
                if not os.path.exists(download_p):
                    # If not present then download the file using the urlretrieve() of urlib.request
                    # module which takes the url and download_path as the arguments
                    urllib.request.urlretrieve(video_url, download_p)
                    # Creating object of VideoCapture with video as argument and capturing frame by frame
                    vid = cv2.VideoCapture(download_p)
                    ret, frame = vid.read()
                    # Setting the download path & name for frame & saving the frame using the cv2.imwrite()
                    video_icon = download_path + "/Video Icons/" + str(file_name) + ".jpg"
                    cv2.imwrite(video_icon, frame)
                    # Opening the video_icon, resizing it, & creating PhotoImage() class object to display it
                    icon = Image.open(video_icon)
                    icon = icon.resize((90, 90), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(icon)
                    # Creating and configuring the label and displaying the image
                    imageLabel = Label(root)
                    imageLabel.grid(row=4, column=i, padx=1, pady=1)
                    imageLabel.config(image=img)
                    imageLabel.photo = img
                    # Displaying the message
                    prev_t = dwldtxt.get()
                    new_t = prev_t+"\n"+str(file_name) + "-" + str(post_n) + ".mp4 DOWNLOADED"
                    root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
                    dwldtxt.set(new_t)
                    # Incrementing i by 1
                    i+=1
                else:
                    # If the file is already present then displaying the appropriate message
                    prev_t = dwldtxt.get()
                    new_t = prev_t+"\n"+str(file_name) + "-" + str(post_n) + ".mp4 EXISTS"
                    root.dwldLabel.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
                    dwldtxt.set(new_t)
            # Incrementing the post_n value by 1
            post_n += 1

# Creating object of tk class
root = tk.Tk()

# Setting the title and background color disabling the resizing property
root.geometry("530x350")
root.title("i-DOWNLOADER")
root.config(background = "deepskyblue4")

# Creating tkinter variable
instaURL = StringVar()
dwldtxt = StringVar()

# Calling the CreateWidgets() function
CreateWidgets()

# Defining infinite loop to run application
root.mainloop()
