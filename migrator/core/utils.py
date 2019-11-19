import os
import json
from datetime import datetime

def create_topics_json(topic_list):

    """
        **Method for creating topics json file**

        Args:
            topic_list (string): list of topics

        Returns:
            dict: dict containing topics in the format required by kafka
    """

    topics_json = {}
    topics_json["version"] = 1
    topics_json["topics"] = []

    for topic in topic_list:
        topics_json["topics"].append({
            "topic": topic,
        })

    return topics_json

def write_to_file(json_type="topics", json_data=None):

    """
        **Method to write given contents to a file**

        Args:
            json_type (string): topics or plan, just to name the file appropriately

        Returns:
            string: Name of the file created
    """

    unix_time_stamp = datetime.now().strftime("%s")

    file_name = os.path.expanduser("~/.{json_type}.json").format(json_type=json_type)

    with open(file_name, "w") as openfile:
        openfile.write(json.dumps(json_data, indent=2))

    return file_name

def write_to_file_csv(csv_data):

    """
        **Method to write csv data to file**

        Args:
            string: csv data
        
        Returns:
            None: Returns nothing
    """

    unix_time_stamp = datetime.now().strftime("%s")

    file_name = os.path.expanduser("~/.plan.csv")

    with open(file_name, "w") as openfile:
        openfile.write(csv_data.decode())


def json_2_csv(json_data):
    
    """
        **Metthod for converting plan in json to csv format for table**

        Args:
            json_data (string): plan in json

        Returns:
            string: cvs data
    """
    partition_data = json_data.get("partitions")

    headers = ["Topic", "Partition", "Replicas", "Log Dirs"]

    rows = []
    rows.append(headers)

    for partition in partition_data:
        topic = partition.get("topic")
        partition_num = str(partition.get("partition"))
        replicas = ",".join([str(i) for i in partition.get("replicas")])
        log_dirs = ",".join([str(i) for i in partition.get("log_dirs")])

        rows.append([topic, partition_num, replicas, log_dirs])

    csv_data = ""

    for row in rows:
        csv_data += "        ".join(row) + "\n"

    return csv_data

def csv_2_json(csv_data):


    """
        **Metthod for converting plan in csv to json format for execution**

        Args:
            json_data (string): plan in csv

        Returns:
            string: json data
    """

    csv_list = csv_data.split("\n")
    csv_list = csv_list[1:len(csv_list)]

    json_data = {}

    json_data["version"] = 1
    json_data["partitions"] = []

    for csv_row in csv_list:
        csv_row_list = csv_row.split()
        csv_row_list = [i.strip() for i in csv_row_list]
        if len(csv_row_list) == 0:
            continue

        topic = csv_row_list[0]
        partition_num = int(csv_row_list[1])

        replicas = csv_row_list[2].split(",")
        replicas = [int(i.strip()) for i in replicas]

        log_dirs = csv_row_list[3].split(",")
        log_dirs = [i.strip() for i in log_dirs]

        partition = {
            "topic": topic,
            "partition": partition_num,
            "replicas": replicas,
            "log_dirs": log_dirs
        }

        json_data["partitions"].append(partition)

    return json_data

def remove_file(file_name):
    os.unlink(file_name)

def read_from_topics_file(topics_file):
    with open(topics_file) as f:
        topics = f.readlines()

    topic_list = []

    for topic in topics:
        topic = topic.strip()
        if topic == "" or len(topic) == 0:
            continue

        topic_list.append(topic)

    return topic_list

def clean_reassignment():
    plan_json = os.path.expanduser("~/.plan.json")
    plan_csv = os.path.expanduser("~/.plan.csv")

    if os.path.isfile(plan_csv):
        os.unlink(plan_csv)

    if os.path.isfile(plan_json):
        os.unlink(plan_json)

if __name__ == "__main__":
    #f = write_to_file("topics", create_topics_json(["topic-1", "topic-2"]))
    #print (f)

    with open("t.csv") as f:
        csv_data = f.read()

    out = csv_2_json(csv_data)

    print (json.dumps(out, indent=2))
