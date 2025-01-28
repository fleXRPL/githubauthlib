"""
GitHub authentication library for retrieving tokens from system keychains.

This library provides a unified interface for retrieving GitHub tokens
from various system-specific secure storage solutions.
"""

from .github_auth import (
    get_github_token,
    GitHubAuthError,
    CredentialHelperError,
    UnsupportedPlatformError
)

__version__ = '1.0.0'
__author__ = 'garotm'
__license__ = 'MIT'
