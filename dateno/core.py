#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import json
import logging
import os
import csv

import typer
import yaml
from flatdict import FlatDict
from tabulate import tabulate

import requests

DEFAULT_CONFIGFILE = ".dateno.yaml"

BASE_API_PATH = 'https://api.dateno.io'
SEARCH_API_PATH = BASE_API_PATH + '/index/0.1/query'
ENTRY_API_PATH = BASE_API_PATH + '/search/0.1/entry/{entry_id}'
REGISTRY_RECORD_API_PATH = BASE_API_PATH + "/registry/catalog/{catalog_id}"
REGISTRY_SEARCH_API_PATH = BASE_API_PATH + "/registry/search/catalogs/"

app = typer.Typer()
index_app = typer.Typer()
app.add_typer(index_app, name='index')
registry_app = typer.Typer()
app.add_typer(registry_app, name='catalogs')




class DatenoCmd(object):
    def __init__(self, debug:bool=False, apikey:str=None):
        # logging.getLogger().addHandler(logging.StreamHandler())
        self.apikey = apikey
        if debug:
            logging.basicConfig(
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                level=logging.DEBUG,
            )
        self.prepare()


    def prepare(self):
        rulepath = []
        filepath = None
        if os.path.exists(DEFAULT_CONFIGFILE):
            logging.debug("Local .dateno.yaml config exists. Using it")
            filepath = DEFAULT_CONFIGFILE
        elif os.path.exists(
            os.path.join(os.path.expanduser("~"), DEFAULT_CONFIGFILE)
        ):
            logging.debug("Home dir .dateno.yaml config exists. Using it")
            filepath = os.path.join(
                os.path.expanduser("~"), DEFAULT_CONFIGFILE
            )
        if filepath:
            f = open(filepath, "r", encoding="utf8")
            config = yaml.load(f, Loader=yaml.FullLoader)
            f.close()
            if config:
                if "apikey" in config.keys():
                    self.apikey = config["apikey"]
                elif self.apikey is None:
                    print('Error: API key (apikey) not found in .dateno.yaml and not provided with args.')
                    sys.exit(1)
            else:
                print('Error: Empty/not existing config file and apikey is empty')
                sys.exit(1)      

    def index_search(self, query, filters=[], offset=0, page=1, limit=500):
        url = SEARCH_API_PATH +'?q=' + query + f'&offset={offset}&page={page}&limit={limit}'
        url = url + '&apikey=%s' % (self.apikey)        
        for afilter in filters:
            if len(afilter.strip()) == 0: continue
            parts = afilter.split('=', 1)
            afilter = '"' + parts[0] + '"' + '=' + '"' + parts[1] + '"'
            url += f'&filters={afilter}'
        logging.debug(f'Requesting {url}')
        resp = requests.get(url)
        return resp.json()

    def index_get(self, entry_id):
        resp = requests.get(ENTRY_API_PATH.format(entry_id=entry_id) + '?apikey=%s' % (self.apikey))
        return resp.json()

    def registry_get(self, catalog_id):
        resp = requests.get(REGISTRY_RECORD_API_PATH.format(catalog_id=catalog_id) + '?apikey=%s' % (self.apikey))
        return resp.json()

    def registry_search(self, query):
        url = REGISTRY_SEARCH_API_PATH +'?q=' + query + '&apikey=%s' % (self.apikey)
#        for afilter in filters:
#            url += f'&filters={afilter}'
        resp = requests.get(url)
        print(resp.content)
        return resp.json()


