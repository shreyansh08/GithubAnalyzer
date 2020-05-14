import json
import requests
import numpy as np
import pandas as pd
import time
import tkinter as tk
import random
import os
import sqlite3

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

def code(topic,nStars,nForks,nContr,nRel):

	root = tk.Tk()
	labs = makeform(root)
	lab = labs[0]

    
	root.update()

	cred = json.loads(open('uiBackEnd/temp.json').read())
	authDetails = HTTPBasicAuth(cred['username'], cred['password'])

	session = requests.Session()
	session.auth = (authDetails.username,authDetails.password) 

	url = 'https://api.github.com/search/repositories?q=' + str(topic) + '&sort=stars&order=desc?page=1'
	lab = labs[0]
	lab["text"] = "Fetching Repositories: page 1"
	root.update()

	datas = session.get(url)
	data = datas.json()

	# get names from the raw data
	# data = np.array(data)

	all_repo = data['items']

	print('All repos fetched')
	print('\n')

	#--------------------------------------------------------------------------------------------------------------------------------

	repo_info = []

	cnt = 1

	for repo in all_repo:
		if(repo['forks'] > int(nForks) and repo['stargazers_count'] > int(nStars)):
			data = []
			data.append(repo['id'])
			data.append(repo['name'])
			data.append(repo['html_url'])
			data.append(repo['description'])
			data.append(repo['created_at'])
			data.append(repo['size'])
			data.append(repo['stargazers_count'])
			data.append(repo['language'])
			data.append(repo['forks'])
			data.append(repo['score'])
			data.append(repo['open_issues'])
			data.append(repo['subscribers_url'])
			data.append(repo['languages_url'])
			data.append(repo['contributors_url'])
			data.append(repo['issue_events_url'])
			data.append(repo['issue_comment_url'])
			data.append(repo['issues_url'])
			data.append(repo['releases_url'])
			data.append(repo['pulls_url'])

			repo_info.append(data)

		cnt += 1
		# print(repo['score'])

	print(all_repo[0])

	count = 1
	while 'next' in  datas.links.keys():
		datas = session.get(datas.links['next']['url'])
		data = (datas.json())

		lab["text"] = "Fetching Repositories: page "+str(count+1)
		root.update()

		all_repo = data['items']
		for repo in all_repo:
			if(repo['forks'] > 50 and repo['stargazers_count'] > 50):
				data = []
				data.append(repo['id'])                             #0
				data.append(repo['name'])                           #1                               
				data.append(repo['html_url'])                       #2
				data.append(repo['description'])                    #3
				data.append(repo['created_at'])                     #4
				data.append(repo['size'])                           #5
				data.append(repo['stargazers_count'])               #6
				data.append(repo['language'])                       #7
				data.append(repo['forks'])                          #8
				data.append(repo['score'])                          #9
				data.append(repo['open_issues'])                    #10
				data.append(repo['subscribers_url'])                       #11
				data.append(repo['languages_url'])                  #12
				data.append(repo['contributors_url'])               #13
				data.append(repo['issue_events_url'])               #14
				data.append(repo['issue_comment_url'])              #15
				data.append(repo['issues_url'])                     #16
				data.append(repo['releases_url'])                   #17
				data.append(repo['pulls_url'])						#18

				repo_info.append(data)
		count += 1
		if count == 5:
			break

	print('All Data Fetched')
	print('\n')

	filename = str(topic) + '.csv'
	repo_df = pd.DataFrame(repo_info, columns=['Id','Name','URL','Description','Created','Size','Stars','Primal Language','Forks','Score','Open Issues Count','Watchers Count','Languages Url','Contributors Url','Issue Event Url','Issue Comment Url','Issues Url','Releases Url','Pulls Url']) 

	# print(len(repo_info))

	for i in range(repo_df.shape[0]):
		lab["text"] = "Fetching Languages for Repo: " + str(i+1)
		root.update()
		response = session.get(repo_df.loc[i, 'Languages Url'])
		response = response.json()
		# print(i, response)
		if response != {}:
			languages = []
			for key, value in response.items():
				languages.append(key)
			languages = (u', '.join(languages)).encode('utf-8')
			repo_df.loc[i, 'Languages'] = (str(languages))[1:-1]
		else:
			repo_df.loc[i, 'Languages'] = ""


	filename = str(topic) + '.csv'
	repo_df.to_csv(filename)

	print(len(repo_info))

	lab["text"] = "CSV created succesfully."
	root.update()

	print('Main CSV obtained')
	print('\n')

	complete_subscribers_data = []

	filtered_subscribers_data = []
	#0 - Login -> Username
	#1 - Type Of Login
	#2 - ID

	for i in range(len(repo_info)):
		
		lab["text"] = "Fetching Subscribers Data for Repo: " + str(i+1)
		root.update()

		url_subscribers = repo_info[i][11] + '?page=1'
		page_no = 1
		
		curr_repo_id = repo_info[i][0]
		
		subscribers_data = []
		
		all_filtered_subscribers_for_one_repo = []
		
		while(True):
			response = session.get(url_subscribers)
			response = response.json()
			
			if(len(response) == 0):
				break
				
			subscribers_data += response
			
			for subs in response:
				data = []
				data.append(subs['login'])
				data.append(subs['type'])
				data.append(curr_repo_id)
				all_filtered_subscribers_for_one_repo.append(data)
				
			page_no += 1
			
			url_subscribers = repo_info[i][11] + '?page=' + str(page_no)
			
		complete_subscribers_data.append(subscribers_data)
		filtered_subscribers_data.append(all_filtered_subscribers_for_one_repo)

	for_csv = []
	for i in filtered_subscribers_data:
		for j in i:
			for_csv.append(j)

	filename = str(topic) + '-subscribers.csv'
	subscribers_repo_df = pd.DataFrame(for_csv, columns=['LoginId','Type','Id']) 
	subscribers_repo_df.to_csv(filename)

	random.shuffle(repo_info)

	for x in range(6):

		if(x == 0):
			cred = json.loads(open('uiBackEnd/temp.json').read())
			authDetails = HTTPBasicAuth(cred['username'], cred['password'])

			session = requests.Session()
			session.auth = (authDetails.username,authDetails.password) 
		elif(x == 1):
			cred = json.loads(open('uiBackEnd/temp1.json').read())
			authDetails = HTTPBasicAuth(cred['username'], cred['password'])

			session = requests.Session()
			session.auth = (authDetails.username,authDetails.password)	
		elif(x == 2):
			cred = json.loads(open('uiBackEnd/temp2.json').read())
			authDetails = HTTPBasicAuth(cred['username'], cred['password'])

			session = requests.Session()
			session.auth = (authDetails.username,authDetails.password)	
		elif(x == 3):
			cred = json.loads(open('uiBackEnd/temp3.json').read())
			authDetails = HTTPBasicAuth(cred['username'], cred['password'])

			session = requests.Session()
			session.auth = (authDetails.username,authDetails.password)	
		elif(x == 4):
			cred = json.loads(open('uiBackEnd/temp4.json').read())
			authDetails = HTTPBasicAuth(cred['username'], cred['password'])

			session = requests.Session()
			session.auth = (authDetails.username,authDetails.password)	
		else:
			cred = json.loads(open('uiBackEnd/temp5.json').read())
			authDetails = HTTPBasicAuth(cred['username'], cred['password'])

			session = requests.Session()
			session.auth = (authDetails.username,authDetails.password)

		# time.sleep(200)
		print('Main loop',x)
		print('\n')
		repos_after_filter1 = repo_info[x*50 : (x+1)*50]

		complete_releases_data = []
		repos_after_filter2 = []

		filtered_releases_data = []
		#0 - Draft
		#1 - Prerelease
		#2 - Created_At
		#3 - Published_At
		#4 - Body
		#5 - ID

		for i in range(len(repos_after_filter1)):
			
			lab["text"] = "Fetching Releases for Repository: " + str(x*50+i+1)
			root.update()

			url_releases = repos_after_filter1[i][17][:-5] + '?page=1'
			print('url_releases',url_releases)

			page_no = 1

			curr_repo_id = repos_after_filter1[i][0]    
			releases_data = []

			all_filtered_releases_for_one_repo = []
			# cc = 0
			while (True):
		#         cc += 1
				# print(cc+1000)
				response = session.get(url_releases)
				response = response.json()

				if(len(response) == 0):
					break

				releases_data += response
				# print(page_no)
				# print('\n')

				for release in response:
					data = []
					data.append(release['draft'])
					data.append(release['prerelease'])
					data.append(release['created_at'])
					data.append(release['published_at'])
					data.append(release['body'])
					data.append(curr_repo_id)
					all_filtered_releases_for_one_repo.append(data)

				page_no += 1

				url_releases = repos_after_filter1[i][17][:-5] + '?page=' + str(page_no)            
			
			# print(len(releases_data))

			if(len(releases_data) > int(nRel)):
				complete_releases_data.append(releases_data)
				repos_after_filter2.append(repos_after_filter1[i])
				filtered_releases_data.append(all_filtered_releases_for_one_repo)

		print('Releases Fetched',x)
		print('\n')

		for_csv = []
		for i in filtered_releases_data:
			for j in i:
				for_csv.append(j)

		filename = str(topic) + '-releases' + str(x) + '.csv'
		releases_repo_df = pd.DataFrame(for_csv, columns=['Draft','Prerelease','Created_at','Published_at','Details','Id']) 
		releases_repo_df.to_csv(filename)

		print('Releases CSV formed',x)
		print('\n')


		complete_contributors_data = []
		repos_after_filter3 = []

		filtered_contributors_data = []
		#0 - Login -> Username
		#1 - Contribution
		#2 - ID

		for i in range(len(repos_after_filter2)):

			url_contributors = repos_after_filter2[i][13] + '?page=1'
			print('url_contributors',url_contributors)

			lab["text"] = "Fetching Contributors for Repository: " + str(x*50+i+1)
			root.update()

			page_no = 1

			curr_repo_id = repos_after_filter2[i][0]

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
					all_filtered_contributors_data_for_one_repo.append(data)

				page_no += 1
				
				url_contributors = repos_after_filter2[i][13] + '?page=' + str(page_no)

			# print(len(contributors_data))

			if(len(contributors_data) > int(nContr)):
				complete_contributors_data.append(contributors_data)
				repos_after_filter3.append(repos_after_filter2[i])
				filtered_contributors_data.append(all_filtered_contributors_data_for_one_repo)

		print('Contributors Fetched',x)
		print('\n')

		for_csv = []
		for i in filtered_contributors_data:
			for j in i:
				for_csv.append(j)

		filename = str(topic) + '-contributors' + str(x) + '.csv'
		contributor_repo_df = pd.DataFrame(for_csv, columns=['LoginId','Contributions','Id']) 
		contributor_repo_df.to_csv(filename)

		print('Contributors CSV formed',x)
		print('\n')


		complete_issues_data = []
		repos_after_filter4 = []

		filtered_issue_data = []
		#0 - Title
		#1 - State
		#2 - Created_At
		#3 - Updated_At
		#4 - Closed_At
		#5 - Type Of Author
		#6 - Body 
		#7 - Issue Comment
		#8 - ID

		for i in range(len(repos_after_filter3)):

			url_issue = repos_after_filter3[i][16][:-9] + '?page=1'
			print('url_issue',url_issue)
			
			lab["text"] = "Fetching Issues for Repository: " + str(x*50+i+1)
			root.update()

			page_no = 1

			curr_repo_id = repos_after_filter3[i][0]

			issues_data = []

			all_filtered_issues_for_one_repo = []
			
			# cc = 0
			
			while (True):
				response = session.get(url_issue)
		#         print(cc)
				# cc += 1
				response = response.json()
				
				if(len(response) == 0):
					break

				issues_data += response
				# print(page_no)
				# print('\n')

				for issue in response:
					data = []
					data.append(issue['title'])
					data.append(issue['state'])
					data.append(issue['created_at'])
					data.append(issue['updated_at'])
					data.append(issue['closed_at'])
					data.append(issue['author_association'])
					data.append(issue['body'])
					
					temp_string = issue['comments_url']
					comment = ""
					
					temp_response = session.get(temp_string)
					temp_response = temp_response.json()
					
					if(len(temp_response) != 0):
						for comments in temp_response:    
							comment = comments['body']
					
					data.append(comment)
					data.append(curr_repo_id)
					all_filtered_issues_for_one_repo.append(data)

				page_no += 1
				
				url_issue = repos_after_filter3[i][16][:-9] + '?page=' + str(page_no)


			# print(len(issues_data))
			# print('\n')
			# print(repos_after_filter1[i][10])

			if(len(issues_data) > 0):
				complete_issues_data.append(issues_data)
				repos_after_filter4.append(repos_after_filter3[i])
				filtered_issue_data.append(all_filtered_issues_for_one_repo)

		print('Issues Fetched',x)
		print('\n')

		for_csv = []
		for i in filtered_issue_data:
			for j in i:
				for_csv.append(j)

		# print(filtered_issue_data[0])
		filename = str(topic) + '-issues' + str(x) + '.csv'
		issue_repo_df = pd.DataFrame(for_csv, columns=['Title','State','Created_at','Updated_at','Closed_at','Author','Details','Comments','Id']) 
		issue_repo_df.to_csv(filename)

		print('Issues CSV formed',x)
		print('\n')


		complete_pull_request_data = []

		filtered_pull_request_data = []
		#0 - Created_At
		#1 - Updated_At
		#2 - Closed_At
		#3 - Merged_At
		#4 - Body
		#5 - Id

		for i in range(len(repos_after_filter4)):
			
			url_pull_request = repos_after_filter4[i][18][:-9]
			print(url_pull_request)
			# print(url_pull_request)
			page_no = 1

			lab["text"] = "Fetching Pull Requests Data for Repository: " + str(x*50+i+1)
			root.update()
			
			pull_request_data = []

			curr_repo_id = repos_after_filter4[i][0]
			
			all_filtered_pull_requests_for_one_repo = []
			
			while (True):
				
				response = session.get(url_pull_request)
				response = response.json()
				
				if(len(response) == 0):
					break
					
				pull_request_data += response
				
				for pull_request in response:
					data = []
					data.append(pull_request['created_at'])
					data.append(pull_request['updated_at'])
					data.append(pull_request['closed_at'])
					data.append(pull_request['merged_at'])
					data.append(pull_request['body'])
					data.append(curr_repo_id)
					all_filtered_pull_requests_for_one_repo.append(data)
					
				page_no += 1
				
				url_pull_request = repos_after_filter4[i][18][:-9] + '?page=' + str(page_no)
				
			complete_pull_request_data.append(pull_request_data)
			filtered_pull_request_data.append(all_filtered_pull_requests_for_one_repo)
					
		print('Pull Requests Fetched',x)

		for_csv = []
		for i in filtered_pull_request_data:
			for j in i:
				for_csv.append(j)

		filename = str(topic) + '-pull_request' + str(x) + '.csv'
		releases_repo_df = pd.DataFrame(for_csv, columns=['Created At','Updated At','Closed At','Merged At','Details','Id']) 
		releases_repo_df.to_csv(filename)

	lab["text"] = "Creating a Database File"

	temp_release = []
	temp_issue = []
	temp_contributor = []
	temp_pull_request = []

	for j in range(6):
		s1 = topic + "-releases" + str(j) + ".csv"
		df1 = pd.read_csv(s1)
		temp_release.append(df1)
		os.remove(s1)

		s2 = topic + "-issues" + str(j) + ".csv"
		df2 = pd.read_csv(s2)
		temp_issue.append(df2)
		os.remove(s2)

		s3 = topic + "-contributors" + str(j) + ".csv"
		df3 = pd.read_csv(s3)
		temp_contributor.append(df3)
		os.remove(s3)

		s4 = topic + "-pull_request" + str(j) + ".csv"
		df4 = pd.read_csv(s4)
		temp_pull_request.append(df4)
		os.remove(s4)
		
	all_releases = pd.concat(temp_release, ignore_index = True)
	all_releases = all_releases.drop(all_releases.columns[0],axis=1)
	
	all_issues = pd.concat(temp_issue,  ignore_index = True)
	all_issues = all_issues.drop(all_issues.columns[0],axis=1)
	
	all_contributors = pd.concat(temp_contributor,  ignore_index = True)
	all_contributors = all_contributors.drop(all_contributors.columns[0],axis=1)

	all_pull = pd.concat(temp_pull_request, ignore_index = True)
	all_pull = all_pull.drop(all_pull.columns[0],axis=1)

	all_issues.to_csv(topic+'-issues.csv')
	all_releases.to_csv(topic+'-releases.csv')
	all_contributors.to_csv(topic+'-contributors.csv')
	all_pull.to_csv(topic+'-pull_request.csv')

	filename = topic + ".db"

	con = sqlite3.connect(filename)
	cur = con.cursor()

	repo_df.to_sql('ALL_DATA' , con , if_exists = 'replace' , index = False)
	all_issues.to_sql('ALL_ISSUE' , con , if_exists = 'replace' , index = False)
	all_releases.to_sql('ALL_RELEASE' , con , if_exists = 'replace' , index = False)
	all_contributors.to_sql('ALL_CONTRIBUTOR' , con , if_exists = 'replace' , index = False)
	all_pull.to_sql('ALL_PULL_REQUEST' , con , if_exists = 'replace' , index = False)
	subscribers_repo_df.to_sql('ALL_SUBSCRIBERS' , con , if_exists = 'replace' , index = False)

	mess = "All process complete. CSV file and database stored in the folder."
	tk.messagebox.showinfo("Process Complete",mess)