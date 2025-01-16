import os
import json
from collections import defaultdict
from datetime import datetime
import statistics
from collections import Counter

ME = "Bhavarth Vakharia"
# individual_dm_data
# overall_dm_data
# followers_following_list_count
# total_likes_comments

def sender_count(messages):
    sender_count = {}
    for message in messages:
        sender_count[message["sender_name"]] = sender_count.get(message["sender_name"], 0) + 1
    return sender_count

def get_chat_senders(messages):
    senders = set([message.get("sender_name") for message in messages])
    return senders

def filter_by_date(date, messages):
    filter_date = datetime.strptime(date, "%d-%m-%Y")
    start_of_day = int(filter_date.replace(hour=0, minute=0, second=0).timestamp() * 1000)
    end_of_day = int(filter_date.replace(hour=23, minute=59, second=59).timestamp() * 1000)
    filtered_messages = [
        message for message in messages if start_of_day<=message["timestamp_ms"]<=end_of_day
    ]
    return filtered_messages

def get_msg_count(messages, name="total"):
    sc = sender_count(messages)
    if name != "total":
        return sc[name]
    else:
        return sum(msg_count for msg_count in sc.values())
    
def count_reels_shared(messages):
    reels_shared = 0
    senders = {sender : 0 for sender in get_chat_senders(messages)}
    senders.pop("Meta AI")
    for message in messages:
        if "share" in message.keys():
            reels_shared += 1
            senders[message["sender_name"]] += 1
    
    return reels_shared, senders
    
def individual_dm_data(id):
    data = defaultdict(int)
    data["name"] = id
    inbox_path = "./your_instagram_activity/messages/inbox/"
    inbox = os.listdir(inbox_path)
    found = False
    user = ""
    for dm in inbox:
        if data["name"] in dm:
            found = True
            user = dm

    if found:
        file_path = inbox_path + user
        user_files = os.listdir(file_path)
        message_files = [file for file in user_files if file.startswith("message")]
        print(len(message_files))
        message_data = []
        for file in message_files:
            data = json.load(open(file_path + "/" + file, "r"))
            if "messages" in data:
                message_data.extend(data["messages"])

        timestamps = [message.get("timestamp_ms") for message in message_data]
        dates = [datetime.fromtimestamp(ts/1000).date().strftime("%d-%m-%Y") for ts in timestamps]
        most_active_date = statistics.mode(dates)
        date_counts = Counter(dates)
        count_reels_shared(message_data)
        print(get_chat_senders(message_data))
        data["senders"] = get_chat_senders(message_data)
        data["most_active_date"] = most_active_date
        data["total_msg_count"] = get_msg_count(message_data)
        data["sender_count"] = sender_count(message_data)
individual_dm_data("kiddie_dhreya")