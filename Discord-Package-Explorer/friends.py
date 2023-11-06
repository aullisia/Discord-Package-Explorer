import os
import json
import requests
import csv
import pandas as pd

def count_lines_in_csv(file_path):
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
            return sum(1 for _ in csv_file)
    except FileNotFoundError:
        return 0  # Return 0 if the file doesn't exist

def find_channels_with_type(folder_path, target_channel_type=1, min_csv_lines=50, userid=None):
    userid = str(userid)
    #print("UID ", userid)
    channel_data = []  # List to store tuples (id, path)

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename == 'channel.json':
                channel_path = os.path.join(root, filename)
                csv_file_path = os.path.join(root, 'messages.csv')
                csv_lines = count_lines_in_csv(csv_file_path)

                if csv_lines >= min_csv_lines:
                    with open(channel_path, 'r') as channel_file:
                        channel_data_json = json.load(channel_file)
                        
                        # Add some debugging print statements
                        #print("Channel JSON Data:", channel_data_json)
                        #print("Current User ID:", userid)
                        
                        if (
                            'type' in channel_data_json and
                            channel_data_json['type'] == target_channel_type and
                            'id' in channel_data_json and
                            'recipients' in channel_data_json and
                            isinstance(channel_data_json['recipients'], list) and
                            len(channel_data_json['recipients']) >= 2 and
                            userid is not None and userid in channel_data_json['recipients']
                        ):
                            channel_id = channel_data_json['id']
                            channel_data.append((channel_id, channel_path, csv_file_path))

    return channel_data



def call_discord_lookup_api(found_channels, userid):
    #print(found_channels)

    friends_ids_and_paths = {}  # Create a dictionary to store recipient_id to file path mappings

    for channel_id, channel_json_path, messages_csv_path in found_channels:
        with open(channel_json_path, 'r', encoding='utf-8') as json_file:
            channel_data = json.load(json_file)
            recipients = channel_data.get('recipients', [])
            print(f"Recipients for channel {channel_id}: {recipients}")
            for recipient_id in recipients:
                if str(recipient_id) != str(userid):
                    friends_ids_and_paths[recipient_id] = messages_csv_path  # Map recipient_id to the messages.csv file path

    # print("Recipient IDs and their corresponding message file paths:")
    # for recipient_id, csv_path in friends_ids_and_paths.items():
    #     print(f"Recipient ID: {recipient_id}, Messages CSV Path: {csv_path}")




    base_url = "https://discordlookup.mesavirep.xyz/v1/user/"
    results = []

    for friend_id, messages_csv_path in friends_ids_and_paths.items():
        url = base_url + str(friend_id)
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            results.append((friend_id, messages_csv_path, data))

    return results


def start(folder_path, target_channel_type, min_csv_lines, current_user_id):
    found_channels = find_channels_with_type(folder_path, target_channel_type, min_csv_lines, current_user_id)
    userdata = call_discord_lookup_api(found_channels, current_user_id)
    return userdata

# data = start(r'C:\Users\alain\Desktop\package\messages', 1, 10000, 647480620426985473)
# print(data[1])