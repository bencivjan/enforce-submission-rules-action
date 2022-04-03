'''
We will create a script to enforce the submission rules of the course.

These include:
1. Ensuring that students are not partners with the same person for more than two projects
2. Ensuring that students are not working alone for more than two projects
3. Ensuring that a student is not choosing the same topic (ex. Testing & CI, Containers & Serverless, etc.) for two different tasks
4. Making sure that a student has not done more a task (ex. presentation, essay, etc.) more than once
'''

import sys
import re

students = []

def find_students(text: str):
    words = text.split()
    for word in words:
        if '@kth.se' in word:
            name = ''
            for char in word.split('@')[0]:
                if char.isalpha():
                    name += char
            students.append(name)


def check_partners():

    return True

# print(sys.argv[1])

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

find_students(example_body)
print(students)
