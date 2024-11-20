#!/usr/bin/bash

# I. G O O G L E  A P I  K E Y
# Uncomment and set your key in the line below if not set in the ".bashrc" file.
# export GOOGLE_API_KEY="PASTE YOUR GOOGLE API SECRET API KEY HERE"

# II. N E T W O R K  P R O X Y
Uncomment below two lines if your location requires a proxy to reach google
# export http_proxy=http://localhost:7890/
# export https_proxy=http://localhost:7890/


ENV_NAME="term_genai_env"
CONDA_FLAG=1
# ==================== III. V I R T U A L   E N V I R O N M E N T   S E T T I N G ==============

# ===III.A  SET CONDA ENV=====

#  Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Error: conda is not installed. Switching to VirualEnv..."
    CONDA_FLAG=0

else # CONDA EXISTS
    # Check if the conda environment already exists
    if conda env list | grep -q "$ENV_NAME"; then
        echo "Conda environment 'term_genai_env' already exists."

    else # Create the conda environment and install pip and project dependencies
        conda create -n "$ENV_NAME" python=3.12  # Adjust python version as needed
        if [[ $? -eq 0 ]]; then
            echo "Conda environment 'term_genai_env' created successfully."
            source ~/anaconda3/etc/profile.d/conda.sh
            conda activate "$ENV_NAME"
            pip --version || conda install --upgrade pip
            pip install -r requirements.txt
        else
            echo "Error creating conda environment '$ENV_NAME'."
            CONDA_FLAG=0
        fi
    fi
fi

# ===III.B SET VirtualEnv ENV=====

if ["$CONDA_FLAG" -eq 1 ]; then
    echo "creating a python environment..."
    python3 -m venv "$ENV_NAME"
    source "./$ENV_NAME/bin/activate"
    echo "You're using: $(which python) and $(which pip)"
fi


# IV.  L A U N C H  A P P
python term_genai/ask.py

# V. C L O S E   G R A C E F U L L Y

# V.A  DEACTIVATE ENVIRONENT
if [ "$CONDA_FLAG" -eq 1 ]; then
    conda deactivate
else
    deactivate
fi
# V.B  RESET NETWORK ENV
unset http_proxy
unset https_proxy