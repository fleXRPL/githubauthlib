# GitHub Authentication Library (githubauthlib)

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
