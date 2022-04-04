'''
We will create a script to enforce the submission rules of the course.

These include:
1. Ensuring that students are not partners with the same person for more than two projects
2. Ensuring that students are not working alone for more than two projects
3. Ensuring that a student is not choosing the same topic (ex. Testing & CI, Containers & Serverless, etc.) for two different tasks
4. Making sure that a student has not done more a task (ex. presentation, essay, etc.) more than once
'''

from ctypes import sizeof
import sys
from github import Github
import re


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

    # if it equals two, need to make sure this current pr is just modifying a proposal.
    if (current pr is adding files):
        if num_times_alone > 1:
            raise RuntimeError("Student may not work alone again")

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

    if (current pr is adding files):
        if num_times_together > 1:
             raise RuntimeError("Students may not work together again")



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
    for file in filter(lambda f : f.status == 'added', files_changed.files):
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
    for file in filter(lambda f : f.status == 'added', files_changed.files):
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


def main():

#     # Local Testing
#     f = open('token.txt','r')
#     github = Github(f.readline())
#     f.close()

#     repo = github.get_repo('KTH/devops-course', lazy=False)
    
    # pr_num = 1606   # worked alone once
    # pr_num = 1605   # worked alone twice
    # pr_num = 1582   # worked together once
    # pr_num = 1650   # worked together twice
    # pr_num = 1614 # Preson's demo pull request

    # pr = repo.get_pull(pr_num)
    # students = []
    # find_students(students, pr.body)
    # check_topic_limit(students, repo, pr)
    # check_task_limit(students, repo, pr)

    # Production
    github = Github(sys.argv[1])
    repo = github.get_repo(sys.argv[3], lazy=False)
    pr = repo.get_pull(int(sys.argv[2]))
    students = []

    find_students(students, pr.body)

    if len(students) == 1:
        soloCheck(students[0],repo)
    elif len(students) == 2:
        partnerCheck(students,repo)
    elif len(students) == 3:
        two = []
        two.append(students[0])
        two.append(students[1])
        partnerCheck(two,repo)
        two = []
        two.append(students[0])
        two.append(students[2])
        partnerCheck(two,repo)
        two = []
        two.append(students[1])
        two.append(students[2])
        partnerCheck(two,repo)
    else:
        raise RuntimeError("Issue with number of students on the PR")

    check_topic_limit(students, repo, pr)
    check_task_limit(students, repo, pr)


if __name__ == "__main__":
    main()
