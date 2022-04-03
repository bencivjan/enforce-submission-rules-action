import sys
import json
import re
from github import Github

def process_json(payload):
    python_obj = json.loads(payload)
    # fetch main branch and pull request number
    repo_main = python_obj['pull_request']['base']['repo']['full_name']
    pull_request_number = python_obj['pull_request']['number']

    return repo_main, pull_request_number
    
# Split added and changed files
def process_added_files(files):
    file_parts = []
    for f in files:
        file_parts.append(f.split('/'))
    return file_parts

"""
Check PR to see if it is a course contribution with a path "/contributions/ .." 
and that PR is for a valid task e.g. demo, essay etc. 
Lastly, the number of students contributed to the PR is extracted.  
"""
def check_student_pr(files):
    valid = True
    valid_files = []
    task = ""
    num_students = -1
    for f in files:
        if len(f) < 4:
            valid = False
        else:
            if f[0] != 'contributions':
                valid = False
            else:
                task = f[1]
            if not 1 <= len(f[2].split('-')) <= 3:
                valid = False
            else:
                student_names = f[2].split('-')
                num_students = len(student_names)
        valid_files.append(valid)
        valid = True
    return valid_files, task, student_names,num_students

""" 
Process the expected input from command line:
- Guthub token
- Payload from pull request
- List of filepaths for files added 
- List of filepaths for files changed
"""
def main():

    print('First off, hello world.')

    github_token = sys.argv[1]
    payload = sys.argv[2]
    files_added = re.sub('[\\\"\[\]]+', '', sys.argv[3]).split(',')
    files_changed = re.sub('[\\\"\[\]]+', '', sys.argv[4]).split(',')

    file_added_parts = process_added_files(files_added)
    file_changed_parts = process_added_files(files_changed)

    # append added files and changed files into one list.
    files_parts = file_added_parts
    for f in file_changed_parts:
        files_parts.append(f)

    repo_main, pull_request_number = process_json(payload)

    valid_files, task, student_names, num_students = check_student_pr(files_parts)

    # If none of the added or changed files is a valid student submission, return nothing
    if True not in valid_files:
        return
        
        
    print(json.dumps({   
        "The students": student_names, 
        "Their task" : task,
        "The number of students": num_students
        }))


if __name__ == "__main__":
    main()