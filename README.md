Summary:
This is a Python-based tool to search, manage, and block user profiles on the Bluesky platform. With this tool, you can search for profiles based on keywords, view profile details, and block unwanted accounts. It uses the Bluesky API to interact with the platform and requires authentication via your Bluesky handle and app password.


Features/How it works:
- Search for Bluesky profiles using keywords and view their basic details.
- The found profiles for the keyword(s) will be stored to a file (found_handles.txt) for future reference. There is no option yet for when searching for multiple keywords that the handles are stored in different lists, based on their keyword.
- View details of a specific handle, including name, bio, and handle itself .
4.	Block Accounts: Block selected profiles from the found list.
5.	Persistent Storage: Found and blocked handles are stored in found_handles.txt and blocked_handles.txt.

Configuration:
Before running the tool, update your Bluesky handle and app password in the script:                                ![image](https://github.com/user-attachments/assets/6c208dc1-149a-4842-86bd-2e00184166c9)
- Open the script file in a text/code editor.
- Replace the placeholders for in line 10/11 with your Bluesky credentials:
    -> BSKY_HANDLE = "yourhandle.bsky.social"
    -> BSKY_PASSWORD = "yourapppassword"

