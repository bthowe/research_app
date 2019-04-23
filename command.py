import sys
import json
import joblib
import datetime
import subprocess
import pandas as pd
from flask_pymongo import PyMongo, ObjectId
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

        summary_id = joblib.load('static/summary_id') + 1
        data_sources = data_object_create(form, summary_id)
        summary = summary_json(form, data_sources, summary_id)
        print('Summary: {}'.format(summary))
        print('Data Sources: {}'.format(data_sources))

        ret_summary = db_papers.\
            db['summary'].\
            insert_one(summary)
        print('Summary document object: \n\t{}'.format(ret_summary.inserted_id))

        print([source for source in data_sources])
        ret_data = db_papers.\
            db['data'].\
            insert_many([source for source in data_sources])
        print('Data document objects: \n\t{}'.format(ret_data.inserted_ids))

        joblib.dump(summary_id, 'static/summary_id')
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

@app.route('/document_view', methods=['POST'])
def document_view():
    form = request.form

    document = document_json(form)
    print(document)

    if form['collection'] == 'Data':
        return render_template('data_document_view.html', doc=document, page_name='Document View')
    else:
        return render_template('summary_document_view.html', doc=document, page_name='Document View')

@app.route('/quit')
def quit():
    sys.exit(4)
    return ''



@app.route('/query_db', methods=['POST', 'GET'])
def query_db():
    js = json.loads(request.data.decode('utf-8'))

    collection = js['collection'].lower()

    docs = []
    docs += list(db_papers.db[collection].find({}))

    payload = []
    for doc in docs:
        document_dict = {}
        for k, v in doc.items():
            if k == '_id':
                document_dict[str(k)] = str(v)
            else:
                document_dict[str(k)] = v
        payload.append(document_dict)
    return jsonify(items=payload)

@app.route('/update_db', methods=['POST'])
def update_db():
    js = json.loads(request.data.decode('utf-8'))

    collection = js['collection'].lower()
    id = js['_id']
    covars_changed = js['covars_changed']
    if not covars_changed:
        return ''
    summary_id = int(float(js['summary_id']))

    js.pop('collection', None)
    js.pop('_id', None)
    js.pop('covars_changed', None)
    js['summary_id'] = summary_id

    query = { '_id':  ObjectId(id) }
    insert = {'$set': js}
    ret_data = db_papers. \
        db[collection]. \
        update_one(query, insert)
    if (collection == 'data'):
        query_summary = {'summary_id': summary_id}

        new_lst = []
        for source in list(db_papers.db['summary'].find(query_summary))[0]['data']:
            if source['data_source'] == js['data_source']:
                for covar in covars_changed:
                    source[covar] = js[covar]
            new_lst.append(source)

        insert_summary = {'$set': {'data': new_lst}}
        db_papers.db['summary'].update_one(query_summary, insert_summary)

    elif (collection == 'summary') and ('data' in covars_changed):
        for source in json.loads(js['data'].replace("'", '"')):
            query_data = {'summary_id': summary_id, 'data_source': source['data_source']}
            source['summary_id'] = summary_id
            insert_data = {'$set': source}

            db_papers.db['data'].update_one(query_data, insert_data)

    print('Data document objects: \n\t{}'.format(ret_data))
    return ''

def summary_json(form, data_sources, summary_id):
    data = {
        "citation": form['Citation'],
        "date_added": str(datetime.datetime.today()),
        "objective": form['Objective'],
        "t_model": form['Theoretical Model'],
        "e_model": form['Empirical Approach'],
        "data": data_sources,
        "conclusions": form['Conclusions'],
        "summary_id": summary_id
    }
    return data

def document_json(form):
    data = {}
    for key in form:
        if key == 'data':
            data_lst = []
            for data_string in form['data'][1:-1].split('},{'):
                if data_string[0] != '{':
                    data_string = '{' + data_string
                if data_string[-1] != '}':
                    data_string = data_string + '}'
                data_lst.append(json.loads(data_string))
            data[key] = data_lst
        else:
            data[key] = form[key]
    return data

def data_object_create(form, summary_id):
    num_data_sources = int((len(list(form.keys())) - 5) / 3)
    return [{"data_source": form['Data_source' + str(i)], "outcomes": form['Outcomes' + str(i)], "covariates": form['Covariates' + str(i)], "summary_id": summary_id} for i in range(num_data_sources)]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
