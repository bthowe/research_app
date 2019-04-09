# Objective
This app has three endpoints: summary, datasets, and quit. 
The first two let me enter information about relevant papers and datasets. The latter enpoint kills the server.
The app is run using the bash script "run.sh". 
After killing the server, the script backs up the database and then terminates mongod.    

todo
1. table viewer
    1. View entries
        1. default sort by entry data
        2. allow other searches
    2. Have a button that allows me to edit.
2. In the paper description page, put in a "save" capability.
2. Is there a way to close the current tab?
    1. Using selenium...but short of this, it doesn't look easy to do.
