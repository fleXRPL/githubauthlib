#!/bin/bash

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting build preparation...${NC}\n"

# Function to run checks and report status
run_check() {
    local check_name=$1
    local command=$2
    
    echo -e "${YELLOW}Running ${check_name}...${NC}"
    if eval "$command"; then
        echo -e "${GREEN}✓ ${check_name} passed${NC}\n"
        return 0
    else
        echo -e "${RED}✗ ${check_name} failed${NC}\n"
        return 1
    fi
}

# Function to clean up
cleanup() {
    echo -e "\n${YELLOW}Cleaning up...${NC}"
    if [ -n "${VIRTUAL_ENV}" ]; then
        deactivate 2>/dev/null || true
    fi
    rm -rf .venv/
    echo -e "${GREEN}✓ Cleanup completed${NC}\n"
}

# Create and activate virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv .venv
source .venv/bin/activate
echo -e "${GREEN}✓ Virtual environment created and activated${NC}\n"

# Clean previous builds
echo -e "${YELLOW}Cleaning previous builds...${NC}"
rm -rf build/ dist/ *.egg-info
echo -e "${GREEN}✓ Previous builds cleaned${NC}\n"

# Install build dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install black isort flake8 pytest pytest-cov build
echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# Run tests and checks
echo -e "${YELLOW}Running tests and checks...${NC}"

# Format and lint
run_check "Black formatting" "black githubauthlib tests"
run_check "isort check" "isort githubauthlib tests"
run_check "Flake8 linting" "flake8 githubauthlib tests"

# Run tests with coverage
run_check "Pytest with coverage" "pytest tests/ --cov=githubauthlib --cov-report=term-missing --cov-fail-under=90"

echo -e "${GREEN}✓ All checks passed${NC}\n"

# Build package
echo -e "${YELLOW}Building package...${NC}"
if python -m build; then
    echo -e "${GREEN}✓ Package built${NC}\n"
    
    # List generated files
    echo -e "\n${YELLOW}Generated files:${NC}"
    ls -l dist/
    
    echo -e "\n${YELLOW}Next steps:${NC}"
    echo -e "1. Create and push a new version tag: ${GREEN}git tag v1.0.0 && git push origin v1.0.0${NC}"
    echo -e "2. The GitHub Action will automatically publish to PyPI"
    echo -e "3. Once published, verify the package: ${GREEN}https://pypi.org/project/githubauthlib/${NC}"
    echo -e "4. Test installation: ${GREEN}pip install githubauthlib${NC}"
    
    # Clean up only if build was successful
    cleanup
    exit 0
else
    echo -e "${RED}✗ Package build failed${NC}\n"
    cleanup
    exit 1
fi 