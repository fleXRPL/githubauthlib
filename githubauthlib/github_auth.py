#!/usr/bin/env python3
"""
This module provides GitHub auth for macOS, Windows, and Linux.

Written by: Garot Conklin
"""

import logging
import platform
import subprocess
from typing import Optional

# Configure logging
logger = logging.getLogger(__name__)


class GitHubAuthError(Exception):
    """Base exception for GitHub authentication errors."""

    pass


class TokenNotFoundError(GitHubAuthError):
    """Raised when no GitHub token is found in the system keychain."""

    pass


class InvalidTokenError(GitHubAuthError):
    """Raised when the retrieved token is invalid or malformed."""

    pass


class PlatformNotSupportedError(GitHubAuthError):
    """Raised when the current platform is not supported."""

    pass


class CredentialHelperError(GitHubAuthError):
    """Raised when credential helper operations fail."""

    pass


def _validate_token(token: str) -> bool:
    """
    Validate GitHub token format.

    Args:
        token: The token to validate

    Returns:
        bool: True if token is valid, False otherwise
    """
    if not token or not isinstance(token, str):
        return False

    # GitHub personal access tokens start with 'ghp_' and are 40 characters long
    # GitHub organization tokens start with 'gho_' and are 40 characters long
    # GitHub fine-grained tokens start with 'github_pat_' and are longer
    # Allow for some flexibility in token length for testing
    if token.startswith("ghp_") and len(token) >= 40:
        return True
    elif token.startswith("gho_") and len(token) >= 40:
        return True
    elif token.startswith("github_pat_") and len(token) > 40:
        return True

    logger.warning("Invalid token format detected")
    return False


def _parse_credential_output(output: str) -> Optional[str]:
    """
    Parse credential helper output to extract password/token.

    Args:
        output: Raw output from credential helper

    Returns:
        Optional[str]: Extracted token or None if not found
    """
    if not output:
        return None

    lines = output.strip().split("\n")
    for line in lines:
        if line.startswith("password="):
            return line.split("=", 1)[1].strip()

    return None


def get_github_token() -> Optional[str]:
    """
    Retrieves the GitHub token from the system's keychain.

    This function uses the 'git' command-line utility to interact with the
    system's keychain. If the system is MacOS, it uses the 'osxkeychain'
    credential helper. If the system is Windows, it uses the 'wincred'
    credential helper. For Linux, it uses libsecret or git credential store.
    For other systems, it raises PlatformNotSupportedError.

    Returns:
        Optional[str]: The GitHub token if it could be found, or None otherwise.

    Raises:
        PlatformNotSupportedError: If the current platform is not supported
        TokenNotFoundError: If no token is found in the system keychain
        InvalidTokenError: If the retrieved token is invalid
        CredentialHelperError: If credential helper operations fail
    """
    if platform.system() == "Darwin":
        try:
            logger.debug("Attempting to retrieve token from macOS keychain")
            output = subprocess.check_output(
                ["git", "credential-osxkeychain", "get"],
                input="protocol=https\nhost=github.com\n",
                universal_newlines=True,
                stderr=subprocess.DEVNULL,
            )

            token = _parse_credential_output(output)
            if not token:
                logger.warning("No token found in macOS keychain")
                raise TokenNotFoundError("GitHub access token not found in osxkeychain")

            if not _validate_token(token):
                logger.error("Invalid token format retrieved from macOS keychain")
                raise InvalidTokenError("Invalid token format")

            logger.info("Successfully retrieved token from macOS keychain")
            return token

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to retrieve token from macOS keychain: {e}")
            raise CredentialHelperError("Failed to access macOS keychain")
    elif platform.system() == "Windows":
        try:
            logger.debug("Attempting to retrieve token from Windows Credential Manager")
            output = subprocess.check_output(
                ["git", "config", "--get", "credential.helper"],
                universal_newlines=True,
                stderr=subprocess.DEVNULL,
            )

            if output.strip() == "manager":
                credential_output = subprocess.check_output(
                    ["git", "credential", "fill"],
                    input="url=https://github.com",
                    universal_newlines=True,
                    stderr=subprocess.DEVNULL,
                )

                token = _parse_credential_output(credential_output)
                if not token:
                    logger.warning("No token found in Windows Credential Manager")
                    raise TokenNotFoundError(
                        "GitHub access token not found in Windows Credential Manager"
                    )

                if not _validate_token(token):
                    logger.error(
                        "Invalid token format retrieved from Windows Credential Manager"
                    )
                    raise InvalidTokenError("Invalid token format")

                logger.info(
                    "Successfully retrieved token from Windows Credential Manager"
                )
                return token
            else:
                logger.warning("Windows Credential Manager not configured")
                raise TokenNotFoundError(
                    "GitHub access token not found in Windows Credential Manager"
                )

        except subprocess.CalledProcessError as e:
            logger.error(
                f"Failed to retrieve token from Windows Credential Manager: {e}"
            )
            raise CredentialHelperError("Failed to access Windows Credential Manager")
    elif platform.system() == "Linux":
        try:
            # Try using libsecret (GNOME Keyring)
            logger.debug("Attempting to retrieve token from Linux libsecret")
            output = subprocess.check_output(
                ["secret-tool", "lookup", "host", "github.com"],
                universal_newlines=True,
                stderr=subprocess.DEVNULL,
            )

            if output.strip():
                token = output.strip()
                if not _validate_token(token):
                    logger.error("Invalid token format retrieved from libsecret")
                    raise InvalidTokenError("Invalid token format")

                logger.info("Successfully retrieved token from Linux libsecret")
                return token

        except FileNotFoundError:
            logger.debug("secret-tool not found, falling back to git credential store")
        except subprocess.CalledProcessError:
            logger.debug(
                "No token found in libsecret, falling back to git credential store"
            )

        # Fall back to git credential store
        try:
            logger.debug("Attempting to retrieve token from git credential store")
            output = subprocess.check_output(
                ["git", "credential", "fill"],
                input="url=https://github.com\n\n",
                universal_newlines=True,
                stderr=subprocess.DEVNULL,
            )

            token = _parse_credential_output(output)
            if not token:
                logger.warning("No token found in git credential store")
                raise TokenNotFoundError(
                    "GitHub access token not found in git credential store"
                )

            if not _validate_token(token):
                logger.error("Invalid token format retrieved from git credential store")
                raise InvalidTokenError("Invalid token format")

            logger.info("Successfully retrieved token from git credential store")
            return token

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to retrieve token from git credential store: {e}")
            raise CredentialHelperError("Failed to access git credential store")
    else:
        logger.error(f"Unsupported operating system: {platform.system()}")
        raise PlatformNotSupportedError(
            f"Unsupported operating system: {platform.system()}"
        )
