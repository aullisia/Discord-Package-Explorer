import os
import io
import requests
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import json
from PIL import Image, ImageTk  # Import PIL and ImageTk


def display_csv_file(file_path, word_to_highlight, app):
    new_window = tk.Toplevel(app)
    new_window.title(f"CSV File Viewer: {file_path}")

    new_window.geometry("800x800")

    # Function to display an image from a URL
    def display_image(image_url, parent_frame):
        try:
            # Download the image using requests
            response = requests.get(image_url)
            response.raise_for_status()  # Check for HTTP errors

            # Convert the image content to bytes
            image_bytes = response.content

            # Open the image from the bytes using PIL
            image = Image.open(io.BytesIO(image_bytes))

            # Convert the image to a format suitable for tkinter
            image_tk = ImageTk.PhotoImage(image)

            # Create a label to display the image
            image_label = tk.Label(parent_frame, image=image_tk)
            image_label.image = image_tk
            image_label.pack()
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {e}")

    # Create a frame for the top navigation bar
    top_nav_bar = ttk.Frame(new_window)
    top_nav_bar.pack(side=tk.TOP, fill=tk.X)

    # Create buttons for CSV and User tabs
    csv_tab_button = ttk.Button(top_nav_bar, text="CSV File", command=lambda: switch_tab("csv"))
    user_tab_button = ttk.Button(top_nav_bar, text="User", command=lambda: switch_tab("user"))
    
    csv_tab_button.pack(side=tk.LEFT)
    user_tab_button.pack(side=tk.LEFT)

    # Create a frame for CSV content
    csv_content_frame = ttk.Frame(new_window)

    # Create a frame for User content
    user_content_frame = ttk.Frame(new_window)

    def switch_tab(tab):
        if tab == "csv":
            csv_content_frame.pack(fill="both", expand=True)
            user_content_frame.pack_forget()
        elif tab == "user":
            user_content_frame.pack(fill="both", expand=True)
            csv_content_frame.pack_forget()

    switch_tab("csv")

    # Configure the highlighting tag
    file_text = ScrolledText(csv_content_frame)
    file_text.pack(fill="both", expand=True)
    highlight_tag = "highlight"

    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            content = file.read()
            file_text.insert(tk.END, content)

            # Search and highlight the word in the content
            start = 1.0
            while True:
                start = file_text.search(word_to_highlight, start, tk.END)
                if not start:
                    break
                end = f"{start}+{len(word_to_highlight)}c"
                file_text.tag_add(highlight_tag, start, end)
                start = end
    except Exception as e:
        print(f"Error opening CSV file: {e}")




    # USER PAGE
    channel_file = os.path.join(os.path.dirname(file_path), "channel.json")
    with open(channel_file, 'r') as json_file:
        data = json.load(json_file)
    #print(data)

    if data['type'] == 1:
        recipients_list = data['recipients']
        id1 = recipients_list[0]
        id2 = recipients_list[1]

        base_url = "https://discordlookup.mesavirep.xyz/v1/user/"
        response1 = requests.get(base_url + id1)
        response2 = requests.get(base_url + id2)

        if response1.status_code == 200 and response2.status_code == 200:
            data1 = response1.json()
            data2 = response2.json()

            # Create a frame for the left user information
            left_user_frame = ttk.Frame(user_content_frame)
            left_user_frame.pack(side=tk.LEFT, padx=10)

            # Create a frame for the right user information
            right_user_frame = ttk.Frame(user_content_frame)
            right_user_frame.pack(side=tk.RIGHT, padx=10)

            # Display user information for User 1 (left side)
            user1_label1 = tk.Label(left_user_frame, text="User Information:")
            user1_label1.pack()
            
            user1_info_label2 = tk.Label(left_user_frame, text="tag: " + data1['tag'])
            user1_info_label2.pack()
            

            user1_info_label1 = tk.Label(left_user_frame, text="Name: " + data1['global_name'])
            user1_info_label1.pack()

            user1_info_label3 = tk.Label(left_user_frame, text="ID: " + data1['id'])
            user1_info_label3.pack()

            display_image(data1['avatar']['link'], left_user_frame,)



            
            # Display user information for User 2 (right side)
            user2_label1 = tk.Label(right_user_frame, text="User Information:")
            user2_label1.pack()
            
            user2_info_label2 = tk.Label(right_user_frame, text="tag: " + data2['tag'])
            user2_info_label2.pack()
            

            user2_info_label1 = tk.Label(right_user_frame, text="Name: " + data2['global_name'])
            user2_info_label1.pack()

            user2_info_label3 = tk.Label(right_user_frame, text="ID: " + data2['id'])
            user2_info_label3.pack()

            display_image(data2['avatar']['link'], right_user_frame,)
        else:
        # Display an error message
            err_label = tk.Label(user_content_frame, text="Failed to fetch data for one or both IDs.")
            err_label.pack()

    else:
        err_label = tk.Label(user_content_frame, text="Data could not be displayed.")
        err_label.pack()
