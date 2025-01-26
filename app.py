import tkinter as tk
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from atproto import Client
from atproto.exceptions import AtProtocolError
import os
import re
import json

BSKY_HANDLE = " "  #ADD BLUESKY HANDLE
BSKY_PASSWORD = " "     #ADD BLUESKY PW 


client = Client()

# Initialize global variables
found_handles = set()  #store found handles
blocked_handles = set()  #store blocked handles
debug_mode = False  #True for detailed logging, False to suppress it

def initialize_client():
    """Initialize the Bluesky client and log in."""
    
    try:
        client.login(BSKY_HANDLE, BSKY_PASSWORD)
        print(f"Logged in successfully as {BSKY_HANDLE}")
        
        # Check if login was successful by confirming that 'client.me' is set
        if not client.me:
            print("Login failed: Authentication not set.")
            messagebox.showerror("Error", "Login failed. Authentication not set.")
            return False  #return False if login fails
        return True  #return True if login successful

    except AtProtocolError as e:
        print(f"Login failed: {e}")
        messagebox.showerror("Error", "Failed to authenticate. Check credentials.")
        return False  #Return False if an error occurs during login

def block_selected_handles():
    global found_handles, blocked_handles

    # Ensure user is logged in before proceeding
    if not initialize_client():  #only proceed if the login is successful
        return

    num_to_block = int(block_spinbox.get())  #get the number of handles to block

    if num_to_block <= 0 or num_to_block > len(found_handles):
        messagebox.showerror("Error", "Invalid number of handles to block.")
        return

    blocked = set(list(found_handles)[:num_to_block])

    # Block handles using block_user function
    for handle in blocked:
        success = block_user(handle, client)
        if success:
            blocked_handles.add(handle)
            found_handles.remove(handle)

    save_handles_to_file()
    save_blocked_handles_to_file()

    update_handle_count()

    messagebox.showinfo("Success", f"Blocked {num_to_block} handles.")

def block_user(handle, client):
    """Block a user by their handle."""
    try:
        # Ensure client is logged in by checking 'client.me'
        if not client.me:
            print("Error: Not logged in.")
            messagebox.showerror("Error", "Authentication required. Please log in first.")
            return False  # Return False if not logged in

        # Get user profile and DID
        profile = client.app.bsky.actor.get_profile({'actor': handle})
        user_did = profile['did']

        # Create block record
        client.app.bsky.graph.block.create(
            repo=client.me.did,  # Ensure we're using the logged-in user's DID
            record={'subject': user_did, 'createdAt': client.get_current_time_iso()}
        )
        print(f"Blocked: {handle}")
        return True

    except AtProtocolError as e:
        print(f"Error blocking {handle}: {e}")
        return False


def search_profiles(term, limit=100, cursor=None):
    """Search profiles using the given term and limit the number of results."""
    try:
        params = {"q": term, "limit": limit}
        if cursor:
            params["cursor"] = cursor
        
        if debug_mode:
            print(f"Making API request with term '{term}', limit {limit}, cursor {cursor}...")

        response = client.app.bsky.actor.search_actors(params=params)
        
        if hasattr(response, "model_dump"):
            response_data = response.model_dump()  # Pydantic V2
        else:
            response_data = response  # It might already be a dictionary

        profiles = response_data.get("actors", [])
        next_cursor = response_data.get("cursor", None)

        if profiles and debug_mode:
            print(f"Found {len(profiles)} profiles for keyword '{term}'")

        matched_profiles = []
        for profile in profiles:
            handle = profile.get("handle", "").lower()  # Extract the handle, ensure it's lowercase

            if handle in blocked_handles or handle in found_handles:
                continue

            matched_profiles.append(profile)

        return matched_profiles, next_cursor

    except Exception as e:
        print(f"Error fetching profiles: {e}")
        return [], None

def load_handles_from_file():
    """Load handles from the 'found_handles.txt' and 'blocked_handles.txt' files."""
    global found_handles, blocked_handles
    found_handles.clear()
    blocked_handles.clear()

    try:
        with open("found_handles.txt", "r") as file:
            for line in file:
                found_handles.add(line.strip())
    except FileNotFoundError:
        print("No 'found_handles.txt' found. Starting fresh.")

    try:
        with open("blocked_handles.txt", "r") as file:
            for line in file:
                blocked_handles.add(line.strip())
    except FileNotFoundError:
        print("No 'blocked_handles.txt' found. Starting fresh.")

def save_handles_to_file():
    """Save found handles to the 'found_handles.txt' file."""
    with open("found_handles.txt", "w") as file:
        for handle in sorted(found_handles):
            file.write(f"{handle}\n")

def save_blocked_handles_to_file():
    """Save blocked handles to the 'blocked_handles.txt' file."""
    with open("blocked_handles.txt", "w") as file:
        for handle in sorted(blocked_handles):
            file.write(f"{handle}\n")

def update_handle_count():
    """Update the live counter of handles in the found_handles.txt file."""
    handle_count = len(found_handles)
    handle_count_label.config(text=f"Total Handles: {handle_count}")

