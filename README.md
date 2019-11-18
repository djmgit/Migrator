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

## Installing Migrator

- Clone this repo on your machine (or remote server)
- Change your working directory to this repository.
- Execute : ```sudo python3 setup.py install```
- Verify your installation using ```migrator --help```

The machine where where you will install Migrator should have the kafka binaries installed on them.
By default Migrator looks for kafka binaries under /opt/kafka/bin. If your binaries are located elsewhere, you
can pass it to Migrator using the --kakfapath option. Dont worry even if you forget to pass the path, Migrator
will automatically ask for it.
