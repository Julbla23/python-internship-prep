import json

class Task:
    def __init__(self, title, status=False):
        self.title = title
        self.status = status

#we need to convert our task object into a dictionary, because JSON cannot directly save custom Python objects
    def to_dict(self):
        return {
            "title": self.title,
            "status": self.status
        }


tasks = []

#dodawanie taska
t1 = Task("Get up")
tasks.append(t1)

#convert all tasks
tasks_as_dicts = []

for task in tasks:
    tasks_as_dicts.append(task.to_dict())

#opens the file, overwrites it and saves it. indent means it's prettily formatted
with open("tasks.json", "w", encoding="utf-8") as file:
    json.dump(tasks_as_dicts, file, indent=4)