@index_app.command('search')
def index_search(query, filters:str="", offset:int=0, page:int=1, limit:int=500, mode:str="results", format:str="yaml", headers:str='id,dataset.title', output:str=None, debug:bool=False, apikey:str=None):
    """Searches for datasets. Supports modes: results, raw, totals, facets"""
    cmd = DatenoCmd(debug, apikey)
    results = cmd.index_search(query, filters=filters.split(';'), offset=offset, page=page, limit=limit)
    if 'status' in results.keys():
        print('No results, status: %s' % (results['status']))
        return
    if output is not None:
        if mode == 'raw':
            f = open(output, 'w', encoding='utf8')
            f.write(json.dumps(results))
            f.close()
            print(f'Raw results saved to {output}')
        elif mode == 'results':
            outres = []
            for item in results['hits']['hits']:
                data = FlatDict(item['_source'], delimiter='.')
                record = []
                for h in headers.split(','):
                    record.append(data[h])
                outres.append(record)
            f = open(output, 'w', encoding='utf8')
            writer = csv.writer(f)
            writer.writerow(headers.split(','))
            writer.writerows(outres)
            f.close()
        elif mode == 'facets':
            if format == 'json':
                f = open(output, 'w', encoding='utf8')
                f.write(json.dumps(results['aggregations']))
                f.close()
            elif format == 'yaml':
                f = open(output, 'w', encoding='utf8')
                f.write(yaml.dump(results['aggregations'], default_flow_style=False))
                f.close()
        elif mode == 'totals':
            f = open(output, 'w', encoding='utf8')
            totals = results['hits']['total']['value']# if 'totalHits' in results.keys() else results['estimatedTotalHits']
            f.write(str(totals))
            f.close()
    else:       
       if mode == 'raw':
           print(results)
       elif mode == 'totals':
           totals = results['hits']['total']['value']# if 'totalHits' in results.keys() else results['estimatedTotalHits']
           print(totals)
       elif mode == 'facets':
           if format == 'json':
               print(json.dumps(results['aggregations'], indent=4))
           elif format == 'yaml':
               print(yaml.dump(results['aggregations'], default_flow_style=False))
       elif mode == 'results':
           outres = []
           for item in results['hits']['hits']:
               data = FlatDict(item['_source'], delimiter='.')
               record = []
               for h in headers.split(','):
                   try:
                       record.append(data[h])
                   except KeyError: 
                       record.append('')
               outres.append(record)
           print(tabulate(outres, headers=headers.split(','))) 



@index_app.command('get')
def index_get(entry_id, format:str='yaml', output:str=None, debug:bool=False, apikey:str=None):
    """Get single index record id"""
    cmd = DatenoCmd(debug, apikey)
    results = cmd.index_get(entry_id)
    if output is not None:
        f = open(output, 'w', encoding='utf8')
        f.write(json.dumps(results))
        f.close()
        print(f'Results saved to {output}')
    else:
       if format == 'json':
           print(json.dumps(results, indent=4))
       elif format == 'yaml':
           print(yaml.dump(results, default_flow_style=False))


@registry_app.command("get")
def registry_get(catalog_id, format:str='yaml', output:str=None, debug:bool=False, apikey:str=None):
    cmd = DatenoCmd(debug, apikey)
    results = cmd.registry_get(catalog_id)
    if output is not None:
        f = open(output, 'w', encoding='utf8')
        f.write(json.dumps(results))
        f.close()
        print(f'Results saved to {output}')
    else:
        if format == 'json':
            print(json.dumps(results, indent=4))
        elif format == 'yaml':
            print(yaml.dump(results, default_flow_style=False))


@registry_app.command('search')
def registry_search(query, filters:str="", headers:str='uid,name,link', output:str=None, debug:bool=False, apikey:str=None):
    """Searches for data catalogs"""
    cmd = DatenoCmd(debug, apikey)
    results = cmd.registry_search(query)
    if 'detail' in results.keys():
        print('Error: %s' % (results['detail']))
        return
    if output is not None:
        f = open(output, 'w', encoding='utf8')
        f.write(json.dumps(results))
        f.close()
        print(f'Results saved to {output}')
    else:       
       outres = []
       if not 'data' in results.keys():
           print('No results found')
           return
       for item in results['data']:
           data = FlatDict(item, delimiter='.')
           record = []               
           for h in headers.split(','):              
               record.append(data[h])
           outres.append(record)
       print(tabulate(outres, headers=headers.split(','))) 
#       print(results)

