import sys
from github import Github


def main():

    print (sys.argv[2].number)

    github = Github(sys.argv[1])
    repo = github.get_repo('KTH/devops-course', lazy=False)

    pr = repo.get_pull(1650)

    print(pr.body)

    # num_students = 0

    # words = pr.body.split()

    # for word in words:
    #     if '@kth.se' in word:
    #         num_students+=1

    # print ('Num students: ', num_students)

if __name__ == "__main__":
    main()