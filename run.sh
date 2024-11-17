#!/usr/bin/bash

# VIRTUAL ENVIRONMENT
source ~/anaconda3/etc/profile.d/conda.sh
conda activate njad_genai_env

# PROXY 
export https_proxy=http://localhost:7890/

# GOOGLE API KEY
export GOOGLE_API_KEY="AIzaSyC-bePxnbw9BQ_AREJqzYilHrU50TpNS_A"

# LAUNCH APP
python term_genai/ask.py
