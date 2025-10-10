# tests/test_github_auth.py
import platform
import subprocess
import unittest
from unittest.mock import patch

from githubauthlib import (CredentialHelperError, InvalidTokenError,
                           PlatformNotSupportedError, TokenNotFoundError,
                           get_github_token)


class TestGitHubAuth(unittest.TestCase):
    """Test cases for GitHub authentication functionality."""

    def setUp(self):
        """Set up test cases."""
        self.test_token = "ghp_1234567890abcdef1234567890abcdef123456"
        self.current_platform = platform.system()  # Store current platform for tests

    @patch("platform.system")
    @patch("subprocess.check_output")
    def test_macos_token_retrieval(self, mock_subprocess, mock_platform):
        """Test successful token retrieval on macOS."""
        mock_platform.return_value = "Darwin"
        mock_subprocess.return_value = f"password={self.test_token}\n"

        token = get_github_token()
        self.assertEqual(token, self.test_token)
        mock_subprocess.assert_called_with(
            ["git", "credential-osxkeychain", "get"],
            input="protocol=https\nhost=github.com\n",
            universal_newlines=True,
            stderr=subprocess.DEVNULL,
        )

    @patch("platform.system")
    @patch("subprocess.check_output")
    def test_macos_no_token(self, mock_subprocess, mock_platform):
        """Test macOS behavior when no token is found."""
        mock_platform.return_value = "Darwin"
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, "git")

        with self.assertRaises(CredentialHelperError):
            get_github_token()

    @patch("platform.system")
    @patch("subprocess.check_output")
    def test_windows_token_retrieval(self, mock_subprocess, mock_platform):
        """Test successful token retrieval on Windows."""
        mock_platform.return_value = "Windows"
        mock_subprocess.side_effect = [
            "manager\n",
            f"protocol=https\nhost=github.com\npassword={self.test_token}\n",
        ]

        token = get_github_token()
        self.assertEqual(token, self.test_token)

    @patch("platform.system")
    @patch("subprocess.check_output")
    def test_windows_no_manager(self, mock_subprocess, mock_platform):
        """Test Windows behavior when credential manager is not configured."""
        mock_platform.return_value = "Windows"
        mock_subprocess.return_value = "wincred\n"

        with self.assertRaises(TokenNotFoundError):
            get_github_token()

    @patch("platform.system")
    @patch("subprocess.check_output")
    def test_windows_credential_error(self, mock_subprocess, mock_platform):
        """Test Windows behavior when credential helper fails."""
        mock_platform.return_value = "Windows"
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, "git")

        with self.assertRaises(CredentialHelperError):
            get_github_token()

    @patch("platform.system")
    @patch("subprocess.check_output")
    def test_linux_libsecret_token(self, mock_subprocess, mock_platform):
        """Test successful token retrieval on Linux using libsecret."""
        mock_platform.return_value = "Linux"
        mock_subprocess.return_value = self.test_token

        token = get_github_token()
        self.assertEqual(token, self.test_token)
        mock_subprocess.assert_called_with(
            ["secret-tool", "lookup", "host", "github.com"],
            universal_newlines=True,
            stderr=subprocess.DEVNULL,
        )

    @patch("platform.system")
    @patch("subprocess.check_output")
    def test_linux_fallback_token(self, mock_subprocess, mock_platform):
        """Test Linux fallback to git credential store."""
        mock_platform.return_value = "Linux"
        mock_subprocess.side_effect = [
            FileNotFoundError(),  # secret-tool not found
            f"protocol=https\nhost=github.com\npassword={self.test_token}\n",
        ]

        token = get_github_token()
        self.assertEqual(token, self.test_token)

    @patch("platform.system")
    @patch("subprocess.check_output")
    def test_linux_all_methods_fail(self, mock_subprocess, mock_platform):
        """Test Linux behavior when both libsecret and git credential store fail."""
        mock_platform.return_value = "Linux"
        mock_subprocess.side_effect = [
            subprocess.CalledProcessError(1, "secret-tool"),  # libsecret fails
            subprocess.CalledProcessError(1, "git"),  # git credential store fails
        ]

        with self.assertRaises(CredentialHelperError):
            get_github_token()

    @patch("platform.system")
    @patch("subprocess.check_output")
    def test_linux_credential_store_no_password(self, mock_subprocess, mock_platform):
        """Test Linux git credential store with no password in output."""
        mock_platform.return_value = "Linux"
        mock_subprocess.side_effect = [
            FileNotFoundError(),  # secret-tool not found
            "protocol=https\nhost=github.com\n",  # no password in output
        ]

        with self.assertRaises(TokenNotFoundError):
            get_github_token()

    @patch("platform.system")
    def test_unsupported_platform(self, mock_platform):
        """Test behavior with unsupported platform."""
        mock_platform.return_value = "SomeOS"
        with self.assertRaises(PlatformNotSupportedError):
            get_github_token()

    @patch("platform.system")
    @patch("subprocess.check_output")
    def test_macos_invalid_token(self, mock_subprocess, mock_platform):
        """Test macOS behavior with invalid token format."""
        mock_platform.return_value = "Darwin"
        mock_subprocess.return_value = "password=invalid_token\n"

        with self.assertRaises(InvalidTokenError):
            get_github_token()

    @patch("platform.system")
    @patch("subprocess.check_output")
    def test_windows_invalid_token(self, mock_subprocess, mock_platform):
        """Test Windows behavior with invalid token format."""
        mock_platform.return_value = "Windows"
        mock_subprocess.side_effect = [
            "manager\n",
            "protocol=https\nhost=github.com\npassword=invalid_token\n",
        ]

        with self.assertRaises(InvalidTokenError):
            get_github_token()

    @patch("platform.system")
    @patch("subprocess.check_output")
    def test_linux_invalid_token(self, mock_subprocess, mock_platform):
        """Test Linux behavior with invalid token format."""
        mock_platform.return_value = "Linux"
        mock_subprocess.return_value = "invalid_token"

        with self.assertRaises(InvalidTokenError):
            get_github_token()

    @patch("platform.system")
    @patch("subprocess.check_output")
    def test_macos_empty_output(self, mock_subprocess, mock_platform):
        """Test macOS behavior with empty credential output."""
        mock_platform.return_value = "Darwin"
        mock_subprocess.return_value = ""

        with self.assertRaises(TokenNotFoundError):
            get_github_token()

    @patch("platform.system")
    @patch("subprocess.check_output")
    def test_windows_empty_output(self, mock_subprocess, mock_platform):
        """Test Windows behavior with empty credential output."""
        mock_platform.return_value = "Windows"
        mock_subprocess.side_effect = [
            "manager\n",
            "",
        ]

        with self.assertRaises(TokenNotFoundError):
            get_github_token()

    def test_validate_token_invalid_types(self):
        """Test token validation with invalid types."""
        from githubauthlib.github_auth import _validate_token

        # Test None
        self.assertFalse(_validate_token(None))

        # Test empty string
        self.assertFalse(_validate_token(""))

        # Test non-string
        self.assertFalse(_validate_token(123))

    def test_validate_token_fine_grained(self):
        """Test token validation with fine-grained token."""
        from githubauthlib.github_auth import _validate_token

        # Test fine-grained token
        fine_grained_token = (
            "github_pat_1234567890abcdef1234567890abcdef1234567890abcdef"
            "1234567890abcdef"
        )
        self.assertTrue(_validate_token(fine_grained_token))

    @patch("platform.system")
    @patch("subprocess.check_output")
    def test_linux_libsecret_empty_output(self, mock_subprocess, mock_platform):
        """Test Linux libsecret with empty output."""
        mock_platform.return_value = "Linux"
        mock_subprocess.side_effect = [
            "",  # Empty output from libsecret
            f"protocol=https\nhost=github.com\npassword={self.test_token}\n",
        ]

        token = get_github_token()
        self.assertEqual(token, self.test_token)

    @patch("platform.system")
    @patch("subprocess.check_output")
    def test_linux_git_credential_store_invalid_token(
        self, mock_subprocess, mock_platform
    ):
        """Test Linux git credential store with invalid token."""
        mock_platform.return_value = "Linux"
        mock_subprocess.side_effect = [
            FileNotFoundError(),  # secret-tool not found
            "protocol=https\nhost=github.com\npassword=invalid_token\n",
        ]

        with self.assertRaises(InvalidTokenError):
            get_github_token()


if __name__ == "__main__":
    unittest.main()
