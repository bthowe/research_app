source ~/VirtualEnvironments/howeschool_app/bin/activate

mongod --fork --logpath db_backup/mongo_log/mongod.log
open -a "Google Chrome" http://0.0.0.0:8001/summary
gunicorn --bind 0.0.0.0:8001 command:app

mongodump -d papers -o db_backup
mongoexport --host localhost --db papers --collection data --type=csv --out db_backup/papers_data.csv --fields data_source,outcomes,covariates
mongoexport --host localhost --db papers --collection summary --type=csv --out db_backup/papers_summary.csv --fields citation,date_added,objective,t_model,e_model,data,conclusions

killall mongod
deactivate
