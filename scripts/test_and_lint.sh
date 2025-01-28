#!/bin/bash

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting test and lint checks...${NC}\n"

# Function to run a command and check its status
run_check() {
    echo -e "${YELLOW}Running $1...${NC}"
    if eval "$2"; then
        echo -e "${GREEN}✓ $1 passed${NC}\n"
    else
        echo -e "${RED}✗ $1 failed${NC}\n"
        exit 1
    fi
}

# Function to clean up
cleanup() {
    echo -e "\n${YELLOW}Cleaning up...${NC}"
    deactivate 2>/dev/null || true
    rm -rf .venv/
    echo -e "${GREEN}✓ Cleanup completed${NC}\n"
}

# Set up trap to clean up on script exit
trap cleanup EXIT

# Create and activate virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv .venv
source .venv/bin/activate
echo -e "${GREEN}✓ Virtual environment created and activated${NC}\n"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install black isort flake8 pytest pytest-cov
echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# Format code
run_check "Black formatting" "black githubauthlib tests"
run_check "isort check" "isort githubauthlib tests"

# Lint with flake8
run_check "Flake8 linting" "flake8 githubauthlib tests"

# Run tests with coverage
run_check "Pytest with coverage" "pytest tests/ --cov=githubauthlib --cov-report=term-missing --cov-fail-under=90"

# Generate coverage report
echo -e "${YELLOW}Generating HTML coverage report...${NC}"
coverage html
echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}\n"

echo -e "${GREEN}All checks passed successfully!${NC}" 