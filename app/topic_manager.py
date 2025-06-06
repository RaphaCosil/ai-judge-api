import os

TOPICS_FOLDER = "data/topics"

def get_topic_file(topic_name):
    if topic_name == "pluto":
        return "data/pluto.txt"
    return f"{TOPICS_FOLDER}/{topic_name}.txt"

def load_topic_content(topic_name):
    file_path = get_topic_file(topic_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None

def get_topics_list():
    topics = ["pluto"]
    try:
        if os.path.exists(TOPICS_FOLDER):
            for file in os.listdir(TOPICS_FOLDER):
                if file.endswith(".txt"):
                    topics.append(file[:-4])
    except:
        pass
    return topics