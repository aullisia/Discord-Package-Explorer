import os
import io
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, Canvas, Scrollbar
import configparser
import json
import requests
from PIL import Image, ImageTk  # Import PIL and ImageTk
import sv_ttk

import wordScan
import display_csv_file
import userStats
import friends

config_file = 'config.ini'


if not os.path.exists(config_file):
    # Create a new configuration object
    config = configparser.ConfigParser()

    # Add default data to the configuration
    config['Settings'] = {
        'filepath': 'No Filepath Configured',
        'excludedwords': '["yes", "UPWAKE", "", "i", "a", "an", "the", "in", "on", "at", "to", "of", "and", "for", "it", "is", "that", "with", "as", "by", "not", "was", "be", "am", "are", "were", "you", "he", "she", "we", "they", "or", "I", "im", "oh", "my", "ik", "me", "ur", "what", "like", "its", "dont", "but", "hi", "so", "do", "ok", "have", "will", "can", "would", "should", "could", "shall", "might", "must", "ought", "need", "now", "then", "there", "here", "where", "when", "how", "why", "who", "which", "whose", "whom", "between", "under", "over", "through", "before", "after", "while", "since", "until", "against", "about", "above", "below", "away", "along", "around", "without", "within", "upon", "behind", "beneath", "beside", "across", "besides", "among", "because", "although", "however", "nevertheless", "meanwhile", "furthermore", "therefore", "otherwise", "le", "la", "les", "un", "une", "de", "du", "des", "et", "ou", "en", "dans", "sur", "sous", "par", "pour", "avec", "mais", "ne", "pas", "est", "sont", "être", "avoir", "avant", "après", "pendant", "depuis", "entre", "chez", "tout", "rien", "plus", "moins", "trop", "très", "ici", "là", "quoi", "comment", "pourquoi", "qui", "quel", "quelle", "quels", "quelles", "cette", "ce", "ces", "ça", "aussi", "encore", "peut-être", "si", "donc", "alors", "voilà", "voici"]',
        'currentuserid': 'No userid Configured',
        'minmessages': '10000'
    }

    # Write the configuration to the file
    with open(config_file, 'w') as configfile:
        config.write(configfile)


    config.read(config_file)
else:
    # If the config file exists, read the configuration
    config = configparser.ConfigParser()
    config.read(config_file)


def setup_complete_check():
    config.read(config_file)
    #print("Setup status:", os.path.exists(config['Settings']['FilePath']))
    return os.path.exists(config['Settings']['FilePath'])

# Create the main application window
app = tk.Tk()
app.title("Discord package explorer")
app.geometry("1000x600")
app.resizable(False, False)
app.iconbitmap(default='./assets/icon.ico')


#Theme
sv_ttk.set_theme("dark")


def check_file_exists(file_path):
    return os.path.exists(file_path)

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
        placeholder_image_path = "./assets/Placeholder_Avatar.jpg"  # Replace with the path to your placeholder image file
        placeholder_image = Image.open(placeholder_image_path)
        placeholder_image_tk = ImageTk.PhotoImage(placeholder_image)

        # Create a label for the placeholder image
        placeholder_label = tk.Label(parent_frame, image=placeholder_image_tk)
        placeholder_label.image = placeholder_image_tk
        placeholder_label.pack()


#adding clicking to the csv files in the scroll thing
def open_csv_file(file_path):
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            # Add code to handle the CSV file content here
            print(f"Opened CSV file: {file_path}")
    except Exception as e:
        print(f"Error opening CSV file: {e}")


#function to update the file list
def update_file_list(file_list, word):
    file_list_text.config(state=tk.NORMAL)
    file_list_text.delete(1.0, tk.END)  # Clear the current content
    for index, file_info in enumerate(file_list):
        file_path, count = file_info
        tag = f"file_{index}"
        file_list_text.tag_configure(tag, foreground="blue", underline=True)
        file_list_text.insert(tk.END, f"CSV file found: {file_path}, Count: {count}\n", tag)
        file_list_text.tag_bind(tag, "<Button-1>", lambda e, path=file_path: display_csv_file.display_csv_file(path, word, app))
    file_list_text.config(state=tk.DISABLED)




