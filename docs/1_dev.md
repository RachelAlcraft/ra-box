# Create dev environment
python3 -m venv .venv

# Load dev environment
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --upgrade

# run app
streamlit run app/home.py

# distribute to streamlit
This will be automatically distributed to streamlit on push to main  
https://share.streamlit.io/
