# Objective
This app has three endpoints: summary, datasets, and quit. 
The first two let me enter information about relevant papers and datasets. The latter enpoint kills the server.
The app is run using the bash script "run.sh". 
After killing the server, the script backs up the database and then terminates mongod.    

# todo
2. If I refresh after an update, the old stuff shows up...is there a way to update the original payload.

3. The plus and minus buttons are arranged in a hideous way...too much space in between

2. Don't list anything in the page if data_source is "None"  

2. button that returns to previous query in table_viewer
    1. put a button in the navbar next to "View Database"
    2. I have the collection name already.
    3. What else am I going to need? A date if there is one. For now assume there isn't 

2. bit more of a margin under the navbar 

3. Expand the search ability in the data viewer

5. The data portions of the summary and data sections are too small

2. Is there a way to close the current tab after shutdown?
    1. Using selenium...but short of this, it doesn't look easy to do.



# big extensions
1. pull list of papers from box papers directory
2. if there are new papers
    1. email informing what these are
    2. include title of the paper and the abstract
3. have a running list of the papers
4. need to have a way to organize by category
5. have I read the paper and written a summary?
6. download the paper and put in local directory
curl https://api.box.com/2.0/folders/0 -H \
"Authorization: Bearer NQJ9j30lWES5dXqth546LBreRJBUbziY"