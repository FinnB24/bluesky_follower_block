# Bluesky Account Finder and Blocker

## Summary

This is a Python-based tool to search, manage, and block user profiles on the Bluesky platform. With this tool, you can search for profiles based on keywords, view profile details, and block unwanted accounts. It uses the Bluesky API to interact with the platform and requires authentication via your Bluesky handle and app password.

---

## Personal Note

The main reason I created this was to prevent spam/trolling accounts or accounts that promote *certain links* from following my account. Even though blocking these profiles prevents them from interacting with any of your content, they still count as followers. Searching for all of these accounts and blocking them individually takes too much time. 

I noticed people on Reddit and Bluesky support pages asking for an option to remove followers. Since that isn’t currently possible due to how Bluesky works, I designed this tool to block accounts before they find my profile. 

This tool can also be used to find people with similar interests. For instance, you could search for "Screenwrite," and it would return profiles with "Screenwriter" or "Screenwriting" in their handle, name, or bio.

---

## Features / How It Works

### Main UI
- Upon running the program, this is the interface you’ll see:  
  ![image](https://github.com/user-attachments/assets/6c208dc1-149a-4842-86bd-2e00184166c9)

### Features:
1. **Keyword-Based Profile Search**  
   - Input keyword(s) to search for (e.g., "photographer").  
   - The tool searches the handle, profile name, and bio for the specified keywords (case-insensitive).  
   - Links can also be searched for. Separate multiple keywords with commas (e.g., "photographer, artist, blogger").  

2. **Control Search Size**  
   - Specify the number of profiles to retrieve (must be between 1 and 100).  

3. **Found Profiles**  
   - After searching, the program saves all found profiles into `found_handles.txt` for future reference.  
   - The "Total Handles" display updates to show how many profiles were found (it will typically match the number you set).

4. **View Profile Details**  
   - Click "Show Found Handles (TXT)" to view the saved handles in a pop-up window.  
   - Select any handle to see its profile details, including **name**, **bio**, and **handle**.  

5. **Block Accounts**  
   - Specify the number of accounts to block (between 1 and 100).  
   - Click "Block Selected Handles" to block them. Blocked profiles are removed from `found_handles.txt` and added to `blocked_handles.txt`.  

---

## What This Program Can’t Do (Yet)

- **Organize Handles by Keywords**  
  Handles found using multiple keywords aren’t categorized into separate lists based on the keyword they matched.  

- **Directly Copy Handle Details**  
  In the "Show Found Handles" pop-up, text is currently not selectable. To copy a handle, you’ll need to open `found_handles.txt` manually and search for it there.  

- **Individual Blocking**  
  You can’t yet select specific accounts to block; you can only specify the number of accounts to block from the top of the list.

---

## Configuration

Before running the program, you must provide your Bluesky credentials in the script:

1. Open the script file in a text/code editor.  
2. Locate these lines near the top of the file:  
   ```python
   BSKY_HANDLE = "yourhandle.bsky.social"
   BSKY_PASSWORD = "yourapppassword"
   ```  
3. Replace `yourhandle.bsky.social` and `yourapppassword` with your Bluesky handle and app password, respectively.  

---

## Example Workflow

1. **Search for Profiles**  
   - Enter keywords like "blogger, artist" and set the profile count to 50.  
   - Click "Search." Profiles matching the keywords will appear in `found_handles.txt`.

2. **View Profile Details**  
   - Click "Show Found Handles (TXT)" and select a profile to view their **name**, **bio**, and **handle**.

3. **Block Accounts**  
   - Set the number of accounts to block (e.g., 20) and click "Block Selected Handles."  
   - The first 20 profiles from `found_handles.txt` will be blocked and moved to `blocked_handles.txt`.

---

## File Structure

- `main.py` – The main Python script for the program.  
- `found_handles.txt` – Stores all profiles found during searches.  
- `blocked_handles.txt` – Stores all profiles that have been blocked.  

---

## Notes

1. **Authentication**  
   - Use a valid Bluesky app password for authentication.  
   - If authentication fails, double-check your credentials.  

2. **API Limitations**  
   - The program adheres to Bluesky API rate limits. Avoid excessive searches in a short time to prevent being temporarily restricted.  

3. **Debugging**  
   - Enable debugging mode in the script for additional logging information:  
     ```python
     debug_mode = True
     ```

---

## License

This project is licensed under the MIT License. Feel free to use, modify, and share it!  

---

Let me know if you want this tailored further, or if you'd like help setting up a GitHub repository to showcase this project! 😊
