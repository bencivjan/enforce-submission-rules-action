# DevOps Course Automatic Rule Verification

Ben Civjan and Brad Palagi

This repository demonstrates and includes all the pieces necessary to verify four rules for the KTH DevOps course.

These include:
1. Ensuring that students are not partners with the same person for more than two projects
2. Ensuring that students are not working alone for more than two projects
3. Ensuring that a student is not choosing the same topic (ex. Testing & CI, Containers & Serverless, etc.) for two different tasks
    - currently only presentations and demos have directories for sorting tasks so they are the only ones being checked in this way
4. Ensuring that a student can not choose the same task (ex. presentation, essay, etc.) more than once

## How to use:

1. Add the github workflow file included in this directory. The main aspect of this yaml file is: on pull request to run 

``` pip install PyGithub ``` and <br /> 
``` python check_rules.py ${{ secrets.GITHUB_TOKEN }} ${{ github.event.pull_request.number }} ${{github.repository}} ```
 
2. Include the ```check_rules.py``` file in your repository 

3. Once these two files are added, assuming you have the properly structured ``` contributions ``` directory, each Pull Request to modify the contributions directory will have these verifications ran automatically

 ## Inputs:

These three inputs allow for the program to navigate the current repository using PyGithub
 1. ${{ secrets.GITHUB_TOKEN }} 
 2. ${{ github.event.pull_request.number }} 
 3. ${{github.repository}}

## Tests:

We've included a ``` contributions ``` directory with the same structure as the KTH/DevOps contributions directory.

This copied structure was then used to perform tests for each of our four new verification steps.

1. When a student already has two files in the contributions directory of assignment proposals by themselves the Github action will fail
2. When two students already have two files in the contributions directory of assignment proposals with each other the Github action will fail
    - Also, tests were performed for the case of a three student group to verify no combination of those students have worked together twice before
3. When any student attempts to propose a demo for the same topic as a presentation they've already proposed or vice versa the Github action will fail 
4. When a student has already proposed an assignemnt of a certain type, when they submit another proposal for the same type of assignment the Github action will fail



# Further Comments:

1. We need a standard method of accepting final submissions. We have found that even for final submissions, it seems there is a previous course-automation or Github Action which is requiring the "Assignment Proposal" template to be followed for all pull requests. For our implementation to work as planned we would need a possibility of a different template for "Final Submission." This will allow us to run our verifications on only the proposals which is when we would like to check these rules are followed.

2. After looking through some past "Final Submissions" theres a few fields we would recommend on this template:
- Title
- Members
- Link to Proposal
- Submission Links to Slides, Repository, Katacoda etc.
- Description 
- Grading Criteria Intended to Meet 
