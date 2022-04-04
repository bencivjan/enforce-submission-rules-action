'''
We will create a script to enforce the submission rules of the course.

These include:
1. Ensuring that students are not partners with the same person for more than two projects
2. Ensuring that students are not working alone for more than two projects
3. Making sure that a student has not done more a task (ex. presentation, essay, etc.) more than once
4. Ensuring that a student is not choosing the same topic (ex. Testing & CI, Containers & Serverless, etc.) for two different tasks
'''

import sys
import re
from github import Github

def find_students(students: list, text: str):
    words = text.split()
    for word in words:
        if '@kth.se' in word:
            name = ''
            for char in word.split('@')[0]:
                if char.isalpha():
                    name += char
            students.append(name)
    return students


def check_task_limit(students: list, repo, pr):
    commits = pr.get_commits()

    # There could be multiple commits
    # TEST WITH MULTIPLE COMMITS
    files_changed = []

    # Take last commit
    if commits.totalCount >= 1:
        files_changed = commits[commits.totalCount - 1]
    else:
        files_changed = commits[0]

    tasks_submitted = []
    for file in files_changed.files:
        path = file.filename.split('/')
        if path[0] == 'contributions':
            tasks_submitted.append(file.filename)

    # since we need the path index of the groups, we need to know which tasks have subfolders that
    # organize group submissions by topic
    tasks_organized_by_date = ['presentation', 'demo']

    for task_filename in tasks_submitted:
        task_submitted = task_filename.split('/')[1]
        topic_submitted = task_filename.split('/')[2]

        groupNamePathIndex = 2 if task_submitted not in tasks_organized_by_date else 3
        # Go to task directory to see if they have already done this task
        previous_groups = repo.get_contents(f'contributions/{task_submitted}')
        if groupNamePathIndex == 3:
            previous_groups = repo.get_contents(f'contributions/{task_submitted}/{topic_submitted}')

        for group in filter(lambda g : g.type == 'dir', previous_groups):            
            group_names = group.path.split('/')[groupNamePathIndex].split('-')
            for student in students:
                if student in group_names:
                    raise RuntimeError(f'Student {student} has already completed task {task_submitted}')
        # if task_list.type == 'dir':
        #     print(task_list.path)
    return True


def check_topic_limit(students: list, repo, pr):
    commits = pr.get_commits()
    
    # There could be multiple commits
    # TEST WITH MULTIPLE COMMITS
    files_changed = []

    # Take last commit
    if commits.totalCount >= 1:
        files_changed = commits[commits.totalCount - 1]
    else:
        files_changed = commits[0]
    
    valid_tasks = ['presentation', 'demo'] # For now only presentations and demos are ordered by topic date
    tasks_submitted = []
    topics_submitted = []
    for file in files_changed.files:
        path = file.filename.split('/')
        if path[0] == 'contributions' and path[1] in valid_tasks:
            tasks_submitted.append(path[1])
            topics_submitted.append(path[2])


    # for each student
    #   for each valid task, check the(each) topic for the student's name
    #       if already exists, throw error
    
    for student in students:
        for valid_task in valid_tasks:
            for topic_submitted in topics_submitted:
                previous_groups = repo.get_contents(f'contributions/{valid_task}/{topic_submitted}')
                for group in filter(lambda g : g.type == 'dir', previous_groups):
                    if student in group.path.split('/')[3].split('-'):
                        raise RuntimeError(f'Student {student} has already completed task {valid_task} for topic {topic_submitted}')
    
    return True


example_body = '''
# Assignment Proposal

## Title

DevOps in healthcare technology

## Names and KTH ID

- Lucas Eren (leren@kth.se)
- Sanherib Elia (sanherib@kth.se)

## Deadline

Task 1 (April 5)

## Category

Week 3: Continuous Deployment / Delivery and Feature flags (April 5)

## Description

The manufacture of medical devices is a strictly regulated domain in the European Union. Medical Devices traditionally follow the Waterfall methodology of development, where design is predefined, testing is often manual and updates can take months to roll out due to a bloated architecture. This is where DevOps solves these problems by making the architecture leaner and allowing for teams to make changes faster and more efficiently. It allows teams to be able to meet changing market needs and factor in feedback. 

We want to give a presentation on how the healthcare industry can (and has) implemented a DevOps methodology to improve software quality. We will discuss DevOps generally but focus on CI/CD pipelines for healthcare software. 
'''

def main():
    f = open('token')
    github = Github(f.readline())
    f.close()

    repo = github.get_repo('KTH/devops-course', lazy=False)
    students = []

    pr = repo.get_pull(1650) # sys.argv[2] hardcode for now

    demo_pr = repo.get_pull(1614)
    find_students(students, pr.body)
    # check_topic_limit(students, repo, demo_pr)
    check_task_limit(students, repo, pr)

    # print(find_students(students, example_body))
    # check_task_limit(students, repo, pr)

    # for i in check_task_limit(students, repo, pr):
    #     print(i)

main()