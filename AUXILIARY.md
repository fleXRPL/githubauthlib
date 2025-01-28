# Python Environment Setup Guide

This guide covers various approaches to setting up your Python environment for working with githubauthlib.

## Managing PYTHONPATH

### Understanding PYTHONPATH

PYTHONPATH is an environment variable that tells Python where to look for modules. When you import a module, Python searches through the directories listed in PYTHONPATH.

### Adding to PYTHONPATH

#### Temporary Configuration

##### Linux/macOS

```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/githubauthlib"
```

##### Windows Command Prompt

```cmd
set PYTHONPATH=%PYTHONPATH%;C:\path\to\githubauthlib
```

##### Windows PowerShell

```powershell
$env:PYTHONPATH += ";C:\path\to\githubauthlib"
```

#### Permanent Configuration

##### Linux/macOS

1. Open your shell configuration file:

   ```bash
   # For bash
   nano ~/.bashrc
   # For zsh
   nano ~/.zshrc
   ```

2. Add the export line:

   ```bash
   export PYTHONPATH="${PYTHONPATH}:/path/to/githubauthlib"
   ```

3. Apply changes:

   ```bash
   source ~/.bashrc  # or ~/.zshrc
   ```

##### Windows

1. Open System Properties:
   - Press `Win + Pause/Break` or
   - Right-click on 'This PC' → Properties → Advanced system settings

2. Click "Environment Variables"

3. Under "System Variables":
   - If PYTHONPATH exists: Add `;C:\path\to\githubauthlib`
   - If not: Create new with name `PYTHONPATH` and value `C:\path\to\githubauthlib`

### Virtual Environments

Instead of modifying PYTHONPATH, consider using virtual environments:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

# Install package in development mode
pip install -e .
```

## Project Structure

Recommended project structure for development:

```bash
githubauthlib/
│
├── .git/
├── .gitignore
├── README.md
├── AUXILIARY.md
├── LICENSE
├── setup.py
├── requirements.txt
│
├── githubauthlib/
│   ├── __init__.py
│   └── github_auth.py
│
├── tests/
│   ├── __init__.py
│   └── test_github_auth.py
│
└── docs/
    ├── conf.py
    └── index.rst
```

## Import Strategies

### Absolute Imports (Recommended)

```python
from githubauthlib import get_github_token
```

### Relative Imports (For Package Development)

```python
from .github_auth import get_github_token
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**
   - Verify PYTHONPATH configuration
   - Check virtual environment activation
   - Confirm package installation

2. **ImportError**
   - Check Python version compatibility
   - Verify all dependencies are installed
   - Ensure correct file permissions

3. **Path Issues**
   - Use `python -c "import sys; print(sys.path)"` to check Python's search path
   - Verify path separators (/ vs \) are correct for your OS

### Getting Help

If you encounter issues:

1. Check the GitHub Issues page
2. Review error logs
3. Include relevant environment details when reporting issues:

   ```bash
   python --version
   pip list
   echo $PYTHONPATH
   ```

## Best Practices

1. Use virtual environments for isolation
2. Prefer absolute imports over relative imports
3. Keep PYTHONPATH modifications temporary when possible
4. Document all environment setup requirements
5. Use consistent path separators per OS
