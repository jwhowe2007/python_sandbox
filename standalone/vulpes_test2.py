from datetime import datetime

def edit_task(self):
    print("Select task ID")
    for ID, t in self.tasks.items():
        print(f"{ID}: {t.name}")
    ID = (input("Enter task ID:")).strip()
    if ID not in self.tasks.keys():
        print("Invalid ID")
        self.menu()
        return  # Exit the function after invalid ID

    task = self.tasks[ID]
    print(f"{task.UID}:")
    print(f"1:    {task.name}")
    print(f"2: Time {task.length} hrs")
    print(f"3: Priority {task.priority}")
    print(f"4: Complete By {task.endDatetime}")
    print(f"5: Dependent on  {task.dependence}")
    print(f"Scheduled? {'Yes' if task.scheduled else 'No'}")
    print(f"Completed? {'Yes' if task.completed else 'No'}")
    num = (input("Enter entry number to edit (1-5):")).strip()
    if num == "1":
        new_name = input("Enter new task name/description: ").strip()
        task.name = new_name
        self.menu()
    elif num == "2":
        while True:
            new_length = input("Enter new time commitment (hours): ")
            try:
                new_length = float(new_length)
                break
            except ValueError:
                print("Please enter a valid number.")
        task.length = new_length
        self.menu()
    elif num == "3":
        while True:
            new_priority = input("Enter new priority (1-5): ").strip()
            if new_priority in ["1", "2", "3", "4", "5"]:
                break
            else:
                print("Please enter a number from 1 to 5.")
        task.priority = int(new_priority)
        self.menu()
    elif num == "4":
        while True:
            new_date = input("Enter new complete-by date [mm/dd/yy]: ").strip()
            try:
                new_datetime = datetime.strptime(new_date, '%m/%d/%y')
                break
            except ValueError:
                print("Invalid date format. Please use mm/dd/yy.")
        task.endDatetime = new_datetime
        self.menu()
    elif num == "5":
        deps = input("Enter task names separated by commas: ").strip()
        deps = [d.strip() for d in deps.split(',')]
        task.dependence = deps
        self.menu()
    else:
        print("Invalid choice")
        self.menu()