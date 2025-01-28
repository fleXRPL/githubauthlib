#!/usr/bin/env python3
"""
This module provides GitHub authentication for macOS, Windows, and Linux systems.

The module retrieves GitHub tokens from the system's secure storage:
- macOS: Keychain Access
- Windows: Credential Manager
- Linux: libsecret

Written by: garotm
"""

import subprocess
import platform
import logging
import re
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GitHubAuthError(Exception):
    """Base exception for GitHub authentication errors."""
    pass

class CredentialHelperError(GitHubAuthError):
    """Raised when there's an error with the credential helper."""
    pass

class UnsupportedPlatformError(GitHubAuthError):
    """Raised when the operating system is not supported."""
    pass

def validate_token(token: str) -> bool:
    """
    Validate the format of a GitHub token.
    
    Args:
        token (str): The token to validate
        
    Returns:
        bool: True if the token format is valid, False otherwise
    """
    # GitHub tokens are 40 characters long and contain only hexadecimal characters
    token_pattern = re.compile(r'^gh[ps]_[A-Za-z0-9_]{36}$|^[a-f0-9]{40}$')
    return bool(token_pattern.match(token))

def get_github_token() -> Optional[str]:
    """
    Retrieves the GitHub token from the system's secure storage.

    Returns:
        str: The GitHub token if found and valid
        
    Raises:
        CredentialHelperError: If there's an error accessing the credential helper
        UnsupportedPlatformError: If the operating system is not supported
    """
    system = platform.system()
    
    try:
        if system == "Darwin":
            return _get_token_macos()
        elif system == "Windows":
            return _get_token_windows()
        elif system == "Linux":
            return _get_token_linux()
        else:
            raise UnsupportedPlatformError(f"Unsupported operating system: {system}")
    except subprocess.CalledProcessError as e:
        raise CredentialHelperError(f"Error accessing credential helper: {str(e)}")

def _get_token_macos() -> Optional[str]:
    """Retrieve token from macOS keychain."""
    output = subprocess.check_output(
        ["git", "credential-osxkeychain", "get"],
        input="protocol=https\nhost=github.com\n",
        universal_newlines=True,
        stderr=subprocess.PIPE
    )
    
    for line in output.split('\n'):
        if line.startswith('password='):
            token = line.split('=')[1].strip()
            if validate_token(token):
                return token
            else:
                logger.warning("Retrieved token failed validation")
                return None
    
    logger.info("No GitHub token found in macOS keychain")
    return None

def _get_token_windows() -> Optional[str]:
    """Retrieve token from Windows Credential Manager."""
    helper = subprocess.check_output(
        ["git", "config", "--get", "credential.helper"],
        universal_newlines=True
    ).strip()
    
    if helper not in ["manager", "manager-core", "wincred"]:
        raise CredentialHelperError("Windows credential manager not configured")
        
    output = subprocess.check_output(
        ["git", "credential", "fill"],
        input="url=https://github.com\n\n",
        universal_newlines=True
    )
    
    credentials = dict(
        line.split('=', 1) 
        for line in output.strip().split('\n') 
        if '=' in line
    )
    
    token = credentials.get('password')
    if token and validate_token(token):
        return token
        
    logger.info("No valid GitHub token found in Windows Credential Manager")
    return None

def _get_token_linux() -> Optional[str]:
    """Retrieve token from Linux libsecret."""
    try:
        output = subprocess.check_output(
            ["secret-tool", "lookup", "host", "github.com"],
            universal_newlines=True
        )
        
        token = output.strip()
        if validate_token(token):
            return token
            
        logger.warning("Retrieved token failed validation")
        return None
        
    except FileNotFoundError:
        logger.error("libsecret-tools not installed. Please install using your package manager.")
        return None
