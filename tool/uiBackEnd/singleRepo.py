import json
import requests
from tkinter.ttk import *
import sys
import numpy as np
import pandas as pd
import tkinter as tk
from requests.auth import HTTPBasicAuth
from tkinter import messagebox
import matplotlib.pyplot as plt

repos_information = []

def choiceOfRepo(value,auth,root):
    choice = int(value.get())
    if choice == -1:
        tk.messagebox.showinfo("Error","Please select a repository")
        return
    print(choice)
    print(auth)
    repos_df = pd.DataFrame(repos_information ,columns = ['Id', 'Name', 'Description', 'Created on', 'Updated on', 'Owner', 'License', 'Includes wiki', 'Forks count', 'Issues count', 'Stars count','Repo URL', 'Commits URL', 'Languages URL','Contributors URL'])

    np_repos_df = repos_df.to_numpy()

    info_file_array = []
    temp_arr = ["Id",repos_information[choice][0],"",""]
    info_file_array.append(temp_arr)
    temp_arr = ["Name",repos_information[choice][1],"",""]
    info_file_array.append(temp_arr)
    temp_arr = ["Description",repos_information[choice][2],"",""]
    info_file_array.append(temp_arr)
    temp_arr = ["Created on",repos_information[choice][3],"",""]
    info_file_array.append(temp_arr)
    temp_arr = ["Updated on",repos_information[choice][4],"",""]
    info_file_array.append(temp_arr)
    temp_arr = ["Owner",repos_information[choice][5],"",""]
    info_file_array.append(temp_arr)
    temp_arr = ["License",repos_information[choice][6],"",""]
    info_file_array.append(temp_arr)
    temp_arr = ["Includes Wiki",repos_information[choice][7],"",""]
    info_file_array.append(temp_arr)
    temp_arr = ["Forks count",repos_information[choice][8],"",""]
    info_file_array.append(temp_arr)
    temp_arr = ["Issues count",repos_information[choice][9],"",""]
    info_file_array.append(temp_arr)
    temp_arr = ["Stars count",repos_information[choice][10],"",""]
    info_file_array.append(temp_arr)
    temp_arr = ["URL",repos_information[choice][11],"",""]
    info_file_array.append(temp_arr)
    temp_arr = ["Contributors URL",repos_information[choice][14],"",""]
    info_file_array.append(temp_arr)

    #Info About Languages

    response = requests.get(repos_df.loc[choice, 'Languages URL'], auth = auth)
    response = response.json()

    print(choice, response)

    if response != {}:
        languages = []
        for key, value in response.items():
            languages.append(key)
        languages = (u', '.join(languages)).encode('utf-8')
        repos_df.loc[choice, 'Languages'] = languages
    else:
        repos_df.loc[choice, 'Languages'] = ""
    temp_arr = ["Languages",(str(languages))[1:-1],"",""]
    info_file_array.append(temp_arr)

    print(info_file_array)

    # print(repos_df)
    filepath = repos_information[choice][1]
    ddf = pd.DataFrame(info_file_array)
    ddf.to_csv(filepath+'-info.csv', index = None)

    #Info About Commits
    temp_arr = ["","","",""]
    info_file_array.append(temp_arr)
    temp_arr = ["","","",""]
    info_file_array.append(temp_arr)
    temp_arr = ["Id","SHA","Date","Commit Message"]
    info_file_array.append(temp_arr)


    commits_information = []

    url = repos_df.loc[choice, 'Commits URL']
    page_no = 1

    while (True):
        response = requests.get(url, auth = auth)
        response = response.json()

        print("URL: {}, commits: {}".format(url, len(response)))

        for commit in response:
            commit_data = []
            commit_data.append(repos_df.loc[choice, 'Id'])
            commit_data.append(commit['sha'])
            commit_data.append(commit['commit']['committer']['date'])
            commit_data.append(commit['commit']['message'])

            info_file_array.append(commit_data)

            commits_information.append(commit_data)
        if (len(response) == 30):
            page_no = page_no + 1
            url = repos_df.loc[choice, 'Commits URL'] + '?page=' + str(page_no)
        else:
            break

    filepath = repos_information[choice][1]
    commits_df = pd.DataFrame(commits_information, columns = ['Repo Id', 'Commit Id', 'Date', 'Message'])
    commits_df.to_csv(filepath+'-commits.csv', index = False)
    # print(commits_df)

    df = pd.DataFrame(info_file_array)
    filepath = repos_information[choice][1] + '.csv'
    df.to_csv(filepath,index=False)
    
    url = repos_df.loc[choice, 'Contributors URL'] + '?page=1'
    page_no = 1
    total = 0 

    all_contributor_data = []

    while(True):
        response = requests.get(url,auth=auth)
        response = response.json()

        print(response)

        if len(response)==0:
            break


        for contributor in response:
            data = []
            data.append(contributor['login'])
            data.append(contributor['contributions'])
            total += contributor['contributions'] 
            all_contributor_data.append(data)

        page_no += 1
        url = repos_df.loc[choice, 'Contributors URL'] + '?page=' + str(page_no)

    labels = []
    sizes = []
    for x in all_contributor_data:
        labels.append(x[0])
        sizes.append(x[1])
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes,labels=labels,autopct='%1.1f%%',shadow=True, startangle=90)
    ax1.axis('equal')
    filepath = repos_information[choice][1]
    plt.savefig(filepath)

    mess = "All data saved in the folder. Please check " + repos_df.loc[choice, 'Name'] + ".png to find contributors."
    tk.messagebox.showinfo("Finished !",mess)
    root.destroy()
    return

