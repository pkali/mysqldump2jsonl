#!/usr/bin/env python3

import sys
import gzip
import ast
import json

class Dumper:
    def __init__(self, path):
        self.path = path
        self.open_file = {}

    def close_all(self)
        #close previous file(s)
        for name in self.open_file:
            self.open_file[name].close()
        self.open_file = {}

    def dump(self, filename, data):
        if filename not in self.open_file:
            close_all()
            f = gzip.open(self.path+filename+'.jsonl.gz', 'wt')
            self.open_file[filename] = f
        else:
            f = self.open_file[filename]
        f.write(data+'\n')

    def readlineq(self, f):
        # Read line and quit if no more data
        line = f.readline()
        if line == '':
            close_all()
            sys.exit(0)
        else:
            return line

dp = Dumper(sys.argv[2])

def get_value_tuples(line):
    values = line.partition(' VALUES ')[-1].strip().replace('NULL', 'None')
    if values[-1] == ';':
        values = values[:-1]

    return ast.literal_eval(values)

def generate_json_line(columns, data, noiter=False):
    jl = {}
    if noiter:
        jl[columns[0]] = data
    else:
        for i in range(len(columns)):
            jl[columns[i]] = data[i]
    return json.dumps(jl, ensure_ascii=False)

with gzip.open(sys.argv[1], 'rt') as f:
    # look for the beginning of the table definition
    while True:
        while True:
            line = dp.readlineq(f)
            if line.startswith('CREATE TABLE'): break  #untill

        table = line.split('`')[1] # name of the table

        # get names and types of columns
        columns = []
        while True:
            line = dp.readlineq(f)
            if line.startswith('  `'):
                columns.append(line.split('`')[1]) # = line.split('`')[2].split(' ')[1]
            else: break

        # look for the beginning of the data
        while True:
            line = dp.readlineq(f)
            if line.startswith('INSERT INTO'): break
        while line.startswith('INSERT INTO'):
            if line.split('`')[1] == table: # check if the INSERT is for the correct table
                data = get_value_tuples(line)
                if isinstance(data, str) or isinstance(data, int) or isinstance(data, float):
                    dp.dump(table, generate_json_line(columns, data, noiter=True))
                else:
                    for i in data:
                        dp.dump(table, generate_json_line(columns, i))
            line = dp.readlineq(f)
