# GDELT on Elasticsearch.
#TODO: explain HISTORIC and REALTIME.

# Environment Variables
`KEY`: Explain here.


# GDELT Data Files
Explain python downloaders here.

# TODO
- ~~Process KGK~~
- ~~Process Mentions~~
- Automaticaly create gdelt index and schema

# Run it
Make sure you have a healthy elasticsearch node ready.

1. Install python requirements with `pip install -r config/requirements.txt`
2. Set the env vars: https://github.com/panchicore/es-gdelt/blob/master/config/enviroment_variables.sample.sh, use `source enviroment_variables.sample.sh`
2. Install the elasticsearch index: `python gdelt_create_index.py` 
3. Collect real time gdelt records: `gdelt_realtime_downloader.py`


