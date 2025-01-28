# tests/test_github_auth.py
import unittest
from unittest.mock import patch, MagicMock
import platform
import subprocess
from githubauthlib import (
    get_github_token,
    GitHubAuthError,
    CredentialHelperError,
    UnsupportedPlatformError
)

class TestGitHubAuth(unittest.TestCase):
    """Test cases for GitHub authentication functionality."""

    def setUp(self):
        """Set up test cases."""
        self.valid_token = "ghp_1234567890abcdef1234567890abcdef123456"
        self.invalid_token = "invalid_token"

    @patch('platform.system')
    @patch('subprocess.check_output')
    def test_macos_valid_token(self, mock_subprocess, mock_platform):
        """Test successful token retrieval on macOS."""
        mock_platform.return_value = "Darwin"
        mock_subprocess.return_value = f"password={self.valid_token}\n"
        
        token = get_github_token()
        self.assertEqual(token, self.valid_token)

    @patch('platform.system')
    @patch('subprocess.check_output')
    def test_windows_valid_token(self, mock_subprocess, mock_platform):
        """Test successful token retrieval on Windows."""
        mock_platform.return_value = "Windows"
        mock_subprocess.side_effect = [
            "manager\n",
            f"password={self.valid_token}\n"
        ]
        
        token = get_github_token()
        self.assertEqual(token, self.valid_token)

    @patch('platform.system')
    def test_unsupported_platform(self, mock_platform):
        """Test behavior with unsupported platform."""
        mock_platform.return_value = "SomeOS"
        
        with self.assertRaises(UnsupportedPlatformError):
            get_github_token()

    @patch('platform.system')
    @patch('subprocess.check_output')
    def test_credential_helper_error(self, mock_subprocess, mock_platform):
        """Test handling of credential helper errors."""
        mock_platform.return_value = "Darwin"
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, "git")
        
        with self.assertRaises(CredentialHelperError):
            get_github_token()

    def test_token_validation(self):
        """Test token validation functionality."""
        from githubauthlib.github_auth import validate_token
        
        # Test valid tokens
        self.assertTrue(validate_token("ghp_1234567890abcdef1234567890abcdef123456"))
        self.assertTrue(validate_token("ghs_1234567890abcdef1234567890abcdef123456"))
        self.assertTrue(validate_token("0123456789abcdef0123456789abcdef01234567"))
        
        # Test invalid tokens
        self.assertFalse(validate_token("invalid_token"))
        self.assertFalse(validate_token("ghp_tooshort"))
        self.assertFalse(validate_token("ghi_1234567890abcdef1234567890abcdef123456"))

if __name__ == '__main__':
    unittest.main()
