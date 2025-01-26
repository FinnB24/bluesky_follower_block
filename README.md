Summary:
This is a Python-based tool to search, manage, and block user profiles on the Bluesky platform. With this tool, you can search for profiles based on keywords, view profile details, and block unwanted accounts. It uses the Bluesky API to interact with the platform and requires authentication via your Bluesky handle and app password.

Personal Note:
The Main reason why I coded this, was to prevent spam/trolling accounts or accounts that promote *certain links* from following my account. Even though you can block these profiles and prevent them from interacting with any of your content, they will still counted as a follower (And searching for all of these Accounts and blocking them all individually will take too long). I found a lot of people on reddit and the bluesky Support/request-stuff pages that wanted an option to remove followers. Apparently that is not possible because of how Bluesky works, so I thought to just block them all before finding my Account.
Though this can also be used to find people with similar interests like you, since you could search for eg "Screenwrite" and it would find profiles that have "Screenwriter/Screenwriting" in their Handle/Name/Bio

Features/How it works:
- This will be the UI shown after running the program:
![image](https://github.com/user-attachments/assets/6c208dc1-149a-4842-86bd-2e00184166c9)
- Input keyword(s) that you want to search for. This will search the Handle, Profile Name and Bio for these words. Upper/lower case does not matter here; Links can also be searched for; Seperate multiple Keywords with a comma.
- Input a number 1<__<101 of how many profiles it should find
- Search button to start the search
- The "Total Handles:__" will show the amount of handles that it found. In the most cases, it will be the number of Accounts that you told it to search for
- The found profiles for the keyword(s) will be stored to a file (found_handles.txt) for future reference. 
- View details of a specific handle, including name, bio, and handle itself: >>"Show Found Handles (TXT) >> Click on any handle and it will show the Infos
- To Block Accounts, select a number 1<__<101 of how many Accounts you want to Block and Click the Button
- The Blocked handles will be removed from the "found_handles.txt" and are stored in blocked_handles.txt

What this Program Cant do (yet):
- Store Handles in different Lists, based on what keyword they were found when searching for multiple keywords
- Select the Text in >>"Show Found Handles (TXT) >>  Handle Info. To select a Handle, you will need to go into the .txt file and select it from there (Ctrl. + F for searching)
- Select Individual Accounts to block (eg. Box select)

Configuration:
Before running the tool, update your Bluesky handle and app password in the script:
- Open the script file in a text/code editor.
- Replace the placeholders for in line 10/11 with your Bluesky credentials:
    -> BSKY_HANDLE = "yourhandle.bsky.social"
    -> BSKY_PASSWORD = "yourapppassword"
