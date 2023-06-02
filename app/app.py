import json
import os
import sqlite3

from flask import Flask, jsonify, request


DB_BASH_PATH = os.environ.get("TODO_DB_PATH", "/data")
DB_PATH = os.path.join(DB_BASH_PATH, "todo-list.db")
TABLE_NAME = "ToDoList"
app = Flask("ToDoList")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        f"CREATE TABLE if not exists {TABLE_NAME} (ITEM TEXT NOT NULL, CONSTRAINT name_unique UNIQUE (ITEM));"
    )
    return conn


def add_item(item):
    app.logger.info(f"Adding {item}")
    conn = get_db()
    conn.execute(f"INSERT INTO {TABLE_NAME} (ITEM) VALUES ('{item}');")
    conn.commit()


def delete_item(item):
    app.logger.info(f"Delete {item}")
    conn = get_db()
    conn.execute(f"DELETE FROM {TABLE_NAME} WHERE ITEM = '{item}';")
    conn.commit()


@app.route("/add", methods=["POST"])
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
        conn = get_db()
        _data = conn.execute(f"select * from {TABLE_NAME}")
        for row in _data:
            res["items"].append(row[0])

        response = jsonify(res)
        return response
    except Exception as ex:
        app.logger.error(f"Error: {ex}")
        return json.dumps({"status": False})


@app.route("/del", methods=["POST"])
def delete_from_list():
    try:
        data = request.json
        delete_item(data["item"])
        data["status"] = True
        return data
    except Exception as ex:
        app.logger.error(f"Error: {ex}")
        return json.dumps({"status": False})


def main():
    app.logger.info(f"Starting {app.name}")
    app.run(port=5000, host="0.0.0.0", use_reloader=False)


if __name__ == "__main__":
    main()
