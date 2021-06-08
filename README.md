# threadnews-backend

This is the source code to the backend for ThreadNews web application developed for CSC 308/309. [![Build Status](https://www.travis-ci.com/ThreadNews/threadnews-backend.svg?branch=dev)](https://www.travis-ci.com/ThreadNews/threadnews-backend)

## Information

Code Formatters Used: 
Black  

Developers should follow these instructions to set up [Black](https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0) formatting for VSCode


## Setup Guide

Pre-setup:
Recommend using python virtual environment to create a sandbox for the project and allows for separation of your local python installation with this project's setup. Additionally, a configuration file will be setup in .config directory with a file name api.conf. The format of which will be generated after the first run of the code. Another option is to use environmental variables.

The required environmental variables are:

``` bash
export JWTSECRET = ...
export MONGOPASS = ...
export MONGOURL = ...
export MONGOUSER = ...
export NEWSAPIKEY = ...
```

### Steps to setup project

``` bash
pip install -r requirements.txt
gunicorn backend:app
```

After which, the backend should be started and running