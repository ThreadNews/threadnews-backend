# threadnews-backend [![Build Status](https://www.travis-ci.com/ThreadNews/threadnews-backend.svg?branch=dev)](https://www.travis-ci.com/ThreadNews/threadnews-backend)

This is the source code to the backend for ThreadNews web application developed for CSC 308/309.

## Information

Code Formatters Used: Black  

Developers should follow these instructions to set up [Black](https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0) formatting for VSCode

## Setup Guide

Pre-setup:
Recommend using python virtual environment to create a sandbox for the project and allows for separation of your local python installation with this project's setup. For more information on setting up a virtual environment, [please read here](https://docs.python.org/3/library/venv.html). Additionally, a configuration file will be setup in .config directory with a file name api.conf. The format of which will be generated after the first run of the code. Another option is to use environmental variables.

The required environmental variables to be set are:

``` bash
export JWTSECRET = ...
export MONGOPASS = ...
export MONGOURL = ...
export MONGOUSER = ...
export NEWSAPIKEY = ...
```

Using a configuration file within .config/, the format of api.conf will look like:

```txt
[NewsAPI]
key = YOURKEYHERE

[MongoDB]
URl = YOURURLHERE
user = YOURUSERHERE
password = YOURPASSWORDHERE

[JWT]
secret = YOURSECRETHERE
```

### Steps to setup project

``` bash
pip install -r requirements.txt
gunicorn backend:app
```

After which, the backend should be started and running

## Testing

Testing the code uses the pytest framework with pytest coverage. The packages are already included in the requirements.txt which will be installed on setup. All tests are contained in the test/ directory.

```bash
pytest test/

# To test for coverage
pytest --cov-report term --cov=utils/ test/
```

## CI Management

This project uses Travis CI to run a set of programs to ensure tests are working and code formatting is valid. Additionally, instead of using a configuration file, environmental variables are set within the travis application since the codes and passwords used in configuration are sensitive information for security purposes.

In particular, the project runs all tests and reports whether any have failed as well as the coverage of the project. Furthermore, the CI runs a code formatting check with black to check for bad formatting of the code.

To edit what the CI performs, edit .travis.yml to add new commands.

## Deployment

The deployment server is [heroku](https://threadnews-backend.herokuapp.com/). Since the project splits the frontend and backend into separate repositories, code for the backend will be ran within its own  heroku app.

Heroku deploys the code from the dev branch once the CI passes after an update. Heroku deploys based on the commands set in Procfile.

The current Procfile only contains the command

```bash
gunicron backend:app
```

Which begins the backend code.

Note: Heroku sleeps the application after a set time when inactive, thus, may take a while to start up