def search_button_click():
    global found_handles  # Use global found_handles to track the matched profiles
    initialize_client()

    if client is None:
        messagebox.showerror("Error", "Failed to authenticate. Check credentials.")
        return

    load_handles_from_file()  # Load previously found handles

    keywords = keywords_entry.get().split(",")  # Split keywords for multiple searches
    num_results = int(num_results_spinbox.get())  # Number of profiles to find
    total_found = 0  # Counter to track the number of profiles found
    cursor = None  # For pagination

    print(f"Starting search for keywords: {keywords}")
    
    for keyword in keywords:
        keyword = keyword.strip()  # Clean up the keyword
        found_for_keyword = 0  # To count profiles found for the current keyword
        
        while total_found < num_results:
            profiles, cursor = search_profiles(keyword, limit=num_results - total_found, cursor=cursor)
            
            if profiles:
                for profile in profiles:
                    handle = profile.get("handle", "").lower()  # Extract the handle, ensure it's lowercase

                    if handle and handle not in found_handles and handle not in blocked_handles:
                        found_handles.add(handle)
                        total_found += 1  # Increment the total found counter

                        if total_found >= num_results:
                            break
            
            if not cursor or total_found >= num_results:
                break

        if total_found >= num_results:
            break

    save_handles_to_file()

    update_handle_count()

    if total_found > 0:
        messagebox.showinfo("Search Completed", f"Found {total_found} new accounts.")
    else:
        messagebox.showinfo("Search Completed", "No matching accounts found.")

    print(f"Total found profiles: {total_found}")
    print(f"Current found handles: {found_handles}")


# Function to show the contents of found_handles.txt and allow clicking a handle button
def show_found_handles_txt():
    try:
        with open('found_handles.txt', 'r') as file:
            handles = file.readlines()
            if not handles:
                messagebox.showinfo("No Data", "The 'found_handles.txt' file is empty.")
                return
            
            # Create a new window to display the handles
            txt_window = tk.Toplevel(root)
            txt_window.title("Found Handles")

            # Create a frame to hold the buttons
            frame = tk.Frame(txt_window)
            frame.pack(padx=10, pady=10)

            # Create a button for each handle
            for handle in handles:
                handle = handle.strip()
                button = tk.Button(frame, text=handle, command=lambda h=handle: show_handle_details(h))
                button.pack(padx=5, pady=5, fill='x')

    except FileNotFoundError:
        messagebox.showerror("Error", "The 'found_handles.txt' file does not exist.")

# Function to fetch and show the details of a selected handle
# Function to fetch and show the details of a selected handle
# Function to fetch and show the details of a selected handle
def show_handle_details(handle):
    try:
        # Ensure the client is authenticated before fetching profile data
        if not initialize_client():  # This will log in if not already authenticated
            messagebox.showerror("Error", "Authentication required. Please log in.")
            return
        
        # Fetch the profile data
        profile = client.app.bsky.actor.get_profile({'actor': handle})
        
        # Check if the profile is of the expected type
        if hasattr(profile, 'model_dump'):  # Handling Pydantic model response
            profile_data = profile.model_dump()  # Get a dictionary of the profile data
        else:
            profile_data = profile  # Assume it is already a dictionary if not a Pydantic model
        
        # Print the profile data to debug and inspect its structure
        print(f"Profile data for {handle}: {profile_data}")
        
        # Ensure the profile data is retrieved correctly
        if not profile_data:
            messagebox.showerror("Error", f"No profile found for {handle}")
            return

        # Extracting name and bio from the profile
        name = profile_data.get("displayName") or profile_data.get("name", "N/A")
        bio = profile_data.get("description", "No bio available.")
        
        # Create a new window to display the name and bio
        details_window = tk.Toplevel(root)
        details_window.title(f"Details for {handle}")
        
        # Display the details in the new window
        tk.Label(details_window, text=f"Name: {name}", font=("Arial", 12)).pack(padx=10, pady=10)
        tk.Label(details_window, text=f"Bio: {bio}", font=("Arial", 12), wraplength=400).pack(padx=10, pady=10)

    except AtProtocolError as e:
        messagebox.showerror("Error", f"Failed to fetch profile for {handle}: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred while fetching profile for {handle}: {e}")


# GUI setup
root = tk.Tk()
root.title("Bluesky Account Finder")

found_handles = set()  # To store the found handles
blocked_handles = set()  # To store the blocked handles

tk.Label(root, text="Enter search terms (comma-separated):").pack(padx=10, pady=5)
keywords_entry = tk.Entry(root, width=50)
keywords_entry.pack(padx=10, pady=5)

tk.Label(root, text="Number of search results:").pack(padx=10, pady=5)
num_results_spinbox = tk.Spinbox(root, from_=1, to=100, width=10)
num_results_spinbox.pack(padx=10, pady=5)

tk.Button(root, text="Search", command=search_button_click).pack(padx=10, pady=10)

# Label to display the live counter
handle_count_label = tk.Label(root, text="Total Handles: 0")
handle_count_label.pack(padx=10, pady=5)

# Add button to show contents of found_handles.txt
tk.Button(root, text="Show Found Handles (TXT)", command=show_found_handles_txt).pack(padx=10, pady=10)

# Add block handles section
tk.Label(root, text="Number of handles to block:").pack(padx=10, pady=5)
block_spinbox = tk.Spinbox(root, from_=1, to=100, width=10)
block_spinbox.pack(padx=10, pady=5)

tk.Button(root, text="Block Selected Handles", command=block_selected_handles).pack(padx=10, pady=10)

# Load handles and update counter immediately when the UI starts
load_handles_from_file()
update_handle_count()

root.mainloop()
