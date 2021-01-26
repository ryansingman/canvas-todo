from canvas_todo import config, canvas_todo


if __name__ == "__main__":
    
    import argparse

    parser = argparse.ArgumentParser()    
    parser.add_argument(
        "command",
        help="command to execute (config, update, ... <TODO>"
    )

    args = parser.parse_args()

    if args.command == "config":
        config.gen_config()

    elif args.command == "update":
        c_todo = canvas_todo.CanvasTodo()
