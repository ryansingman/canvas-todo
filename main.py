from canvas_todo import config


if __name__ == "__main__":
    
    import argparse

    parser = argparse.ArgumentParser()    
    parser.add_argument(
        "command",
        help="command to execute (config, ... <TODO>"
    )

    args = parser.parse_args()

    if args.command == "config":
        config.gen_config()