def singleRepoAnalysis(username,password,privateR):

    choice = privateR

    auth = HTTPBasicAuth(username,password)
    r = requests.get('https://api.github.com/users/',auth = HTTPBasicAuth(username,password))
    print(r.status_code)
    if r.status_code==401:
        mess = "Incorrect Password"
        tk.messagebox.showwarning('Error',mess)
        return
                 
    data = requests.get('https://api.github.com/users/' + username,auth = auth)
    data = data.json()

    if choice == 0:
        url = 'https://api.github.com/user/repos'
    else:
        url = data['repos_url']
        
    page_no = 1
    repos_data = []
    tmp_url = url

    while (True):
        response = requests.get(url, auth = auth)
        response = response.json()
        # print(response)    
        repos_data = repos_data + response
        
        tmp = len(response)
        
        if (tmp == 30):
            page_no = page_no + 1
            url = tmp_url + '?page=' + str(page_no)
        else:
            break

    cnt = 1

    # all_names = []
    values = {
        
    }

    for i, repo in enumerate(repos_data):
        data = []
        data.append(repo['id'])                                                        #0
        data.append(repo['name'])                                                      #1
        data.append(repo['description'])                                               #2

        cnt += 1
        values.update({repo['name']:i})

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

    labs = []
    root = tk.Tk()

    row = tk.Frame(root)
    row.pack(side=tk.TOP,anchor='w', padx=5)
    lab = tk.Label(row,text="")
    lab.pack(side=tk.LEFT)
    labs.append(lab)

    row = tk.Frame(root)
    row.pack(side=tk.TOP,anchor='w', padx=5)
    tk.Label(row,text="Select the Repository: ").pack(side=tk.LEFT, padx = 5)

    v = tk.StringVar(root,"-1")
    for (text, value) in values.items():
        row = tk.Frame(root)
        row.pack(side=tk.TOP,anchor='w',padx=5)
        Radiobutton(row, text = text, variable = v,value=value).pack(side=tk.LEFT,anchor='w', padx = 5)
    
    row = tk.Frame(root)
    row.pack(side=tk.TOP,anchor='w',padx=10)
    b1 = tk.Button(row,text="Start",command=(lambda  v=v, auth=auth: choiceOfRepo(v,auth,root)))
    b1.pack(side=tk.LEFT,padx = 5)

    row = tk.Frame(root)
    row.pack(side=tk.TOP)
    tk.Label(row)

    root.mainloop()

