#!/usr/bin/env python3
"""
This module provides GitHub auth for macOS or Windows.

Written by: Garot Conklin
"""

import platform
import subprocess


def get_github_token():
    """
    Retrieves the GitHub token from the system's keychain.

    This function uses the 'git' command-line utility to interact with the
    system's keychain. If the system is MacOS, it uses the 'osxkeychain'
    credential helper. If the system is Windows, it uses the 'wincred'
    credential helper. For Linux, it uses libsecret or git credential store.
    For other systems, it prints an error message.

    Returns:
        str: The GitHub token if it could be found, or None otherwise.
    """
    if platform.system() == "Darwin":
        try:
            output = subprocess.check_output(
                ["git", "credential-osxkeychain", "get"],
                input="protocol=https\nhost=github.com\n",
                universal_newlines=True,
                stderr=subprocess.DEVNULL,
            )
            access_token = output.strip().split()[0].split("=")[1]
            return access_token
        except subprocess.CalledProcessError:
            print("GitHub access token not found in osxkeychain.")
            return None
    elif platform.system() == "Windows":
        try:
            output = subprocess.check_output(
                ["git", "config", "--get", "credential.helper"],
                universal_newlines=True,
                stderr=subprocess.DEVNULL,
            )
            if output.strip() == "manager":
                output = subprocess.check_output(
                    ["git", "credential", "fill"],
                    input="url=https://github.com",
                    universal_newlines=True,
                    stderr=subprocess.DEVNULL,
                )
                credentials = {}
                for line in output.strip().split("\n"):
                    key, value = line.split("=")
                    credentials[key] = value.strip()
                access_token = credentials.get("password")
                return access_token
            print("GitHub access token not found in Windows Credential Manager.")
            return None
        except subprocess.CalledProcessError:
            print("Error retrieving GitHub credential helper.")
            return None
    elif platform.system() == "Linux":
        try:
            # Try using libsecret (GNOME Keyring)
            output = subprocess.check_output(
                ["secret-tool", "lookup", "host", "github.com"],
                universal_newlines=True,
                stderr=subprocess.DEVNULL,
            )
            if output.strip():
                return output.strip()
        except FileNotFoundError:
            print("secret-tool not found, falling back to git credential store.")
        except subprocess.CalledProcessError:
            print("No token found in libsecret, falling back to git credential store.")

        # Fall back to git credential store
        try:
            output = subprocess.check_output(
                ["git", "credential", "fill"],
                input="url=https://github.com\n\n",
                universal_newlines=True,
                stderr=subprocess.DEVNULL,
            )
            for line in output.strip().split("\n"):
                if line.startswith("password="):
                    return line.split("=", 1)[1].strip()
            print("GitHub access token not found in git credential store.")
            return None
        except subprocess.CalledProcessError:
            print("Error retrieving GitHub credential from git store.")
            return None
    else:
        print("Unsupported operating system.")
        return None
