# GitHub Authentication Library (githubauthlib)

[![PyPI version](https://badge.fury.io/py/githubauthlib.svg)](https://pypi.org/project/githubauthlib/)
[![Python](https://img.shields.io/pypi/pyversions/githubauthlib.svg)](https://pypi.org/project/githubauthlib/)
[![Tests](https://github.com/fleXRPL/githubauthlib/actions/workflows/tests.yml/badge.svg)](https://github.com/fleXRPL/githubauthlib/actions/workflows/tests.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_githubauthlib&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=fleXRPL_githubauthlib)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_githubauthlib&metric=coverage)](https://sonarcloud.io/summary/new_code?id=fleXRPL_githubauthlib)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_githubauthlib&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=fleXRPL_githubauthlib)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_githubauthlib&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=fleXRPL_githubauthlib)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_githubauthlib&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=fleXRPL_githubauthlib)
[![Dependabot Status](https://img.shields.io/badge/Dependabot-enabled-success.svg)](https://github.com/fleXRPL/githubauthlib/blob/main/.github/dependabot.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Downloads](https://pepy.tech/badge/githubauthlib)](https://pepy.tech/project/githubauthlib)

A Python library for securely retrieving GitHub tokens from system keychains across different operating systems.

## Features

- Cross-platform support:
  - macOS: Uses Keychain Access
  - Windows: Uses Credential Manager
  - Linux: Uses libsecret
- Secure token retrieval
- Token validation
- Comprehensive error handling
- Logging support

## Prerequisites

### All Platforms

- Python 3.6 or higher
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
from githubauthlib import get_github_token, GitHubAuthError

try:
    token = get_github_token()
    if token:
        print("Token retrieved successfully!")
    else:
        print("No token found in system keychain")
except GitHubAuthError as e:
    print(f"Error retrieving token: {e}")
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

## Troubleshooting

1. **Token Not Found**
   - Verify Git credentials are properly configured
   - Check system keychain for GitHub credentials

2. **Permission Issues**
   - Ensure proper system keychain access
   - Verify Python has required permissions

3. **Linux Issues**
   - Confirm libsecret-tools is installed
   - Check D-Bus session is running

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
