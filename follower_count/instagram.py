#!/usr/bin/env python3
"""This file contains functionality for parsing instagram profiles"""

import json
import requests
from html.parser import HTMLParser

SCHEME = "https"
URL = "www.instagram.com"


class ProfileParser(HTMLParser):
    """Used to extract Instagram account information (Followers & Following) from html."""

    def __init__(self):
        """Constructor"""

        HTMLParser.__init__(self)
        self.followers = 0
        self.following = 0
        self._in_script_tag = False
        self._found_profile_info = False

    def handle_starttag(self, tag: str, attrs: list):
        """Looks for section of HTML that may contain information we're looking for.

        Args:
            tag (str): The name of the tag converted to lower case
            attrs (list): (name, value) Pairs containing attritbutes found inside tag's brackets 
        """
        # Early out when we've found the information we're looking for
        if self._found_profile_info == True:
            return

        # Look for script tags
        if tag == "script":
            for name, value in attrs:
                if name == "type" and value == "text/javascript":
                    self._in_script_tag = True
                    return

    def handle_data(self, data):
        """Checks the data for a html tag when we've flagged that we're in a script tag.

        Args:
            data (str): Content of HTML section  
        """
        # Early out when we've found the information we're looking for
        if self._found_profile_info == True:
            return

        if self._in_script_tag:
            key = "window._sharedData"
            if data.startswith(key):
                # We only want to use the data assigned to `window._sharedData` and to skip the `;` at the end
                shared_data = json.loads(data[len(f"{key} = "):-1])
                graphql_user = shared_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]
                # Update the users info
                self.followers = int(graphql_user["edge_followed_by"]["count"])
                self.following = int(graphql_user["edge_follow"]["count"])
                # Log that we've found the profile information
                self._found_profile_info = True
            # Log that we've completed looking through the script tag
            self._in_script_tag = False


def get_profile_page(username: str):
    """If profile link is publicly accessible proceed, otherwise return None.

    Args:
        username (str): Instagram username for which information will be printed.

    Returns:
        str: Either profile link or None
    """

    response = requests.get(f"{SCHEME}://{URL}/{username}")

    # If the instagram page was found
    if response.status_code == 200:
        return response.text

    return None


def print_influence(username: str):
    """Print the profile's follower and following information.

    Args:
        username (str): Instagram username for which information will be printed.
    """
    response = get_profile_page(username)

    if response:
        parser = ProfileParser()
        parser.feed(response)
        parser.close()
        print(username)
        print("Following -", parser.following)
        print("Followers -", parser.followers)
    else:
        print("Profile not found for username:", username)
