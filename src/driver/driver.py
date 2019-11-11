from src.core.topic_mover import generate_plan, execute_plan
from src.core.utils import json_2_csv, csv_2_json, write_to_file_csv
import optparse
import editor
import sys
import os

def drive():

	options = setup_optparse()

	if options.edit:
		edit_plan()
		exit(0)

	if options.kafkapath:
		kafka_path = options.kafkapath
	else:
		kafka_path = input("kafka path : ")

	is_all = options.all

	if options.topics:
		topics = [t.strip() for t in options.topics.split(",")]
	else:
		topics = None

	if options.filter:
		topic_filter = options.filter
	else:
		topic_filter = None

	if options.zookeeper:
		zookeeper = options.zookeeper
	else:
		zookeeper = input("Zookeeper : ")

	if options.brokers:
		brokers = options.brokers
	else:
		brokers = input("Brokers (separated by comma) : ")

	brokers = [b.strip() for b in brokers.split(",")]

	if options.topics == None and options.all == False:
		topics = input("Topics to move (separated by comma) : ")
		topics = [t.strip() for t in topics.split(",")]

	error, plan_json = generate_plan(
										zookeeper=zookeeper,
										all_topics=is_all,
										topics=topics,
										kafka_path=kafka_path,
										topic_filter=topic_filter,
										brokers=brokers
									)

	plan_csv = json_2_csv(plan_json)

	plan_csv = editor.edit(contents=plan_csv)

	write_to_file_csv(plan_csv)

def edit_plan():
	if not os.path.isfile(".plan.csv"):
		print ("No ressasignment in progress!")
		exit(0)

	with open(".plan.csv") as openfile:
		csv_plan = openfile.read()

	plan_csv = editor.edit(contents=csv_plan)

	write_to_file_csv(plan_csv)

def setup_optparse():
	parser = optparse.OptionParser()
	parser.add_option('-p', '--kafkapath', dest='kafkapath', default="/opt/kafka/bin", help="Provide path to kafka binaries")
	parser.add_option('-a', '--all', dest="all", action="store_true", default=False, help="Select all the topics for moving")
	parser.add_option('-f', '--filter', dest="filter", help="Regex to filter topic names")
	parser.add_option('-t', '--topics', dest='topics', help="Comma separated topics")
	parser.add_option('-z', '--zookeeper', dest='zookeeper', help="Provide zookeeper host/ip. If port used is different from 2181, then provide host:port")
	parser.add_option('-b', '--brokers', dest="brokers", help="Provide broker ids separated by comma")
	parser.add_option('-e', '--edit', dest="edit", action="store_true", default=False, help="Edit current plan" )

	options, args = parser.parse_args()

	return options

if __name__ == "__main__":
	drive()
