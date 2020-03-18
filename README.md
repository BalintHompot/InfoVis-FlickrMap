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

Balint: World map and steam graph

Urscha: Finishing the dataset: mapping country codes, looking at camera type in the metadata, filtering only useful tags, categorizing the tags.

Neeraj: Charts and donut integration with the map.

Vignesh: Charts and donut integration with the map.

Martijn: Counting the tags per country and per timestep of 1 month. Converting the data to json format and adding the precalculated top 5 tags per country per timestep.

### Week 6 To-Dos - Before 12-03-2020 ###

Balint: two instances of streamgraph,  allowing selection of 2 countries for the two sets of graphs,  focused stream graph should show tags (can only be done after update on data, tag color should be a version of category color.

Urscha: Categorize the tags, placement of glyphs, font type, colors etc., map missing data to grey, adding filter panels (category) , add colored list of categories.

Neeraj: fix position to country, add top tags (also requires data update), remove transition?

Vignesh: Tooltip alterations and donut chart of device category distribution

Martijn: adding top 5 tags per category (needed for tooltip, focused stream graph) 

## Week 7 To-Dos - Before 18-03-2020 ##

Design - Mainly Urscha
  - Placement of glyphs, font type, titles, colors etc. - Urscha
  - Fix stream graph design, ticks, titles - Urscha
  - Add information about visualization to the first page (from report) - Martijn
  - add play button (functions already implemented) - Balint/Urscha
  - remove right shift (coming from the template) - Urscha
  - tag filter position and design - Urscha
  - fix country name in panel - Balint
  - fix inherited text colors in side panels - Urscha
  - extra: reset button on side panels (to get back to World) - Balint

Functions - Balint
  - two instances of streamgraph - Balint
  - two instance of donut for comparison - Neeraj
  - allowing selection of 2 countries for the two sets of graphs - Balint
  - add colored list of categories - Balint
  - On reload plot the world map in the middle of the screen - Urscha

Data - Martijn
  - adding top 5 tags per category (needed for tooltip, focused stream graph) - Martijn
  - WORLD aggregation missing - Martijn
  - add sum of all_tags in category - Martijn
  - add sum of tags per category - Martijn

Streamgraph - Balint
  - focused stream graph should show tags (can only be done after update on data) Balint
  - Tag color should be a version of category color Balint
  - add other tags per category to focused Balint
  - exit data when refreshing focused Balint
  - Add ticks to top streamgraph as well - Balint
  - typeerror when dragged to the right side - Balint
  - zooming out should revert focused graph Balint
  - Chop off before 2003 or 2004. - Balint
  - Make streamgraph.js - Balint
  - zoom in and out fix to corresponding country - Balint
  - when clicked filter, add tag to filter text - Balint
  - make selection indicator  - Balint
  - Bugs with filtering, functionality and colors - Balint
	
Tooltip - Neeraj and Vignesh
  - Tooltip positioning Neeraj
  - add top tags (also requires data update) Neeraj
  - handle countries with no data Neeraj
  - add category distribution Neeraj
  - reduce the tooltip size to at least half  Vicky 
  - Fix the tiles of the tooltip (users → image, tags → category) - Urscha
  - remove category color list (and put it next to the map permanently) Vicky
  - disable tooltip during zoom Vicky
  - tooltip content is completely missing from the side bars- Neeraj
  - tooltip list should only have dots, not different symbols at the tags - Neeraj
  - there are some random shapes appearing in the tooltip after loading - Neeraj
  - Only show total top 5 tags in the tooltip, not per category since we cant scroll - Neeraj
  - Colors of the circles have to correspond to the category color- Neeraj
  - Make the positioning of the pie charts relative to the side panel svg’s - Neeraj
	
Donut chart - Neeraj and Vignesh
- donut chart of device category distribution Neeraj 
- link with map selection Neeraj
- Add labels Neeraj
- Add transitions (need discussion) Neeraj
- Place pie chart on the side panels Neeraj
- Link functionalities with donut chart Neeraj


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
