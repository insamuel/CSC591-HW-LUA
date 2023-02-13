import os
import re

from Row import Row
from Cols import Cols
from Data import Data

def parse_row(line: str):
    split_line = line.split(',')
    
    headers = []
    cells = []

    for item in split_line:
        if len(item) == 0:
            continue
        
        item_stripped = item.strip()
        is_number = item_stripped.isdigit()
        if not is_number:
            for match in re.findall('\'(.*?)\'', item):
                headers.append(match.replace('\'', ''))
        else:
            cells.append(item_stripped)

    cells.append(':'.join(headers))
    return cells
    
def process_repgrid_file(src: str):

    #try to catch relative paths
    if not os.path.isfile(src):
        src = os.path.join(os.path.dirname(__file__), src)

    src = os.path.abspath(src)

    repgrid_contents = []
    with open(src, 'r') as repgrid_file:
        repgrid_contents = repgrid_file.readlines()

    rows = []
    names = []

    col_query = "( )*\t*cols( )*\t*=( )*\t*{"
    row_query = "( )*\t*rows( )*\t*=( )*\t*{"

    row_len = 0
    
    current_line = repgrid_contents.pop(0).strip()
    while not re.search(col_query, current_line): #for now, let's just skip to the cols section
        current_line = repgrid_contents.pop(0).strip()

    # parse the cols section
    # keep trying to read and parse until we reach the rows section
    while not re.search(row_query, current_line):
        row = parse_row(current_line.strip())
        rows.append(row)
        row_len = max(row_len, len(row))
        if len(repgrid_contents) > 0:
            current_line = repgrid_contents.pop(0).strip()

    #read the rows
    current_line = re.split(row_query, current_line)[-1]
    names = [""] * row_len

    #keep reading until we read the end
    while re.search("( )*\t*[{].*[}]", current_line):
        index = current_line.count('_')
        split = current_line.split('}')[0].split(',')
        value = split[-1]
        names[index] = value.strip().replace('\'', '').replace('{', '')
        if len(repgrid_contents) > 0:
            current_line = repgrid_contents.pop(0).strip()
        else:
            break
    
    names[-1] = "thingX" # end this off with an X so it gets skipped in calculations
    generated_data = Data(names)

    for row in rows:
        generated_data.add(row)
    return generated_data
                


        

    
