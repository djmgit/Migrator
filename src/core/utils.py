import os
import json
from datetime import datetime

def create_topics_json(topic_list):

    topics_json = {}
    topics_json["versio"] = 1
    topics_json["topics"] = []

    for topic in topic_list:
        topics_json["topics"].append({
            "topic": topic,
        })

    return topics_json

def write_to_file(json_type="topics", json_data=None):

    unix_time_stamp = datetime.now().strftime("%s")

    file_name = "{json_type}-{unix_time_stamp}.json".format(json_type=json_type, unix_time_stamp=unix_time_stamp)

    with open(file_name, "w") as openfile:
        openfile.write(json.dumps(json_data, indent=2))

    return file_name

def remove_file(file_name):
    os.unlink(file_name)

if __name__ == "__main__":
    f = write_to_file("topics", create_topics_json(["test-1", "test-2"]))
    print (f)
