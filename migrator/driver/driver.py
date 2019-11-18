from migrator.core.topic_mover import generate_plan, execute_plan, verify_plan
from migrator.core.utils import json_2_csv, csv_2_json, write_to_file_csv, read_from_topics_file, clean_reassignment
import optparse
import editor
import sys
import os
import json
from tabulate import tabulate

def drive():

	options = setup_optparse()

	if options.edit:
		edit_plan()
		exit(0)

	if options.list_partitions:
		show_plan(frmt="csv")
		exit(0)

	if options.list_partitions_json:
		show_plan(frmt="json")
		exit(0)

	if options.clean:
		clean_reassignment()
		print ("Existing reassignment data cleaned")
		exit(0)

	if options.deploy:
		deploy(options)
		exit(0)

	if options.verify:
		verify(options)
		exit(0)

	if options.kafkapath:
		kafka_path = options.kafkapath
	else:
		kafka_path = input("kafka path : ")

	is_all = options.all

	if options.topics:
		topics = [t.strip() for t in options.topics.split(",")]
	elif options.topics_file:
		topics = read_from_topics_file(options.topics_file)
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

	if topics == None and options.all == False:
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

	if error:
		print ("Reassignment plan generation failed with error : {}".format(str(error)))
		exit(2)

	plan_csv = json_2_csv(plan_json)

	plan_csv = editor.edit(contents=plan_csv)

	write_to_file_csv(plan_csv)

def edit_plan():
	if not os.path.isfile(os.path.expanduser("~/.plan.csv")):
		print ("No ressasignment in progress!")
		exit(0)

	with open(os.path.expanduser("~/.plan.csv")) as openfile:
		csv_plan = openfile.read()

	plan_csv = editor.edit(contents=csv_plan)

	write_to_file_csv(plan_csv)

def deploy(options):
	if not os.path.isfile(os.path.expanduser("~/.plan.csv")):
		print ("No ressasignment in progress!")
		exit(0)

	print ("Using the following Plan")
	print ("\n")
	show_plan(frmt="csv")
	print ("\n")
	show_plan(frmt="json")

	if options.zookeeper:
		zookeeper = options.zookeeper
	else:
		zookeeper = input("Zookeeper : ")
	pass

	if options.kafkapath:
		kafka_path = options.kafkapath
	else:
		kafka_path = input("kafka path : ")

	with open(os.path.expanduser("~/.plan.csv")) as plan:
		csv_data = plan.read()

	plan_json = csv_2_json(csv_data)

	error, plan_json_file = execute_plan(zookeeper=zookeeper, plan_json=plan_json, kafka_path=kafka_path)

	if error:
		print ("Reassignment plan execution failed with error : {}".format(str(error)))
		exit(2)

	print ("Plan executed successfully!")
	print ("Please execute migrator -v to verify reassignment")

def verify(options):
	if not os.path.isfile(os.path.expanduser("~/.plan.json")):
		print ("No ressasignment plan present!")
		exit(0)

	plan_json_file = os.path.expanduser("~/.plan.json")

	if options.zookeeper:
		zookeeper = options.zookeeper
	else:
		zookeeper = input("Zookeeper : ")
	pass

	if options.kafkapath:
		kafka_path = options.kafkapath
	else:
		kafka_path = input("kafka path : ")

	error, status = verify_plan(zookeeper=zookeeper, kafka_path=kafka_path, plan_json_file=plan_json_file)

	if error:
		print ("Reassignment plan verification failed with error : {}".format(str(error)))
		exit(2)

	print (status)

def show_plan(frmt="csv"):
	plan_csv = os.path.expanduser("~/.plan.csv")

	if not os.path.isfile(plan_csv):
		print ("No plan present")
		return

	print ("\n")
	with open(plan_csv) as f:
		data_csv = f.read()

	if frmt == "csv":
		print (show_table(data_csv))
		print ("\n")
		return

	data_json = csv_2_json(data_csv)

	print (json.dumps(data_json, indent=2))

	print ("\n")

def show_table(plan_csv):
	rows_temp = plan_csv.split("\n")
	rows = []

	for row in rows_temp:
		if len(row) != 0:
			rows.append(row)

	headers = rows[0].split()
	body =  []

	for row in rows[1:]:
		body.append(row.split())

	return tabulate(body, headers, tablefmt="grid")

def setup_optparse():
	parser = optparse.OptionParser()
	parser.add_option('-p', '--kafkapath', dest='kafkapath', default="/opt/kafka/bin", help="Provide path to kafka binaries")
	parser.add_option('-a', '--all', dest="all", action="store_true", default=False, help="Select all the topics for moving")
	parser.add_option('-f', '--filter', dest="filter", help="Regex to filter topic names")
	parser.add_option('-t', '--topics', dest='topics', help="Comma separated topics")
	parser.add_option('-k', '--topics-file', dest="topics_file", help="File containing list of topics to move")
	parser.add_option('-z', '--zookeeper', dest='zookeeper', help="Provide zookeeper host/ip. If port used is different from 2181, then provide host:port")
	parser.add_option('-b', '--brokers', dest="brokers", help="Provide broker ids separated by comma")
	parser.add_option('-e', '--edit', dest="edit", action="store_true", default=False, help="Edit current plan" )
	parser.add_option('-d', '--deploy', dest="deploy", action="store_true", default=False, help="Deploy the plan" )
	parser.add_option('-v', '--verify', dest="verify", action="store_true", default=False, help="Verify execution" )
	parser.add_option('-c', '--clean', dest="clean", action="store_true", default=False, help="Clean any reassignmnet data")
	parser.add_option('-l', '--list', dest="list_partitions", action="store_true", default=False, help="List partition reassignments")
	parser.add_option('-j', '--list-json', dest="list_partitions_json", action="store_true", default=False, help="List partition reassignments in json format")

	options, args = parser.parse_args()

	return options

if __name__ == "__main__":
	drive()