#Saving file path
def save_data(file_path, UserId):
    config = configparser.ConfigParser()

    # Read the existing configuration
    config.read('config.ini')

    # Update the specific settings you want
    if 'Settings' not in config:
        config['Settings'] = {}

    config['Settings']['FilePath'] = file_path
    config['Settings']['currentUserId'] = UserId

    # Save the entire updated configuration
    with open('config.ini', 'w') as configfile:
        config.write(configfile)



#loading file path
def load_file_path():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    if 'Settings' in config and 'FilePath' in config['Settings']:
        return config['Settings']['FilePath']
    
    return None




# Function to handle button actions
def handle_button_action(action):
    # Get the text from the input field based on the action
    
    if action == "submit_word":
        if not setup_complete_check(): return
        word = input_field.get()
        word_count, file_list = wordScan.start(word, load_file_path())
        if word_count is not None:
            word_count_label.config(text=f"Word Count: {word_count}")
            update_file_list(file_list, word)

    elif action == "save_data":
        file_path = input_fields["save_path"].get()

        #check if filepath is real!!
        if not os.path.exists(file_path) and not os.path.exists(os.path.join(file_path, 'account', 'user.json')):
            print("File path does not exist")

            return
        

        json_file_path = os.path.join(file_path, 'account', 'user.json')
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            userid = data.get('id', None)
            if userid is not None:
                print(f"The 'id' value from 'user.json' is: {userid}")
            else:
                print("The 'id' key does not exist in the JSON file.")
                return


        
        #print(file_path, userid)
        save_data(file_path, userid)

        print(f"Saved path: {file_path}")
        filepath_label.config(text=f"Current Filepath: "+ load_file_path())
    
    elif action == "req_stats":
        if not setup_complete_check(): return
        path = load_file_path()
        account_folder = os.path.join(path, 'account')
        user_json_path = os.path.join(account_folder, 'user.json') 

        with open(user_json_path, 'r') as user_json_file:
            user_data = json.load(user_json_file)



        #make changes to page

        #make changes to text on page
        userid_label.config(text=f"User ID: {user_data['id']}")
        user_name_label.config(text=f"Name: {user_data['global_name']}")
        
        #do the statistic stuff:

        freq_words = userStats.topwords(load_file_path(), config['Settings']['excludedWords'], 10)
        print(freq_words)

        for i, word in enumerate(freq_words):
            word_label = ttk.Label(frequent_words_frame, text=word)
            word_label.grid(row=i, column=0, padx=5, pady=0)

    elif action == "req_friends":
        if not setup_complete_check(): return
        path = load_file_path()
        messages_folder = os.path.join(path, 'messages')

        friend_users = friends.start(messages_folder, 1, int(config["Settings"]["minMessages"]), config["Settings"]["currentUserId"])

        
        maxcount = len(friend_users)
        count = 0

        print("Rendering images: ", maxcount)

        for user in friend_users:
            if 'global_name' in user[2] and user[2]['global_name']:
                name = user[2]['global_name']
            else:
                name = "PlaceHolder"
            
            if 'avatar' in user[2] and 'link' in user[2]['avatar']:
                avatar_img_link = user[2]['avatar']['link']
            else:
                avatar_img_link = None

            message_link = user[1]
            #Create an image using the profile picture and a name to the right of it

            def create_avatar_frame(parent_frame, avatar_img_link, user_name, message_link):
                def on_avatar_click():
                    display_csv_file.display_csv_file(message_link, None , app)
                # Create a frame to contain the avatar and name
                avatar_frame = ttk.Frame(parent_frame)
                avatar_frame.pack(side="top", padx=10)

                # Create an image using the profile picture and a name to the right of it
                display_image(avatar_img_link, avatar_frame)

                # Create a label for the user's name
                name_label = ttk.Label(avatar_frame, text=user_name)
                name_label.pack()

                name_label.bind("<Button-1>", lambda e: on_avatar_click())

            create_avatar_frame(friends_avatars_container, avatar_img_link, name, message_link)

            count = count+1
            print(f"Progress: {count} / {maxcount}")





