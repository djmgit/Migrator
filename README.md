## Migrator

Migrator is a CLI based tool for easy and flexible migration of kafka topic partions to given set of brokers
Migrator can used to easily move topic partions without using those long kakfa commands. Also it displays reassignment
data in simple and easy to understand/edit table format. It replaces those largy kafka-cli commands with short
and crisp commands.

### Features provided by Migrator

- Easy and short commands to generate reassignment plan and execute.verify it.
- Display and edit reassignment plan in simple table format rather than json
- View and edit your plan in table format as many times you want.
- Execute and verigy with quick short command
- If at any step you forget to provide a vital parameter, migrator itself will ask for it. So no issues even if you
  forget a parameter. No need to go back and search the kafka doc or lookup your history and copy that huge command.

### Installing Migrator

- Clone this repo on your machine (or remote server)

- Change your working directory to this repository.

- Execute : ```sudo python3 setup.py install```

- Verify your installation using ```migrator --help```

The machine where where you will install Migrator should have the kafka binaries installed on them.
By default Migrator looks for kafka binaries under /opt/kafka/bin. If your binaries are located elsewhere, you
can pass it to Migrator using the --kakfapath option. Dont worry even if you forget to pass the path, Migrator
will automatically ask for it.

### Usage

```
Usage: migrator [options]

Options:
  -h, --help            show this help message and exit
  -p KAFKAPATH, --kafkapath=KAFKAPATH
                        Provide path to kafka binaries
  -a, --all             Select all the topics for moving
  -f FILTER, --filter=FILTER
                        Regex to filter topic names
  -t TOPICS, --topics=TOPICS
                        Comma separated topics
  -k TOPICS_FILE, --topics-file=TOPICS_FILE
                        File containing list of topics to move
  -z ZOOKEEPER, --zookeeper=ZOOKEEPER
                        Provide zookeeper host/ip. If port used is different
                        from 2181, then provide host:port
  -b BROKERS, --brokers=BROKERS
                        Provide broker ids separated by comma
  -e, --edit            Edit current plan
  -d, --deploy          Deploy the plan
  -v, --verify          Verify execution
  -c, --clean           Clean any reassignmnet data
  -l, --list            List partition reassignments
  -j, --list-json       List partition reassignments in json format
```

Lets get into the usage of Migrator with few examples.

First lets try to move the topic topic-1 to brokers with ids 3,4. This can be done with the following  command

```
migrator -z 127.0.0.1 -t topic-1 -b 3,4
```
If you do not feel like typing so much, thats absolutely fine. You can just do the following:

```
migrator
```
and it will ask for required parameters:

```
migrator
Zookeeper : 127.0.0.1
Brokers (separated by comma) : 3,4
Topics to move (separated by comma) : topic-1

```

Once you provide all the parameters, it will generate the plan and open it in your terminal editior, in simple table format
(no json!)

```
Topic        Partition        Replicas        Log Dirs
topic-1        0                3,4            any,any
topic-1        1                4,3            any,any
```

Once you are satisfied with the plan, save and exit from the editor.

You can display the plan to review using the following:

```
migrator -l


+---------+-------------+------------+---------+
| Topic   |   Partition | Replicas   | Log     |
+=========+=============+============+=========+
| topic-1 |           0 | 3,4        | any,any |
+---------+-------------+------------+---------+
| topic-1 |           1 | 4,3        | any,any |
+---------+-------------+------------+---------+

 migrator -j


{
  "version": 1,
  "partitions": [
    {
      "topic": "topic-1",
      "partition": 0,
      "replicas": [
        3,
        4
      ],
      "log_dirs": [
        "any",
        "any"
      ]
    },
    {
      "topic": "topic-1",
      "partition": 1,
      "replicas": [
        4,
        3
      ],
      "log_dirs": [
        "any",
        "any"
      ]
    }
  ]
}
```
Yep! you can see the plan both in pretty table format and json format.

But wait, you have to make some last moment changes in your reassignment plan. Thats absolutely fine. All you need to
do is the following:

```
migrator -e
```
 That will open the existing plan in your terminal editor in table format.
 
 It should be noted here that, migrator allows only one reassignment to be done at a time. If you try to generate another
 reassignment plan at this moment, your previous plan's data will be replaced with the new one.


