from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
FILE = "tasks.json"

# cria arquivo se não existir
if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump([], f)

def load_tasks():
    with open(FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=2)

# AGENT
def analyze_task(title):
    title = title.lower()
    if "urgente" in title or "hoje" in title:
        return "alta"
    elif "estudar" in title or "importante" in title:
        return "media"
    else:
        return "baixa"

@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form["title"]
    tasks = load_tasks()

    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "priority": analyze_task(title)
    }

    tasks.append(new_task)
    save_tasks(tasks)

    return redirect("/")

# 👇 AQUI (mesmo nível das outras funções)
@app.route("/delete/<int:id>")
def delete_task(id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != id]
    save_tasks(tasks)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
