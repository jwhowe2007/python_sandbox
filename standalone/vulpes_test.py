def edit_task(self):
    print("Select task ID")
    for ID, t in self.tasks.items():
        print(f"{ID}: {t.name}")
    ID = (input("Enter task ID:")).strip()
    if ID not in self.tasks.keys():
        print("Invalid ID")
        self.menu()

    else:
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
        if num=="1":
            new_name = input("Enter new task name/description:")
            task.name = new_name
            print(f"Task name updated to: {new_name}")
            self.menu()
        elif num=="2":
            new_length = input("Enter new task time commitment (hours):")
            try:
                new_length = float(new_length)
                task.length = new_length
                print(f"Task time commitment updated to: {new_length} hours")
                self.menu()
            except ValueError:
                print("Invalid input. Please enter a number.")
                self.menu()
        elif num=="3":
            new_priority = (input("Enter new task priority from 1(low) to 5(high): ")).strip()
            if new_priority in ["1","2","3","4","5"]:
                task.priority = int(new_priority)
                print(f"Task priority updated to: {new_priority}")
                self.menu()
            else:
                print("Invalid input. Priority must be a number between 1 and 5.")
                self.menu()
        elif num=="4":
            if (input("Does this task have a complete-by date? [y/yes]")).strip().lower() in ["y","yes"]:
                try:
                    end_date = (input("Enter complete-by date: [mm/dd/yy]")).strip()
                    end_datetime = datetime.strptime(end_date, '%m/%d/%y')
                    task.endDatetime = end_datetime
                    print(f"Task complete-by date updated to: {end_date}")
                    self.menu()
                except ValueError:
                    print("Invalid date format. Please use mm/dd/yy format.")
                    self.menu()
            else:
                task.endDatetime = None
                print("Task complete-by date removed.")
                self.menu()
        elif num=="5":
            if (input("Is this task dependent on others completed first? [y/yes]")).strip().lower() in ["y","yes"]:
                new_tasks = (input("Enter task names, separated by commas:")).split(",")
                new_tasks = [t.strip() for t in new_tasks]
                task.dependence = new_tasks
                print(f"Task dependencies updated to: {new_tasks}")
                self.menu()
            else:
                task.dependence = []
                print("Task dependencies removed.")
                self.menu()
        else:
            print("Invalid choice")
            self.menu()