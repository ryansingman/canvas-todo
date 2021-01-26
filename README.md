# canvas-todo
Automatically adds Canvas assignments to Google Keep

## Installation

You can install this package by cloning to your local machine and installing the necessary python packages

```bash
$ git clone https://github.com/ryansingman/canvas-todo.git && cd canvas-todo
$ pip install -r requirements.txt
```

## Setup

You can set up the app by using the built-in config tool, as follows, and follow the prompts:

```bash
$ python main.py config
```

> The prompt `Canvas URL: ` is referring to the URL of your Canvas LMS. For Virginia Tech students, this will be `https://canvas.vt.edu`.

> The prompt `Canvas Key:` is referring to your Canvas access token. To create a Canvas access token, you can follow the instructions [here](https://community.canvaslms.com/t5/Student-Guide/How-do-I-manage-API-access-tokens-as-a-student/ta-p/273).

## Running the App

You can run the app using the following command:

```bash
$ python main.py run
```

> For now, all this will do is print your completed and upcoming assignments for each course at your prompting. There is no Google Keep or other todo application integration at this point.