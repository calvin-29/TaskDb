import sqlite3 as sq
import sys
import os

commands = sys.argv
if commands:
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
    not_allowed_names = ["-add", "--priority", "-list", "-done", "-delete"]
    if "-add" in commands:
        if "--priority" not in commands:
            print("no priority mentioned")
            exit()
        name = None
        priority = None

        try:
            name = commands[commands.index("-add")+1]
            priority = commands[commands.index("--priority")+1]
        except IndexError:
            print("No name or priority added")
        except Exception as e:
            print(e)
        else:
            if priority.lower() not in ["high", "med", "low"]:
                print("priority has to be high, med, low not {}".format(priority))
                exit()
            elif name.lower() in not_allowed_names:
                print(f"names can not be {''.join(not_allowed_names)}")
                exit()
            else:
                try:
                    cursor.execute(
                        """INSERT INTO tasks (name, priority, done) VALUES (?, ?, ?)""",
                        (name, priority.lower(), False)
                    )
                    conn.commit()
                    print("Finished")
                except Exception as e:
                    print(e)
    
    elif "-list" in commands:

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
    
    elif "-done" in commands:
        try:
            id = commands[commands.index("-done")+1]
        except IndexError:
            print("No id or s/n added")
        except Exception as e:
            print(e)
        else:
            try:
                cursor.execute("UPDATE tasks SET done=? WHERE id=?", (1, int(id)))
                conn.commit()
            except Exception as e:
                print(e)
    
    elif "-delete" in commands:
        try:
            id = commands[commands.index("-delete")+1]
        except IndexError:
            print("No id or s/n added")
        except Exception as e:
            print(e)
        else:
            try:
                cursor.execute("DELETE FROM tasks WHERE id=?", (int(id),))
                conn.commit()
            except Exception as e:
                print(e)
    
    elif "-clear" in commands:
        cursor.execute("DELETE FROM tasks")
        conn.commit()

    conn.close()
else:
    # error message
    print("Command not found")