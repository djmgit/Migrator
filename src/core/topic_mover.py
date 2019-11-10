import os
import json
import subprocess
from src.core.topic_extractor import list_topics, topic_filter
from src.core.utils import create_topics_json, write_to_file, remove_file

GENERATE_PLAN = "kafka-reassign-partitions.sh --zookeeper {zookeeper} --generate --topics-to-move-json-file {topics_json} --broker-list {broker_list}"
EXECUTE_PLAN = "kafka-reassign-partitions.sh --zookeeper {zookeeper} --execute --reassignment-json-file {plan_json}"

def generate_plan(**kwargs):

	zookeeper = kwargs.get("zookeeper")
	all_topics = kwargs.get("all_topics")
	topics = kwargs.get("topics")
	kafka_path = kwargs.get("kafka_path")
	topic_filter = kwargs.get("topic_filter")
	brokers = kwargs.get("brokers")

	if all_topics == True or topic_filter:
		error, topics = list_topics(zookeeper=zookeeper, kafka_path=kafka_path)

		if error:
			return error, None

	if topic_filter:
		topics = topic_filter(topics, regex=topic_filter)

	topics_json = create_topics_json(topics)
	topic_json_file = write_to_file(json_type="topics", json_data=topics_json)

	plan_generation_command = GENERATE_PLAN.format(zookeeper=zookeeper, topics_json=topic_json_file, broker_list=",".join(brokers))
	plan_generation_command = os.path.join(kafka_path, plan_generation_command)

	proc = subprocess.Popen(plan_generation_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
	output, error = proc.communicate()
	proc_exit_code = proc.returncode

	if proc_exit_code != 0:
		return error, None

	output_list = output.split("\n")
	plan_json = json.loads(output_list[4])

	remove_file(topic_json_file)

	return None, plan_json

def execute_plan(**kwargs):
	zookeeper = kwargs.get("zookeeper")
	plan_json = kwargs.get("plan_json")
	kafka_path = kwargs.get("kafka_path")

	plan_json_file = write_to_file(json_type="plan", json_data=plan_json)

	plan_execution_command = EXECUTE_PLAN.format(zookeeper=zookeeper, plan_json=plan_json_file)
	plan_execution_command = os.path.join(kafka_path, plan_execution_command)

	proc = subprocess.Popen(plan_execution_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
	output, error = proc.communicate()
	proc_exit_code = proc.returncode

	if proc_exit_code != 0:
		return error, None

	return None, plan_json_file
	

if __name__ == "__main__":
	plan_json = generate_plan(
		zookeeper="127.0.0.1",
		topics=["test-1"],
		kafka_path="/opt/kafka/bin",
		brokers=["1", "2", "3"]
	)[1]

	print (execute_plan(zookeeper="127.0.0.1", plan_json=plan_json, kafka_path="/opt/kafka/bin"))
	
