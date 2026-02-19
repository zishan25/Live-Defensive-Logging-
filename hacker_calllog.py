import sqlite3
import os
import json
from datetime import datetime
from colorama import Fore, Style, init
from tabulate import tabulate
import getpass

init(autoreset=True)

DB_NAME = "hacker_calllog.db"
PASSWORD = "admin123"   # এখানে পাসওয়ার্ড পরিবর্তন করতে পারো

def clear():
    os.system("clear")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            type TEXT,
            duration INTEGER,
            datetime TEXT
        )
    """)
    conn.commit()
    conn.close()

def login():
    clear()
    print(Fore.GREEN + Style.BRIGHT + "\n💀 HACKER CALL LOG SYSTEM 💀\n")
    pwd = getpass.getpass("🔐 Enter Password: ")
    if pwd != PASSWORD:
        print(Fore.RED + "❌ Access Denied!")
        exit()
    print(Fore.CYAN + "✅ Access Granted!\n")

def add_log():
    name = input("Name: ")
    phone = input("Phone: ")
    call_type = input("Type (Incoming/Outgoing/Missed): ")
    duration = int(input("Duration (seconds): "))
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO logs (name, phone, type, duration, datetime) VALUES (?,?,?,?,?)",
              (name, phone, call_type, duration, date_time))
    conn.commit()
    conn.close()

    print(Fore.GREEN + "\n✅ Log Added!\n")

def view_logs():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM logs")
    rows = c.fetchall()
    conn.close()

    print(Fore.GREEN + "\n📞 CALL LOG DATABASE\n")
    print(tabulate(rows, headers=["ID","Name","Phone","Type","Duration","DateTime"], tablefmt="fancy_grid"))

def delete_log():
    view_logs()
    log_id = input("\nEnter ID to delete: ")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM logs WHERE id=?", (log_id,))
    conn.commit()
    conn.close()

    print(Fore.RED + "\n🗑️ Log Deleted!\n")

def statistics():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM logs WHERE type='Incoming'")
    incoming = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM logs WHERE type='Outgoing'")
    outgoing = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM logs WHERE type='Missed'")
    missed = c.fetchone()[0]

    conn.close()

    print(Fore.YELLOW + "\n📊 STATISTICS")
    print(f"Incoming: {incoming}")
    print(f"Outgoing: {outgoing}")
    print(f"Missed: {missed}\n")

def export_json():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM logs")
    rows = c.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "name": row[1],
            "phone": row[2],
            "type": row[3],
            "duration": row[4],
            "datetime": row[5]
        })

    with open("calllog_export.json", "w") as f:
        json.dump(data, f, indent=4)

    print(Fore.CYAN + "\n📁 Exported to calllog_export.json\n")

def main():
    init_db()
    login()

    while True:
        print(Fore.GREEN + Style.BRIGHT + """
╔══════════════════════════════╗
║      💀 HACKER EDITION 💀     ║
╠══════════════════════════════╣
║ 1. Add Call Log              ║
║ 2. View Logs                 ║
║ 3. Delete Log                ║
║ 4. Statistics                ║
║ 5. Export to JSON            ║
║ 6. Exit                      ║
╚══════════════════════════════╝
""")

        choice = input("Choose option: ")

        if choice == "1":
            add_log()
        elif choice == "2":
            view_logs()
        elif choice == "3":
            delete_log()
        elif choice == "4":
            statistics()
        elif choice == "5":
            export_json()
        elif choice == "6":
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
