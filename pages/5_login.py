import streamlit as st
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

with open("./config.yaml","r") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')


authenticator.login()
