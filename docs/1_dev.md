# Create dev environment
python3 -m venv .venv

# Load dev environment
source .venv/bin/activate
pip install -r requirements.txt --upgrade

# run app
streamlit run app/home.py

# distribute to streamlit
https://share.streamlit.io/
