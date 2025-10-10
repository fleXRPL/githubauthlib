"""
GitHub authentication library for retrieving tokens from system keychains.

This library provides a unified interface for retrieving GitHub tokens
from various system-specific secure storage solutions.
"""

from .github_auth import (
    CredentialHelperError,
    GitHubAuthError,
    InvalidTokenError,
    PlatformNotSupportedError,
    TokenNotFoundError,
    get_github_token,
)

__version__ = "2.0.0"
__author__ = "garotm"
__license__ = "MIT"

__all__ = [
    "get_github_token",
    "GitHubAuthError",
    "TokenNotFoundError",
    "InvalidTokenError",
    "PlatformNotSupportedError",
    "CredentialHelperError",
]
