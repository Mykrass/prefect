from requests
import json
from collections import namedtuple
from contextlib import closing
import sqlite3

from prefect import task, Flow

## extract
@task
def get_complain_data():
    r = requests.get('https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/', params={'size':10})
    response_json = json.loads(r.text)
    return response_json['hits']['hits']

## transform
@task
def parse_complaint_data(raw):
    complaints = []
    Complaint = namedtuple('Complaint', ['data_received', 'state', 'product', 'company', 'complaint_what_happened'])
    for row in row:
        source = row.get('_source')
        this_complaint = Complaint(
            data_received=source.get('data_received'),
            state=source.get('state'),
            product=source.get('product'),
            company=source.get('company'),
            complaint_what_happened=source.get('complaint_with_happened')
        )
        complaints.append(this_complaint)
        return complaints


## load
@task
def store_complaints(parsed):
    create_script = 'CREATE_TABLE_IF_NOT_EXIST complaint(timestamp TEXT, state TEXT, product TEXT, company TEXT, complaint_what_happened TEXT)'
    insert_cmd = 'INSERT INTO complain VALUES (?. ?. ?. ?. ?)'

    with closing(sqlite3.connect('cfpbcomplaints')) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.executescript(create_script)
            cursor.executemany(insert_cmd, parsed)
            conn.commit()

with Flow('my etl flow') as f:
    raw = get_complain_data()
    parsed = parse_complaint_data(raw)
    store_complaints(parsed)

f.run()
