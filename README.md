# GithubAnalyzer
3 different type of analysis based on user, repository

The following libraries are needed with python3.7 installed on your device to run the tool successfully.

tkinter    
numpy    
pandas    
matplotlib    
json   
requests   
sqlite3    


For running the first part of tool (generating data-set according to topic and input parameters),
Go to folder \uiBackEnd.     
There are 6 files temp.json, temp1.json, temp2.json, temp3.json, temp4.json, temp5.json     
Each of the json files has 2 empty entries, username and password.       
Take 6 github account usernames and their personal access tokens and store them in each of the files. To generate access code for your account, follow this link (https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line). Alternatively, you can also use your github password in place of using a personal access token, but that is not a recommended practise and should be avoided.      
Run the tool using the command: python ui.py    
Input all the needed inputs and run the script.   
     
For running the second and third part of tool (generating single repository analysis or generating data about a single user),    
Run the tool using the command: python ui.py     
Select the option (Single Repository or Single User) and input username and personal access token.   
Choose if you want to include private repositories.    
