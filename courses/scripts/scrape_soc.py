# -*- coding: utf-8 -*-
import argparse
import json
import os
from progressbar import ProgressBar, Percentage, Bar, AdaptiveETA, Timer, Counter, FormatLabel
import requests
# Needed for using regular expressions.
import re

# Defines the address from which we fetch all the courses.
ONE_UF_API_ENDPOINT = 'https://one.uf.edu/apix/soc/schedule'


# Fetches courses from ONE.UF API endpoint, shows a handy progressbar if verbosity is true.
def fetch_courses(is_verbose=True):
    payload = {'category': 'RES', 'term': '20168', 'last-row':'0'}
    responses = list()
    total_rows = 0
    next_row = 0
    bar = ProgressBar(
            widgets=[
                FormatLabel('Rows: %(value)d/%(max_value)d '),
                Percentage(), 
                Bar(marker=u'■', left='[', right=']'), 
                ' ',
                Timer(), 
                ' ', 
                AdaptiveETA()
            ]
        )
    
    if is_verbose:
        print('Fetching courses from one.uf.edu!')
        bar.max_value = total_rows
        bar.update(0)

    while True:
        bar.max_value = total_rows
        if is_verbose:
            bar.update(next_row)
        payload['last-row'] = str(next_row)
        r = requests.get(ONE_UF_API_ENDPOINT, params=payload)
        responses.append(r.json()[0])
        total_rows = responses[-1]['TOTALROWS']
        next_row = responses[-1]['LASTROW']
        if (next_row is None) or (next_row > total_rows):            
            print('')
            break
    
    if is_verbose:
        print('Recieved course data from one.uf.edu!')
    courses_nested_list = [r['COURSES'] for r in responses]
    return [course for sublist in courses_nested_list for course in sublist]

# Fetches the course prerequistes and appends them to a new field in the .json file.
def fetch_prereqs():
    
    # Creates a list to hold our scraped courses. 
    scraped_course_list = []

    # Performs a regular expression search on the database file.
    with open('db.json') as database_json: 
    	for line in database_json:
    	    #Add that scraped course code data to a list. 
            scraped_course_list.append(re.search('[A-Z]{3}[0-9]{4}[A-Z]*', line))
       
    print (scraped_course_list)
    
    """
    4. For each element of the array, append that course code to a predefined endpoint string.
       (ex. https://one.uf.edu/apix/soc/cdesc/DDDCCCCL)

       DDD = Department 
       CCCC = Course Number
       L = Lab (optional)

    5. Query the API using that endpoint string.
    6. Retrieve the prerequisties and append it to a newly created "prereqs" field in db.json.
    6b. If there are no prerequisties, append 'NULL' to the newly created prereqs field in db.json.
    """

def write_db(course_list, kind='json', path='.', separator=','):
    """
    Writes the JSON array to a database.
    """
    script_dir = os.path.dirname(__file__)
    
    # Name the output file is called changed temporarily for testing.
    out_path = os.path.join('db.' + script_dir + kind)
    with open(out_path, 'w+') as outfile:
        json.dump(course_list, outfile, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Fetches course data from https://one.uf.edu/!'
    )
    parser.add_argument(
        '-q', dest='quiet', 
        help='Disable all output', 
        action='store_true'
    )
    
    parser.set_defaults(quiet=False)
    
    opts = parser.parse_args()
    is_verbose = not opts.quiet
    course_list = fetch_courses(is_verbose)

    # Path the db is written to has changed temporarily for testing.
    write_db(course_list, kind='json', path='../')

    # Call fetch_prereqs() to test it out. Overwhelms the console currently, be careful!
    fetch_prereqs()