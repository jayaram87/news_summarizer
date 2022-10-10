import os

SITE_URL = 'http://www.indiatoday.in/'
SECRET_PATH = os.path.join(os.getcwd(), 'config', 'secret.yaml')
DB = 'db'
CASDB = 'cassandraDb'
ID = 'clientId'
SECRET = 'secret'
BUNDLE_PATH = os.path.join(os.getcwd(), 'config', 'secure-connect-news-app.zip')
USERNAME = 'username'
PASSWORD = 'password'
MODEL_CONFIG_PATH = os.path.join(os.getcwd(), 'config', 'model.yaml')
PARAMS = 'params'
TEXT_LEN = 'max_len'
NUM_BEAMS = 'num_beams'
REPETITION_PENALTY = 'repetition_penalty'
LEN_PENALTY = 'length_penalty'
SUMMARY_LEN = 'summary_len'
SEED = 42
LR = 0.001
TOKENIZER_PATH = os.path.join('.','models', 'tokenizer')
MODEL_PATH = os.path.join('models', 't5model.pth')
