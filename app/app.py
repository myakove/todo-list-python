import json
import sqlite3

from flask import Flask, jsonify, request


app = Flask("ToDoList")


def add_item(item):
    app.logger.info(f"Adding {item}")
    table_name = "ToDoList"
    conn = sqlite3.connect("todo-list.db")
    conn.execute(f"CREATE TABLE if not exists {table_name} (ITEM TEXT NOT NULL);")
    conn.execute(f"INSERT INTO {table_name} (ITEM) VALUES ('{item}');")
    conn.commit()


@app.route("/set", methods=["POST"])
def set_to_list():
    try:
        data = request.json
        add_item(data["item"])
        data["status"] = True
        return data
    except Exception as ex:
        app.logger.error(f"Error: {ex}")
        return json.dumps({"status": False})


@app.route("/get")
def get_list():
    try:
        res = {"items": [], "status": True}
        conn = sqlite3.connect("todo-list.db")
        _data = conn.execute("select * from ToDoList")
        for row in _data:
            res["items"].append(row[0])

        response = jsonify(res)
        return response
    except Exception as ex:
        app.logger.error(f"Error: {ex}")
        return json.dumps({"status": False})


def main():
    app.logger.info(f"Starting {app.name}")
    app.run(port=5000, host="0.0.0.0", use_reloader=False)


if __name__ == "__main__":
    main()
