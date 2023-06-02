from flask import Flask


app = Flask("ToDoList")


@app.route("/set", methods=["POST"])
def set_to_list():
    try:
        """"""
    except Exception as ex:
        app.logger.error(f"Error: {ex}")
        return "POST process failed"


@app.route("/get", methods=["GET"])
def get_list():
    try:
        """"""
    except Exception as ex:
        app.logger.error(f"Error: {ex}")
        return "GET process failed"


def main():
    app.logger.info(f"Starting {app.name}")
    app.run(port=5000, host="0.0.0.0", use_reloader=False)


if __name__ == "__main__":
    main()
