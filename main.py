from canvas_todo import config, canvas_todo


if __name__ == "__main__":
    
    import argparse

    parser = argparse.ArgumentParser()    
    parser.add_argument(
        "command",
        help="command to execute (config, run, ... <TODO>"
    )

    args = parser.parse_args()

    # configure canvas todo app
    if args.command == "config":
        config.gen_config()

    # run canvas todo app
    elif args.command == "run":
        c_todo = canvas_todo.CanvasTodo()
        c_todo.run()
