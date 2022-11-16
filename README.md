[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=8874528&assignment_repo_type=AssignmentRepo)

# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Team Members
- [Anvi Agarwal](https://github.com/agarwalanvi01) (aa7140)
- [Tiffany Lee](https://github.com/les5185) (el2765)
- [Wuji Cao](https://github.com/cwj2099) (wc1629)
- [Larry Li](https://github.com/86larryli) (zl2902)

## Product vision statement

A website where you can create daily motivational promises to yourself and visualize the accomplishment to promote consistent motivation. 

## User stories

https://github.com/software-students-fall2022/web-app-exercise-team-13-1/issues


## Wireframes

Use the link below to check our wireframes :

https://www.figma.com/file/8FzmxcMe926TtobNgbP4C9/Untitled?node-id=0%3A1

## Task boards

### Sprint 1

https://github.com/orgs/software-students-fall2022/projects/12/views/1

### Sprint 2

https://github.com/orgs/software-students-fall2022/projects/35

## Setup

### Insert Sample Data

- In your MongoDB shell, switch to database `team13db` by running command `use team13db`.

- Then, copy the command in `back-end/insert-data.js` and run it in your MongoDB shell.

### Install Dependencies

- Inside the `back-end` folder, run `pip3 install -r requirements.txt`.

### Create `.env`

- Create your `.env` file in side the `back-end` folder.

    - You can either modify `back-end/env.example` or use the `.env` file provided in the [discord channel](https://discord.com/channels/1014892538601152572/1029898964729872468/1034549521377673346).

## Run the App

- In side the `back-end` folder:

    - Define two environment variables from the command line:

        - on Mac, use the commands: `export FLASK_APP=app.py` and `export FLASK_ENV=development`.

        - on Windows, use `set FLASK_APP=app.py` and `set FLASK_ENV=development`.

    - Start flask with `flask run` - this will output an address at which the app is running locally, e.g. https://127.0.0.1:5000. Visit that address in a web browser.

    - In some cases, the command `flask` will not be found when attempting `flask run`... you can alternatively launch it with `python3 -m flask run --host=0.0.0.0 --port=10000`.
