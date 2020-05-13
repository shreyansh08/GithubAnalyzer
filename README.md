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

Use this link (https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) to generate personal access token of your GitHub profile.     

     
For running the second part of tool (generating single repository analysis),     
Run the tool using the command: python ui.py     
If you want details about other user’s repositories, input their username in Username (repository owner).     
Input your own username and personal access token in the next 2 fields.       
Choose if you want to include private repositories. If you choose to include private repositories, you would need to have both Username and Username (repository owner) to be the same.      
         
For running the third part of tool (generating data about a single user),      
Run the tool using the command: python ui.py      
If you want details about other user, input their username in Username (search user).     
Input your own username and personal access token in the next 2 fields.       
Choose if you want to include private repositories. If you choose to include private repositories, you would need to have both Username and Username (search user) to be the same.