input_fields = {}


# Create a notebook to manage pages
notebook = ttk.Notebook(app)
notebook.pack(fill=tk.BOTH, expand=True)

pages = {}

for page_name in ["Home", "Word Scanner", "Stats", "Friends"]:
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=page_name)
    pages[page_name] = frame


























# Example content for Home page
home_label = ttk.Label(pages["Home"], text="Welcome to the Home Page")
home_label.pack(pady=20)

# Create a frame to contain the label and input field
save_frame = ttk.Frame(pages["Home"])
save_frame.pack(fill="both", expand=True)

# Center the frame horizontally
save_frame.grid_columnconfigure(0, weight=1)
save_frame.grid_columnconfigure(1, weight=1)

# Create a label for the input field
save_label = ttk.Label(save_frame, text="Enter file path:    ")
save_label.grid(row=0, column=0, sticky="e", pady=10)

# Create an input field for the path
input_field = ttk.Entry(save_frame)
input_field.grid(row=0, column=1, sticky="w", pady=10)
input_fields["save_path"] = input_field  # Correct key for the path field


file_path = load_file_path()
if file_path is not None:
    filepath_label = ttk.Label(pages["Home"], text=f"Current Filepath: {file_path}")
else:
    filepath_label = ttk.Label(pages["Home"], text="No Filepath Configured")
filepath_label.pack(pady=10)

# Create a Save button
submit_button = ttk.Button(pages["Home"], text="Save", command=lambda: handle_button_action("save_data"))
submit_button.pack()








# Example content for WORD SCANNER PAGE
page1_label = ttk.Label(pages["Word Scanner"], text="Welcome to the word scanner!")
page1_label.pack(pady=20)

input_field = ttk.Entry(pages["Word Scanner"])
input_field.pack(pady=10)
input_fields["submit_word"] = input_field

submit_button = ttk.Button(pages["Word Scanner"], text="Submit", command=lambda: handle_button_action("submit_word"))
submit_button.pack()

# Add a label to display the word count
word_count_label = ttk.Label(pages["Word Scanner"], text="")
word_count_label.pack(pady=10)

#add scrollable file thing
file_list_text = ScrolledText(pages["Word Scanner"], state=tk.DISABLED)
file_list_text.pack(fill="both", expand=True)









# Example content for STATS
stats_page_label = ttk.Label(pages["Stats"], text="You are on the stats page!")
stats_page_label.pack(pady=20)

submit_button = ttk.Button(pages["Stats"], text="Request stats", command=lambda: handle_button_action("req_stats"))
submit_button.pack()

userid_label = ttk.Label(pages["Stats"], text="")
userid_label.pack(pady=0)

user_name_label = ttk.Label(pages["Stats"], text="")
user_name_label.pack(pady=0)

frequent_words_frame = ttk.LabelFrame(pages["Stats"], text="Frequent Words")
frequent_words_frame.pack(side="left", pady=10, padx=10)






# Example content for FRIENDS PAGE
friend_page_label = ttk.Label(pages["Friends"], text="Friends page!")
friend_page_label.pack(pady=20)

friends_button = ttk.Button(pages["Friends"], text="Request data", command=lambda: handle_button_action("req_friends"))
friends_button.pack()

# Create a canvas to hold the avatars with vertical scrolling
friends_canvas = Canvas(pages["Friends"])
friends_canvas.pack(side="left", fill=tk.BOTH, expand=True)

# Create a frame to contain the avatars
friends_avatars_container = ttk.Frame(friends_canvas)
friends_canvas.create_window((0, 0), window=friends_avatars_container, anchor="nw")

# Add a vertical scrollbar for vertical scrolling
friends_vertical_scrollbar = Scrollbar(pages["Friends"], orient="vertical", command=friends_canvas.yview)
friends_canvas.configure(yscrollcommand=friends_vertical_scrollbar.set)
friends_vertical_scrollbar.pack(side="right", fill="y")

# Update the scroll region when the content changes
friends_avatars_container.bind("<Configure>", lambda event: friends_canvas.configure(scrollregion=friends_canvas.bbox("all")))


app.mainloop()


