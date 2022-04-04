import requests
from requests.auth import HTTPBasicAuth
import pandas as pd


rapidViewId = 157
sprintId = 804
jiraUrl = "" # replace your jira url


row = []

# fetch data from jira
def fecth_data(jiraUrl,rapidViewId,sprintId):

    headers = { "Accept": "application/json"}
    
    url = f"{jiraUrl}/rest/greenhopper/latest/rapid/charts/sprintreport?rapidViewId={rapidViewId}&sprintId={sprintId}"

    email = "" # replace your email

    api_key = "" # replace your API key

    auth = HTTPBasicAuth(email, api_key)

    response = requests.request(
        "GET",
        url=url,
        headers=headers,
        auth=auth
    )


    return response.json()

# add data in dataframe
def add_dataFrame():

    data = fecth_data(jiraUrl,rapidViewId,sprintId)

    completedIssues = data["contents"]["completedIssues"]

    for data in completedIssues:
        issueType = data['typeName']
        storyPoint = data.get('currentEstimateStatistic',{}).get('statFieldValue',{}).get('value')
        
        row.append((issueType,storyPoint))

# write dataframe in csv
def write_csv():
    
    fileName = f"completed_issues_{sprintId}.csv"

    result = pd.DataFrame(row, columns=['IssueType','StoryPointsSpent'])
    total = result['StoryPointsSpent'].sum()
    totalStoryPoint = result.groupby(['IssueType']).sum()
    totalStoryPoint['StoryPointsSpentAsPercentage'] = (totalStoryPoint['StoryPointsSpent']/total)*100
    totalStoryPoint.to_csv(fileName)
    



def main():
    add_dataFrame()
    write_csv()
    



if __name__=="__main__":
    main()


