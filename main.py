import sqlite3 as sq
import argparse

parser = argparse.ArgumentParser(description='A simple script to manage tasks in a db.')

conn = sq.connect('tasks.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        priority TEXT,
        done INTEGER
    )
""")

parser.add_argument('-add', type=str, help='Add a task')
parser.add_argument('--priority', '--p', type=str, help='Put a priority level for task (used with -add).')
parser.add_argument('-list', action="store_true", help='List all the task by order of priority.')
parser.add_argument('-done', type=int, help='Check a task as done')
parser.add_argument('-r', type=int, help='Check a task as not done')
parser.add_argument('-delete', type=int, help='Delete a task')
parser.add_argument('-clear', action="store_true", help='Delete all tasks')

args = parser.parse_args()

if args.add:
    if not args.priority:
        print("no priority mentioned")
        exit()

    name = args.add
    priority = args.priority
    
    if priority.lower() not in ["high", "med", "low"]:
        print("priority has to be high, med, low not {}".format(priority))
        exit()
    else:
        try:
            cursor.execute(
                """INSERT INTO tasks (name, priority, done) VALUES (?, ?, ?)""",
                (name, priority.lower(), False)
            )
            conn.commit()
            print("Finished")
        except sq.IntegrityError:
            print("This task already exist")
        except Exception as e:
            print(e)
elif args.list:
    sn = f"S/N{' '*5}"
    name_col = f" NAME{' '*30}"
    priority_col = f" PRIORITY{' '*10}"
    done_col = f" DONE{' '*10}"

    head = f"{sn}|{name_col}|{priority_col}|{done_col}"
    print(head)
    print("-"*len(head))

    high = []
    med = []
    low = []
    for i in cursor.execute("""SELECT * FROM tasks""").fetchall():
        if i[2] == "high":
            high.append(i)
        elif i[2] == "med":
            med.append(i)
        elif i[2] == "low":
            low.append(i)
    
    def get(i):
        space = " "*(len(sn) - len( str(i[0]) ))
        num = f"{i[0]}{space}"

        space1 = " "*(len(name_col) - 1 - len( str(i[1]) ))
        dot = "..." if len(i[1]) > len(name_col)-4 else ""
        nam = f" {i[1][:len(name_col)-4]}{dot}{space1}"

        space2 = " "*(len(priority_col) - 1 - len( str(i[2]) ))
        prior = f" {i[2]}{space2}"

        space3 = " "*(len(done_col) - len( str(bool(i[3])) ))
        done = f" {str(bool(i[3]))}{space3}"

        return f"{num}|{nam}|{prior}|{done}"
    
    for i in [high, med, low]:
        for j in i:
            print(get(j))

elif args.done or args.r:
    id = args.done if args.done else args.r
    try:
        cursor.execute("UPDATE tasks SET done=? WHERE id=?", (0 if args.r else 1, int(id)))
        conn.commit()
    except Exception as e:
        print(e)

elif args.delete:    
    id = args.delete
    try:
        cursor.execute("DELETE FROM tasks WHERE id=?", (int(id),))
        conn.commit()
    except Exception as e:
        print(e)

elif args.clear:
    try:
        cursor.execute("DELETE FROM tasks")
        conn.commit()
    except Exception as e:
        print(e)

conn.close()
