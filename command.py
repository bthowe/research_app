import sys
import json
import datetime
import subprocess
import pandas as pd
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, url_for, request, redirect, jsonify

pd.set_option('max_columns', 1000)
pd.set_option('max_info_columns', 1000)
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 30000)
pd.set_option('max_colwidth', 4000)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


app = Flask(__name__)
app.secret_key = 'mysecret'
bootstrap = Bootstrap(app)

db_papers = PyMongo(app, uri="mongodb://localhost:27017/papers")

@app.route('/summary', methods=['POST', 'GET'])
def summary():
    if request.method == 'POST':
        form = request.form

        data_sources = data_object_create(form)
        summary = summary_json(form, data_sources)
        print('Summary: {}'.format(summary))
        print('Data Sources: {}'.format(data_sources))

        ret_summary = db_papers.\
            db['summary'].\
            insert_one(summary)
        print('Summary document object: \n\t{}'.format(ret_summary.inserted_id))

        ret_data = db_papers.\
            db['data'].\
            insert_many(data_sources)
        print('Data document objects: \n\t{}'.format(ret_data.inserted_ids))

        return redirect(url_for('summary'))
    return render_template('summary.html')

@app.route('/datasets', methods=['POST', 'GET'])
def datasets():
    if request.method == 'POST':
        form = request.form

        data_sources = data_object_create(form)
        print('Data Sources: {}'.format(data_sources))

        ret_data = db_papers.\
            db['data'].\
            insert_many(data_sources)
        print('Data document objects: \n\t{}'.format(ret_data.inserted_ids))

        return redirect(url_for('datasets'))
    return render_template('datasets.html')

@app.route('/database_viewer', methods=['POST', 'GET'])
def database_viewer():
    return render_template('data_viewer.html', page_name='Table Viewer')

@app.route('/quit')
def quit():
    sys.exit(4)
    return ''



@app.route('/query_db', methods=['POST', 'GET'])
def query_db():
    js = json.loads(request.data.decode('utf-8'))

    collection = js['collection'].lower()

    docs = []
    docs += list(db_papers.db[collection].find({}, {'_id': False}))

    return jsonify(items=[{str(k): str(v) for k, v in doc.items()} for doc in docs])


def summary_json(form, data_sources):
    data = {
        "citation": form['Citation'],
        "date_added": str(datetime.datetime.today()),
        "objective": form['Objective'],
        "t_model": form['Theoretical Model'],
        "e_model": form['Empirical Approach'],
        "data": data_sources,
        "conclusions": form['Conclusions']
    }
    return data

def data_object_create(form):
    num_data_sources = int((len(list(form.keys())) - 5) / 3)
    return [{"data_source": form['Data_source' + str(i)], "outcomes": form['Outcomes' + str(i)], "covariates": form['Covariates' + str(i)]} for i in range(num_data_sources)]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
