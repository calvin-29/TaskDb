# TaskDb
A command-line task manager. Add, list, complete and delete tasks stored in a local SQLite database.

usage: main.py [-h] [-add ADD] [--priority PRIORITY] [-list] [-done DONE] [-r R] [-delete DELETE] [-clear]

A simple script to manage tasks in a db.

options:
  -h, --help            show this help message and exit
  -add, -a ADD          Add a task
  --priority, --p PRIORITY
                        Put a priority level for task (used with -add).
  -list, -l             List all the task by order of priority.
  -done DONE            Check a task as done
  -r R                  Check a task as not done
  -delete, -d DELETE    Delete a task
  -clear, -c            Delete all tasks

Adding a task:
    python main.py -add "Clean my room" --priority med
    python main.py -a "Clean my room" --p med

Showing the tasks in a table form:
    python main.py -list
    python main.py -l

Checking a task as done:
    python main.py -done 1

Checking a task as not done:
    python main.py -r 1

Deleting a task:
    python main.py -delete 1
    python main.py -d 1

Clearing all tasks:
    python main.py -clear
    python main.py -c
