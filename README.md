# GitHub Authentication Library (githubauthlib)

A Python library for securely retrieving GitHub tokens from system keychains across different operating systems.

#### versions

[![PyPI version](https://badge.fury.io/py/githubauthlib.svg)](https://pypi.org/project/githubauthlib/)
[![PyPI version](https://img.shields.io/pypi/v/githubauthlib.svg)](https://pypi.org/project/githubauthlib/)
[![Python](https://img.shields.io/pypi/pyversions/githubauthlib.svg)](https://pypi.org/project/githubauthlib/)

#### health

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_githubauthlib&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=fleXRPL_githubauthlib)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_githubauthlib&metric=coverage)](https://sonarcloud.io/summary/new_code?id=fleXRPL_githubauthlib)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_githubauthlib&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=fleXRPL_githubauthlib)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_githubauthlib&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=fleXRPL_githubauthlib)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_githubauthlib&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=fleXRPL_githubauthlib)
[![Dependabot Status](https://img.shields.io/badge/Dependabot-enabled-success.svg)](https://github.com/fleXRPL/githubauthlib/blob/main/.github/dependabot.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

#### stats

[![Downloads](https://pepy.tech/badge/githubauthlib)](https://pepy.tech/project/githubauthlib)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- Cross-platform support:
  - macOS: Uses Keychain Access
  - Windows: Uses Credential Manager
  - Linux: Uses libsecret
- Secure token retrieval with validation
- Comprehensive exception hierarchy for precise error handling
- Structured logging support
- Token format validation (supports personal, organization, and fine-grained tokens)
- Robust credential parsing and sanitization

## Prerequisites

### All Platforms

- Python 3.9 or higher
- Git (with credentials configured)

### Linux-Specific

```bash
# Ubuntu/Debian
sudo apt-get install libsecret-tools

# Fedora
sudo dnf install libsecret
```

## Installation

### From PyPI

```bash
pip install githubauthlib
```

### From Source

```bash
# Clone the repository
git clone https://github.com/GIALaboratory/cloud-platform-engineering.git

# Navigate to the library directory
cd cloud-platform-engineering/githubauthlib

# Install the package
pip install .
```

## Usage

```python
from githubauthlib import (
    get_github_token,
    GitHubAuthError,
    TokenNotFoundError,
    InvalidTokenError,
    PlatformNotSupportedError,
    CredentialHelperError
)

try:
    token = get_github_token()
    print("Token retrieved successfully!")
    print(f"Token: {token[:10]}...")  # Show first 10 chars only
except TokenNotFoundError:
    print("No GitHub token found in system keychain")
except InvalidTokenError:
    print("Invalid token format detected")
except PlatformNotSupportedError:
    print("Current platform is not supported")
except CredentialHelperError:
    print("Failed to access system credential store")
except GitHubAuthError as e:
    print(f"GitHub authentication error: {e}")
```

## Verifying Installation

```bash
# Check installed version
pip list | grep githubauthlib

# View package details
pip show githubauthlib
```

## Development Setup

For development, you may want to add the package directory to your PYTHONPATH. See [AUXILIARY.md](AUXILIARY.md) for detailed instructions.

## Breaking Changes in v2.0.0

⚠️ **Important**: Version 2.0.0 introduces breaking changes:

- `get_github_token()` now raises specific exceptions instead of returning `None`
- All error handling now uses structured logging instead of print statements
- Token validation is now strict and validates format
- Python 3.6, 3.7, and 3.8 support has been removed (EOL)

### Migration Guide

**Before (v1.x.x):**

```python
token = get_github_token()
if token:
    print("Success!")
else:
    print("Failed!")
```

**After (v2.0.0):**

```python
try:
    token = get_github_token()
    print("Success!")
except TokenNotFoundError:
    print("No token found!")
except GitHubAuthError as e:
    print(f"Error: {e}")
```

## Troubleshooting

1. **Token Not Found**
   - Verify Git credentials are properly configured
   - Check system keychain for GitHub credentials
   - Handle `TokenNotFoundError` exception

2. **Permission Issues**
   - Ensure proper system keychain access
   - Verify Python has required permissions
   - Handle `CredentialHelperError` exception

3. **Linux Issues**
   - Confirm libsecret-tools is installed
   - Check D-Bus session is running
   - Handle `PlatformNotSupportedError` exception

4. **Invalid Token Format**
   - Verify token starts with `ghp_` (personal), `gho_` (organization), or `github_pat_` (fine-grained)
   - Handle `InvalidTokenError` exception

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
