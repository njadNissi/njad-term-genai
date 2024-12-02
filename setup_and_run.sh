#!/usr/bin/bash

## I. E N V I R O N M E N T   V A R I A B L E S
## by default it will be somewhere like at: /home/$USER/Downloads/njad-term-genai
BASE_DIR_PATH="/media/njad/NJAD/coding/Python/Projects/njad-term-genai"

VENV_NAME="genaiterm_env"

## GOOGLE API KEY
## Uncomment and set your key in the line below if not set in the ".bashrc" file.
# export GOOGLE_API_KEY="PASTE YOUR GOOGLE API SECRET API KEY HERE"

## II. N E T W O R K  P R O X Y
## Unmment below two lines if your location requires a proxy to reach google
# export http_proxy=http://localhost:7890
# export https_proxy=http://localhost:7890

CONDA_FLAG=1
CONDA_BASE_DIR=/home/$USER/anaconda3 # if this default path is not your case, change this line to match your system.
# ==================== III. V I R T U A L   E N V I R O N M E N T   S E T T I N G ==============

## ===III.A  SET CONDA ENV=====

##  Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Error: conda is not installed. Switching to VirualEnv..."
    CONDA_FLAG=0

else # CONDA EXISTS
    conda init
    # Check if the conda environment already exists
    if conda env list | grep -q "$VENV_NAME"; then
        echo "Conda environment '$VENV_NAME' already exists."
        # [].  L A U N C H  A P P 
        $CONDA_BASE_DIR/envs/$VENV_NAME/bin/python "$BASE_DIR_PATH/term_genai/ask.py"

    else # Create the conda environment and install pip and project dependencies
        conda env create -f $BASE_DIR_PATH/environment.yml
    fi
    CONDA_FLAG=1
fi

# ===III.B SET VirtualEnv ENV=====

if [ "$CONDA_FLAG" -eq 0 ]; then
    # Check if the virtual environment exists
    if [ -d "$BASE_DIR_PATH/$VENV_NAME" ]; then
        # Activate the virtual environment
        source "$BASE_DIR_PATH/$VENV_NAME/bin/activate"
        echo "Activated virtual environment: $VENV_NAME"
    else
        echo "creating a python environment..."
        python3 -m venv "$BASE_DIR_PATH/$VENV_NAME" && source "$BASE_DIR_PATH/$VENV_NAME/bin/activate"
        $BASE_DIR_PATH/$VENV_NAME/bin/python install --upgrade pip
        $BASE_DIR_PATH/$VENV_NAME/bin/pip install -r $BASE_DIR_PATH/requirements.txt
        echo "You're using: $(which python) and $(which pip)"
    fi    
    # [].  L A U N C H  A P P
    $BASE_DIR_PATH/$VENV_NAME/bin/python "$BASE_DIR_PATH/term_genai/ask.py"
fi


# V. C L O S E   G R A C E F U L L Y

# V.A  DEACTIVATE ENVIRONENT
if [ "$CONDA_FLAG" -eq 1 ]; then
    conda init 
    conda deactivate
else # deactivate virtualenv
    deactivate
fi

# V.B  RESET NETWORK ENV
unset http_proxy
unset https_proxy