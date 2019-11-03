import os
import subprocess
import re

LIST_TOPIC = "kafka-topics.sh --zookeeper {zookeeper} --list"

def list_topics(zookeeper="127.0.0.1", kafka_path="/opt/kafka/bin"):

	list_topic_command = LIST_TOPIC.format(zookeeper=zookeeper)
	list_topic_command = os.path.join(kafka_path, list_topic_command)

	proc = subprocess.Popen(list_topic_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
	output, errors = proc.communicate()
	proc_exit_code = proc.returncode

	if proc_exit_code != 0:
		return False, errors, proc_exit_code

	output_list = output.split("\n")[0:-1]

	return output_list

def topic_filter(topic_list, regex=".*"):
	
	filtered_topics = []
	pattern = re.compile(regex)

	for topic in topic_list:
		if pattern.search(topic):
			filtered_topics.append(topic)

	return filtered_topics

if __name__ == "__main__":
	t = list_topics()
	print (t)

	print (topic_filter(t, regex="topic-[5-9]+"))
