#!/bin/bash

# Step 1: Check Python version
echo "Step 1: Checking Python version..."

# Get the installed Python version
PYTHON_VERSION=$(python --version 2>&1)

# Check if Python version is compatible (3.8, 3.9, or 3.10)
if [[ "$PYTHON_VERSION" == *"3.6"* || "$PYTHON_VERSION" == *"3.7"* || "$PYTHON_VERSION" == *"3.8"* || "$PYTHON_VERSION" == *"3.9"* ]]; then
    echo "Python version $PYTHON_VERSION is compatible. Proceeding with the setup..."
else
    echo "Python version is not compatible or not found. Installing Python 3.9..."

    # Install Python 3.9 based on OS
    if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Installing Python 3.9 on Linux/MacOS..."

        # Update package list and install dependencies
        sudo apt update
        sudo apt install -y software-properties-common
        sudo add-apt-repository ppa:deadsnakes/ppa -y
        sudo apt update
        sudo apt install -y python3.9 python3.9-dev python3.9-venv python3-pip

        # Verify Python installation
        python3.9 --version
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "Installing Python 3.9 on Windows..."

        # Check if Chocolatey is installed
        if ! command -v choco &> /dev/null; then
            echo "Chocolatey is not installed. Installing Chocolatey first..."

            # Install Chocolatey
            powershell -NoProfile -ExecutionPolicy Bypass -Command \
                "Set-ExecutionPolicy Bypass -Scope Process; \
                [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; \
                iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"

            if ! command -v choco &> /dev/null; then
                echo "Failed to install Chocolatey. Please install it manually from https://chocolatey.org/."
                exit 1
            fi
        else
            echo "Chocolatey is already installed."
            
            # Check if an upgrade is recommended
            CHOCO_VERSION=$(choco --version)
            echo "Chocolatey version $CHOCO_VERSION is installed."
            echo "If you encounter issues, consider updating Chocolatey by running 'choco upgrade chocolatey' in an elevated command prompt."
        fi

        # Proceed to install Python 3.9 using Chocolatey if available
        if command -v choco &> /dev/null; then
            choco install python --version 3.9 -y
            
            # Verify Python installation
            if command -v python &> /dev/null; then
                python --version
            else
                echo "Failed to install Python 3.9. Please install it manually."
                exit 1
            fi
        else
            echo "Chocolatey is not available for installing Python. Please install Python 3.9 manually."
            exit 1
        fi
    fi
fi

# Step 2: Check for virtualenv
echo "Step 2: Checking for virtualenv..."

if ! command -v virtualenv &> /dev/null; then
    echo "virtualenv not found. Installing..."
    pip install virtualenv
else
    echo "virtualenv is already installed."
fi

# Step 3: Create or activate the virtual environment
echo "Step 3: Creating and activating the virtual environment..."

PROJECT_DIR="$(pwd)"
VENV_DIR="$PROJECT_DIR/venv"
echo $PROJECT_DIR
# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    
    # Try first method to create virtual environment
    virtualenv $VENV_DIR
    # Check if activation files were created
    if [ ! -f "$VENV_DIR/bin/activate" ] && [ ! -f "$VENV_DIR/Scripts/activate" ]; then
        echo "First method failed. Trying python -m venv method..."
        rm -rf $VENV_DIR
        python -m venv $VENV_DIR
    fi

    # If still not created, try the third method
    if [ ! -f "$VENV_DIR/bin/activate" ] && [ ! -f "$VENV_DIR/Scripts/activate" ]; then
        echo "Second method failed. Trying python3 -m venv method..."
        rm -rf $VENV_DIR
        python3 -m venv $VENV_DIR
    fi

    # Final check if virtual environment was created
    if [ -f "$VENV_DIR/bin/activate" ] || [ -f "$VENV_DIR/Scripts/activate" ]; then
        echo "Virtual environment successfully created."
    else
        echo "Virtual environment creation failed. Exiting..."
        exit 1
    fi
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment based on OS
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Activating virtual environment for Linux/MacOS..."
    source "$VENV_DIR/bin/activate"
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "Activating virtual environment for Windows..."
    source "$VENV_DIR/Scripts/activate"
else
    echo "Unknown OS. Cannot activate virtual environment."
    exit 1
fi

# Step 4: Install dependencies
echo "Step 4: Installing dependencies from requirements.txt..."
python -m pip install --upgrade pip

if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    pip install -r $PROJECT_DIR/requirements.txt
else
    echo "requirements.txt not found. Please ensure it exists in the project directory."
    exit 1
fi

# Step 5: Fetching system IP address (optional for server running)
echo "Step 5: Fetching system IP address..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    IP_ADDRESS=$(hostname -I | awk '{print $1}')
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    IP_ADDRESS=$(ipconfig | grep -oP "IPv4 Address[. ]*:\s*\K[\d.]+")
fi

# Step 6: Start Django application
echo "Step 6: Starting Django application..."
if [[ -n "$IP_ADDRESS" ]]; then
    echo "Running server at http://$IP_ADDRESS:7001"
    python manage.py runserver "$IP_ADDRESS:7001"
else
    echo "Could not fetch IP address. Running server on default http://localhost:7001"
    python manage.py runserver localhost:7001
fi


# Step 3: Create or activate the virtual environment
echo "Step 3: Creating and activating the virtual environment..."
