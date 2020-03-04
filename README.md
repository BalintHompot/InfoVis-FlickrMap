# InfoVis Assignment #

This is the Information Visualization of team 15. We are using the Flickr dataset to show the development of tags used over time, throughout the world. 

## Planning ##

### Week 4 To-Dos - Before 27-02-2020 ###
Balint: Create the world map in D3

Neeraj and Vignesh: Creating a dynamic barchart

Urscha: Putting together the dataset for the backend

Martijn: Looking for other datasets to add to the visualization for extra depth

### Week 5 To-Dos - Before 05-03-2020 ###

Everyone: Assignment for next week

Balint: 

Urscha: Finishing the dataset: mapping country codes, looking at camera type in the metadata, filtering only useful tags, categorizing the tags.

Neeraj: Charts and donut integration with the map.

Vignesh: Charts and donut integration with the map.

Martijn: Counting the tags per country and per timestep of 1 month. Converting the data to json format and adding the precalculated top 5 tags per country per timestep.

## Requirements ##

See the requirements.txt file
You can automatically install all the requirements by running: pip install -t requirements.txt

## How it works ##

You can get the app to run in your local browser by following the steps below.

### Linux & Mac ###

* The app can be started by running: bash start_app.sh
* The app can then be accessed by navigating to http://127.0.0.1:5000/

### Windows ###

* Type the following in your terminal when using windows CMD: set FLASK_ENV=development **OR** when using windows powershell: $env:FLASK_ENV=development
* Followed by: python run.py
* The app can then be accessed by navigating to http://127.0.0.1:5000/
