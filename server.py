
from flask import Flask
from flask import render_template
from flask import request
from collections import defaultdict
#from random import randint
from others import Trie
import sys
import re
# import json
# import urllib

#Using Trie


app = Flask(__name__)

@app.route("/")
def search_home():
    data, code_for_names = loaddata("data.csv")
    query = request.args.get("query_string")
    if not query or len(str(query)) < 3:
        results=["Please Enter a query of len greater than 3"]
    else:
        results=allsearches(data, query, code_for_names)
    return render_template("server.html",results=results)

code_for_names = defaultdict(str)

def loaddata(file):
    data = {}
    data['fn'] = Trie('')
    data['mn'] = Trie('')
    data['ln'] = Trie('')
    alldata = [data['fn'],data['mn'],data['ln']]
    with open(file) as f:
        lines = f.readlines()

    try:
        for l, name in enumerate(lines[1:]):
            name  = name.lower()
            #code_for_names[hash(name)] = name
            namelist = name.split(',')
            for i,n in enumerate(namelist):
                if n.strip():
                    alldata[i].append(n.strip())
    except:
        # print("Unexpected error:", sys.exc_info()[0])
        # print(namelist)
        pass

    return data, lines

def allsearches(data, query, lines):
    first_names = list(data['fn'].autocomplete(query))
    middle_names = list(data['mn'].autocomplete(query))
    last_names = list(data['ln'].autocomplete(query))

    matches = set(first_names+middle_names+last_names)
    results = set()
    for word in matches:
        regex = re.compile(str(word), re.IGNORECASE)
        iterator = filter(regex.search, lines)
        for mat in iterator:
            results.add(' '.join(filter(None, [x.strip() for x in mat.split(',')])))
    return list(results)
