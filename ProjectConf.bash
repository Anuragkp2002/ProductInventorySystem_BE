#!/bin/bash

# Step 1: Checking Python version
echo "Step 1: Checking Python version..."

# Get the installed Python version
PYTHON_VERSION=$(python3 --version 2>&1)

# Check if the Python version is 3.8, 3.9, 3.10, or 3.12
if [[ "$PYTHON_VERSION" == *"3.8"* || "$PYTHON_VERSION" == *"3.9"* || "$PYTHON_VERSION" == *"3.10"* || "$PYTHON_VERSION" == *"3.12"* ]]; then
    echo "Python version $PYTHON_VERSION is compatible. Proceeding with the setup..."
else
    echo "Python version is not compatible. Installing the latest version of Python..."

    # Install the latest Python version based on OS

    # For Linux (Ubuntu/Debian-based systems)
    if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Installing the latest Python version on Linux/MacOS..."

        # Update package list
        sudo apt update

        # Install dependencies for building Python
        sudo apt install -y software-properties-common

        # Add the deadsnakes PPA (for Ubuntu) or update repository list for other Linux distributions
        sudo add-apt-repository ppa:deadsnakes/ppa -y
        sudo apt update

        # Install the latest Python 3 (this will install the latest available Python version)
        sudo apt install -y python3 python3-pip python3-dev python3-venv

        # Verify Python installation
        python3 --version
    fi

    # For Windows
    if [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "Installing the latest Python version on Windows..."

        # Windows installation via Chocolatey (ensure Chocolatey is installed first)
        choco install python --version latest -y

        # Verify Python installation
        python --version
    fi

    echo "Python installation complete."
fi

# Step 2: Check for virtualenv
echo "Step 2: Checking for virtualenv..."

# Check if virtualenv is installed, if not, install it
if ! command -v virtualenv &> /dev/null; then
    echo "virtualenv not found. Installing..."
    pip install virtualenv
else
    echo "virtualenv is already installed."
fi

# Step 3: Create or activate the virtual environment
echo "Step 3: Creating and activating the virtual environment..."

# Set project directory and virtual environment location
PROJECT_DIR="$(pwd)"
VENV_DIR="$PROJECT_DIR/venv"

# Create virtual environment if not already exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
else
    echo "Virtual environment already exists."
fi

# Detect the OS and activate the virtual environment accordingly
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    # Linux or macOS
    echo "Activating virtual environment for Linux/MacOS..."
    source $VENV_DIR/bin/activate
    echo "$VENV_DIR"
    echo "(venv): Virtual Environment Activated Successfully"

elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    echo "Activating virtual environment for Windows..."
    .\venv\Scripts\activate
    echo "($VENV_DIR): Virtual Environment Activated Successfully"

else
    echo "Unknown OS. Cannot activate virtual environment."
    exit 1
fi

# Step 4: Ensure pip is up-to-date and install dependencies
echo "Step 4: Installing dependencies from requirements.txt..."
# Upgrade pip to the latest version
pip install --upgrade pip
# Install dependencies from requirements.txt
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r $PROJECT_DIR/requirements.txt
else
    echo "requirements.txt file not found. Please make sure the file exists in the project directory."
    exit 1
fi

# Step 5: Check if Django is installed
# echo "Step 5: Checking if Django is installed..."
# if ! python -c "import django" &> /dev/null; then
#     echo "Django is not installed. Installing Django..."
#     pip install django
# else
#     echo "Django is already installed."
# fi

# Step 6: Fetching system IP address (optional for server running)
echo "Step 6: Fetching system IP address..."
SYSTEM_IP=$(hostname -I | awk '{print $1}')
echo "System IP address: $SYSTEM_IP"

# Step 7: Start Django application
# echo "Step 7: Starting Django application..."
# python $PROJECT_DIR/manage.py runserver 0.0.0.0:8000
echo "Step 5: Starting Django application..."
if [[ -n "$SYSTEM_IP" ]]; then
    echo "Running server at http://$SYSTEM_IP:8000"
    python manage.py runserver "$SYSTEM_IP:8000"
else
    echo "Could not fetch IP address. Running server on default http://localhost:8000"
    python manage.py runserver
fi
