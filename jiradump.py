# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 14:24:24 2020

@author: DChanter

dumps jira issues and transistion data for user defined filter

the follows vars need to be defined 

server = 
usrn = 
key =
jirafilter =

"""


from jira import JIRA
import pandas as pd


server = 
usrn = 
key =
jirafilter = 
jira = jira = JIRA({'server':server}, basic_auth=(usrn, key))

#mapping states
#todo = 
#in_Progress = 
#done = 

#print(issue)

block_size = 100
block_num = 0
allissues = []
print("Exporting Issues!")
while True:
    start_idx = block_num*block_size
    issues = jira.search_issues(jirafilter,startAt = start_idx, maxResults = block_size, expand='changelog')

    if len(issues) == 0:
        # Retrieve issues until there are no more to come
        break
    block_num += 1
    for issue in issues:
        #log.info('%s: %s' % (issue.key, issue.fields.summary))
        allissues.append(issue)
print('Number of issues:', len(allissues))


issues = pd.DataFrame()

print('made it out')
for issue in allissues:
    changelog= issue.changelog
    for history in changelog.histories:
        for item in history.items:
           # print(item.field)
            if item.field == 'status' :
                d = {
                    'key': issue.key, 
                    'summary': issue.fields.summary,
                    'issuetype': issue.fields.issuetype.name,
                    'project' : issue.fields.project.name,
                    'status.name': issue.fields.status.name,
 #                   'status.category' : issue.fields.status.category.name,
                    'date': history.created,
                    #'field': item.field,
                    #'fieldtype' : item.fieldtype,
                    #'from': getattr(item, 'from'), # because using item.from doesn't wor
                    'fromString' : item.fromString,
                    #'to': item.to,
                    'toString': item.toString   
                    }
                issues = issues.append(d, ignore_index=True)


issues['date'] = pd.to_datetime(issues['date'],utc = True).dt.date

todo = ['Funnel','ToDo', 'To Do','Reopened', 'Blocked', 'Estimation', 
        'Ready to Work', 'Intake Funnel','Review for Prioritization','Profolio Backlog',
        'Reviewing','Analyzing','No Entry','Received','Investigation','Approved', 
        'Waiting for Approval','Ready for Work', 'Backlog', 'Hold', 'Analysis','Requirements']

inP = ['In Progress','System Testing', 'In QA','Ready for Demo','In PO Review',
       'Building','Build Breakdown', 'Ready for UAT', 'Design','Peer Review',
       'Committed to PI','Review','Implementing','Validation/UAT', 'Holding/ With Other Team',
       'Needs Classification', 'Legal Review 1', 'Integration Sheduled', 'Needs Estimate',
       'Vendor Risk Assessment','Legal Review 2','Needs Owner Approval', 'Ready for Prod', 
       'Holding: Internal Team', 'Holding: External Team/Vendor', 'Ready', 'Testing',
       'In Review','Requirements/Mapping','Mapping', 'Development', 'In Development',
       'UAT', 'Approved for Implementation','Ready for QA','In UAT']

done = ['Approved for Release','Resolved','Removed','Done','Cancelled', 'Complete',
        'Observing','Rejected', 'Ready for CAB', 'CAB Approval','Stage Deployment',
        'Prod Deployment', 'Maintenance','Closed']

if todo != None:
    issues = issues.replace(todo, 'TODO')
if inProgress != None:
    issues = issues.replace(inProgress, 'INPROGRESS')
if done !=None:
    issues = issues.replace(done, 'DONE')


issues_pivot=issues.pivot_table(index= ['key', 'project','status.name'] , columns='toString',values= 'date', aggfunc = 'min' )

issues_final = issues_pivot.reset_index()

if  (todo != None &  inProgress != None & done !=None):
    issues_final = issues_final.reindex(['key','TODO','INPROGRESS','DONE','project','status.name'],axis=1)

issues_final.to_csv("jiradump.csv")
