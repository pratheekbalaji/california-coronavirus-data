# California Coronavirus Data 

## Overview
This repository contains data related to coronavirus cases and deaths in california  other additional details and visualizations in the file resulting.py
## Installation

First, start by closing the repository:

git clone https://github.com/pratheekbalaji/california-coronavirus-data.git

We recommend using pip to create virtual environment
- Create a new virtual environment with a given name

- python3 -m venv env_name    

- Activate the environment

source env_name/bin/activate

- Install the dependencies to run the project

pip install -r requirements.txt


## Instatition

We can  run the visualization script as follow


bokeh serve --show resulting.py

To stop the server , use Ctrl + C

## Serving the visualization through Docker

1) Download Docker Desktop from the following url https://docs.docker.com/get-docker/

2) Go to your cloned repository folder 
   cd california-coronavirus-data
3) Create a dockerfile as follows
- touch Dockerfile
4) Edit the dockerfile as follows:
- vi Dockerfile
'''
FROM python:3
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD resulting.py /app
ADD latimes-state-totals.csv /app
ADD cdph-race-ethnicity.csv /app
CMD ["bokeh","serve","--show", "/app/resulting.py", "--port", "5002"]
'''
