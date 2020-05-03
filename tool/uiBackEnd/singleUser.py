import json
import requests
import sys
import numpy as np
import pandas as pd
import tkinter as tk
import sqlite3
from tkinter import messagebox
import matplotlib.pyplot as plt

from requests.auth import HTTPBasicAuth

def makeform(root):
    labs = []
    row = tk.Frame(root, width = 400)
    row.pack(side=tk.TOP,anchor='w',padx=30)
    tk.Label(row,text="Status").pack(side=tk.LEFT)

    row = tk.Frame(root, width = 400)
    row.pack(side=tk.TOP,anchor='w',padx=30)
    lab = tk.Label(row,text="Current Status")
    lab.pack(side=tk.LEFT)
    labs.append(lab)
    return labs

def singleUserAnalysis(username,password,privateR):

    root = tk.Tk()
    labs = makeform(root)
    lab = labs[0]
    root.update()

    choice = privateR
    auth = HTTPBasicAuth(username, password)
    r = requests.get('https://api.github.com/users/',auth = HTTPBasicAuth(username,password))
    print(r.status_code)
    if r.status_code==401:
        mess = "Incorrect Password"
        tk.messagebox.showwarning('Error',mess)
        return
    
    data = requests.get('https://api.github.com/users/' + username,auth = auth)
    data = data.json()

    lab["text"] = "Fetching User Details ..."
    root.update()

    print("Information about user {}:\n".format(username))
    print("Name: {}".format(data['name']))
    print("Email: {}".format(data['email']))
    print("Public repos: {}".format(data['public_repos']))
    if(choice == 0):
        print("Private repos: {}".format(data['total_private_repos']))
    print("About: {}".format(data['bio']))
    print("Followers: {}".format(data['followers']))
    print("Following: {}".format(data['following']))
    print("Site Admin: {}".format(data['site_admin']))
    print("Blog: {}".format(data['blog']))
    print("Public Gists: {}".format(data['public_gists']))
    if(choice == 0):
        print("Private Gists: {}".format(data['private_gists']))
    print("Company: {}".format(data['company']))
    print("Location: {}".format(data['location']))



    url = data['repos_url']
    print(url)

    if(choice == 0):
        url = 'https://api.github.com/user/repos'

    tmp_url = url

    page_no = 1

    repos_data = []
    repos_fetched = 0

    tmp = 0

    lab["text"] = "Fetching Repositories Data ... "
    root.update()

    while (True):
        response = requests.get(url, auth = auth)
        response = response.json()
        repos_data = repos_data + response
        repos_fetched += len(response)
        tmp = len(response)
        if (tmp == 30):
            page_no = page_no + 1
            url = tmp_url + '?page=' + str(page_no)
        else:
            break

    print("Total repositories fetched: {}".format(repos_fetched))


    repos_information = []

    cnt = 1

    print("All Repositories :")
    print("\n")

    for i, repo in enumerate(repos_data):
        data = []
        data.append(repo['id'])                                                        #0
        data.append(repo['name'])                                                      #1
        data.append(repo['description'])                                               #2
        
        temp_string = str(cnt) + ". " + repo['name']
        cnt += 1
        
        print(temp_string)
        
        data.append(repo['created_at'])                                                #3
        data.append(repo['updated_at'])                                                #4
        data.append(repo['owner']['login'])                                            #5
        data.append(repo['license']['name'] if repo['license'] != None else None)      #6
        data.append(repo['has_wiki'])                                                  #7
        data.append(repo['forks_count'])                                               #8
        data.append(repo['open_issues_count'])                                         #9
        data.append(repo['stargazers_count'])                                          #10
        data.append(repo['url'])                                                       #11
        data.append(repo['commits_url'].split("{")[0])                                 #12
        data.append(repo['languages_url'])                                             #13
        data.append(repo['contributors_url'])                                          #14
        
        repos_information.append(data)

    repos_df = pd.DataFrame(repos_information ,columns = ['Id', 'Name', 'Description', 'Created on', 'Updated on', 'Owner', 'License', 'Includes wiki', 'Forks count', 'Issues count', 'Stars count','Repo URL', 'Commits URL', 'Languages URL','Contributors URL'])

    language_count = []

    #Info About Languages

    for i in range(repos_df.shape[0]):
        lab["text"] = "Fetching Languages of Repository  "+str(i+1)
        root.update()
        response = requests.get(repos_df.loc[i, 'Languages URL'], auth = auth)
        response = response.json()
        print(i, response)
        language_count.append(json.dumps(response))
    #         language_count.append(response)
        if response != {}:
            languages = []
            for key, value in response.items():
                languages.append(key)
            languages = (u', '.join(languages)).encode('utf-8')
            repos_df.loc[i, 'Languages'] = (str(languages))[1:-1]
        else:
            repos_df.loc[i, 'Languages'] = ""


    print(repos_df)

    repos_df.to_csv(username + '_repos_info.csv', index = None)

    print('\n\n\n')
    print('Repowise Total Commits: ')
    print('\n')

    #Info About Commits
    temp = 0
    commits_information = []

    for i in range(repos_df.shape[0]):

        lab["text"] = "Fetching Commit Details of Repository " + str(i+1)
        root.update()

        url = repos_df.loc[i, 'Commits URL']
        page_no = 1

        name = repos_df.loc[i, 'Name']

        sum = 0

        while (True):

            response = requests.get(url, auth = auth)
            response = response.json()

            sum += len(response)

            for commit in response:
                commit_data = []
                commit_data.append(repos_df.loc[i, 'Id'])
                commit_data.append(commit['sha'])
                commit_data.append(commit['commit']['committer']['date'])
                commit_data.append(commit['commit']['message'])
                # if(temp == 0):
                #     print(commit)
                #     temp += 1
                commits_information.append(commit_data)
            if (len(response) == 30):
                page_no = page_no + 1
                url = repos_df.loc[i, 'Commits URL'] + '?page=' + str(page_no)
            else:
                break

        print("Repo Name: {} --> Number of commits: {}".format(name, sum))

    commits_df = pd.DataFrame(commits_information, columns = ['Repo Id', 'Commit Id', 'Date', 'Message'])
    commits_df.to_csv(username + '_commits_info.csv', index = False)


    languages = []
    count = []

    hm = dict()

    for i in range(len(language_count)):
        temp = language_count[i]
        temp = temp[2 : len(temp) - 2]
        
        if(len(temp) != 0):
            t1 = temp.split(",")
            
            for j in range(len(t1)):
                t2 = t1[j].split(": ")
                t2[0] = t2[0][:-1]
                
                if(j != 0):
                    t2[0] = t2[0][2:]
                    
    #             print(j,t2[0])
                
                if(t2[0] not in hm):
                    hm[t2[0]] = int(t2[1])
                else:
                    hm[t2[0]] += int(t2[1])
                
    labels = []
    sizes = []
    for key,value in hm.items():
        labels.append(key)
        sizes.append(value)
    
    patches, texts = plt.pie(sizes, shadow=True, startangle=90)
    plt.legend(patches,labels,loc="best")
    plt.axis('equal')
    plt.tight_layout()
    filepath = username+"-languages"
    plt.savefig(filepath)

    print('Languagewise Total Lines Of Data: ')
    print('\n')
    cnt = pd.DataFrame(hm.items(), columns = ['Language','Total Lines Of Data'])
    cnt = cnt.sort_values(by='Total Lines Of Data',ascending = False)
    print(cnt)


    session = requests.Session()
    session.auth = (auth.username,auth.password)

    complete_contributors_data = []

    filtered_contributors_data = []
    #0 - Login -> Username
    #1 - Contribution
    #2 - ID

    for i in range(len(repos_information)):

        lab["text"] = "Fetching Contributors of Repository " + str(i+1)
        root.update()

        url_contributors = repos_information[i][14] + '?page=1'
        page_no = 1

        print(url_contributors)
        
        curr_repo_id = repos_information[i][0]

        contributors_data = []

        all_filtered_contributors_data_for_one_repo = []

        # cc = 0
        while (True):
            # cc+=1
    #         print(cc+10)
            response = session.get(url_contributors)
            response = response.json()
            
            if(len(response) == 0):
                break

            contributors_data += response
            # print(page_no)
            # print('\n')

            for contributor in response:
                data = []
                data.append(contributor['login'])
                data.append(contributor['contributions'])
                data.append(curr_repo_id)
                print(data)
                all_filtered_contributors_data_for_one_repo.append(data)

            page_no += 1
            
            url_contributors = repos_information[i][14] + '?page=' + str(page_no)

        # print(len(contributors_data))

        complete_contributors_data.append(contributors_data)
        filtered_contributors_data.append(all_filtered_contributors_data_for_one_repo)



    for_csv = []
    for i in filtered_contributors_data:
        for j in i:
            for_csv.append(j)

            
    print('Repowise Per User Contribution: ')
    print('\n')
    filename = username + 'contributors.csv'
    contributor_repo_df = pd.DataFrame(for_csv, columns=['LoginId','Contributions','Id']) 
    contributor_repo_df.to_csv(filename)
    print(contributor_repo_df)

    con = sqlite3.connect('DB1.db')
    cur = con.cursor()

    df1 = contributor_repo_df
    df1.to_sql('Contributor' , con , if_exists = 'replace' , index = False)

    data = pd.read_sql_query("SELECT LoginId, Id, (Contributions * 100)/Total + 0.0 as '% Code Ownership' FROM Contributor NATURAL JOIN (SELECT Id, sum(Contributions) As Total FROM Contributor GROUP BY Id)",con)
    print('Repowise Code Ownership')
    print('\n')
    print(data)

    mess = "All data saved in the folder. Please check " + username + ".png to find prominent languages."
    tk.messagebox.showinfo("Finished !",mess)
    return