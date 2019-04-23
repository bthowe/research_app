# Objective
This app has three endpoints: summary, datasets, and quit. 
The first two let me enter information about relevant papers and datasets. The latter enpoint kills the server.
The app is run using the bash script "run.sh". 
After killing the server, the script backs up the database and then terminates mongod.    

todo
2. button that returns to previous query in table_viewer
    1. put a button in the navbar next to "View Database"
    2. I have the collection name already.
    3. What else am I going to need? A date if there is one. For now assume there isn't 

2. bit more of a margin under the navbar 

3. Expand the search ability in the data viewer

5. The data portions of the summary and data sections are too small

2. Is there a way to close the current tab after shutdown?
    1. Using selenium...but short of this, it doesn't look easy to do.
