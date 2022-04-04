from ctypes import sizeof
import sys
from github import Github


# No student works alone more than twice
def soloCheck(name, repo):
    num_times_alone = 0

    # contents should contain all folders contained in /contributions
    contents = repo.get_contents("contributions/course-automation")
    contents += repo.get_contents("contributions/essay")
    contents += repo.get_contents("contributions/executable-tutorial")
    contents += repo.get_contents("contributions/feedback")
    contents += repo.get_contents("contributions/open-source")

    # check folders containing this students name
    for word in contents:
        word = str(word)[len("ContentFile(path=\"contributions/"):len(str(word))].split("/")
        if name in word[1]:
            # determine if this was also a solo project
            names = word[1].split("-")
            if len(names) == 1:
                num_times_alone+=1

    contents = repo.get_contents("contributions/presentation/week2-testing-and-CI")
    contents += repo.get_contents("contributions/presentation/week3-CD-and-feature-flag")
    contents += repo.get_contents("contributions/presentation/week4-containers-and-serverless")
    contents += repo.get_contents("contributions/presentation/week5-Infrastructure-as-Code")
    contents += repo.get_contents("contributions/presentation/week6-software-bots")
    contents += repo.get_contents("contributions/presentation/week7-dependency-DevSecOps")
    contents += repo.get_contents("contributions/presentation/week8-culture-and-legal")
    contents += repo.get_contents("contributions/presentation/week9-other")

    for word in contents:
        word = str(word)[len("ContentFile(path=\"contributions/presentation/"):len(str(word))].split("/")
        if name in word[1]:
            # determine if this was also a solo project
            names = word[1].split("-")
            if len(names) == 1:
                num_times_alone+=1

    contents = repo.get_contents("contributions/demo/week2-testing-and-CI")
    contents += repo.get_contents("contributions/demo/week3-CD-and-feature-flag")
    contents += repo.get_contents("contributions/demo/week4-containers-and-serverless")
    contents += repo.get_contents("contributions/demo/week5-Infrastructure-as-Code")
    contents += repo.get_contents("contributions/demo/week6-software-bots")
    contents += repo.get_contents("contributions/demo/week7-dependency-DevSecOps")
    contents += repo.get_contents("contributions/demo/week8-culture-and-legal")
    contents += repo.get_contents("contributions/demo/week9-other")

    for word in contents:
        word = str(word)[len("ContentFile(path=\"contributions/demo/"):len(str(word))].split("/")
        if name in word[1]:
            # determine if this was also a solo project
            names = word[1].split("-")
            if len(names) == 1:
                num_times_alone+=1

    print("Number of times ", name, "worked alone: ", num_times_alone)


    if num_times_alone >=2:
        print ("Student may not work alone again")
    else:
        print ("Student okay to work alone")


# No two students work together more than twice
def partnerCheck(students, repo):
    num_times_together = 0

    # contents should contain all folders contained in /contributions
    contents = repo.get_contents("contributions/course-automation")
    contents += repo.get_contents("contributions/essay")
    contents += repo.get_contents("contributions/executable-tutorial")
    contents += repo.get_contents("contributions/feedback")
    contents += repo.get_contents("contributions/open-source")

    # check folders containing this students name
    for word in contents:
        word = str(word)[len("ContentFile(path=\"contributions/"):len(str(word))].split("/")
        if students[0] in word[1] and students[1] in word[1]:
            num_times_together+=1

    contents = repo.get_contents("contributions/presentation/week2-testing-and-CI")
    contents += repo.get_contents("contributions/presentation/week3-CD-and-feature-flag")
    contents += repo.get_contents("contributions/presentation/week4-containers-and-serverless")
    contents += repo.get_contents("contributions/presentation/week5-Infrastructure-as-Code")
    contents += repo.get_contents("contributions/presentation/week6-software-bots")
    contents += repo.get_contents("contributions/presentation/week7-dependency-DevSecOps")
    contents += repo.get_contents("contributions/presentation/week8-culture-and-legal")
    contents += repo.get_contents("contributions/presentation/week9-other")

    for word in contents:
        word = str(word)[len("ContentFile(path=\"contributions/presentation/"):len(str(word))].split("/")
        if students[0] in word[1] and students[1] in word[1]:
            num_times_together+=1

    contents = repo.get_contents("contributions/demo/week2-testing-and-CI")
    contents += repo.get_contents("contributions/demo/week3-CD-and-feature-flag")
    contents += repo.get_contents("contributions/demo/week4-containers-and-serverless")
    contents += repo.get_contents("contributions/demo/week5-Infrastructure-as-Code")
    contents += repo.get_contents("contributions/demo/week6-software-bots")
    contents += repo.get_contents("contributions/demo/week7-dependency-DevSecOps")
    contents += repo.get_contents("contributions/demo/week8-culture-and-legal")
    contents += repo.get_contents("contributions/demo/week9-other")

    for word in contents:
        word = str(word)[len("ContentFile(path=\"contributions/demo/"):len(str(word))].split("/")
        if students[0] in word[1] and students[1] in word[1]:
            num_times_together+=1


    print("Number of times ", students, "worked together: ", num_times_together)

    if num_times_together >=2:
        print ("Students may not work together again")
    else:
        print ("Student okay to work together")



def main():

    f = open('token.txt','r')
    github = Github(f.readline())
    f.close()
    # github = Github(sys.argv[1])

    repo = github.get_repo('KTH/devops-course', lazy=False)

    pr_num = 1650
    # pr_num = 1605
    # pr_num = sys.argv[2]

    pr = repo.get_pull(pr_num)
    words = pr.body.split()
    students = []

    for word in words:
        if '@kth.se' in word:
            students.append(word.split('(')[1].split('@')[0])

    if len(students) == 1:
        soloCheck(students[0],repo)
    elif len(students) == 2:
        partnerCheck(students,repo)
    else:
        print('Issue with number of students on the PR')


if __name__ == "__main__":
    main()



# '''
# We will create a script to enforce the submission rules of the course.

# These include:
# 1. Ensuring that students are not partners with the same person for more than two projects
# 2. Ensuring that students are not working alone for more than two projects
# 3. Ensuring that a student is not choosing the same topic (ex. Testing & CI, Containers & Serverless, etc.) for two different tasks
# 4. Making sure that a student has not done more a task (ex. presentation, essay, etc.) more than once
# '''

# import sys
# import re

# def find_students(students: list, text: str):
#     words = text.split()
#     for word in words:
#         if '@kth.se' in word:
#             name = ''
#             for char in word.split('@')[0]:
#                 if char.isalpha():
#                     name += char
#             students.append(name)
#     return students


# def check_partners():

#     return True

# # print(sys.argv[1])

# example_body = '''
# # Assignment Proposal

# ## Title

# DevOps in healthcare technology

# ## Names and KTH ID

#     print (sys.argv[2].number)

# ## Deadline

# Task 1 (April 5)

# ## Category

# Week 3: Continuous Deployment / Delivery and Feature flags (April 5)

# ## Description

# The manufacture of medical devices is a strictly regulated domain in the European Union. Medical Devices traditionally follow the Waterfall methodology of development, where design is predefined, testing is often manual and updates can take months to roll out due to a bloated architecture. This is where DevOps solves these problems by making the architecture leaner and allowing for teams to make changes faster and more efficiently. It allows teams to be able to meet changing market needs and factor in feedback. 

# We want to give a presentation on how the healthcare industry can (and has) implemented a DevOps methodology to improve software quality. We will discuss DevOps generally but focus on CI/CD pipelines for healthcare software. 
# '''

# students = []
# print(find_students(students, example_body))