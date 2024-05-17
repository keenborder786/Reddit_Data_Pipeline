import configparser
import os

parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), '../config/config.conf'))

SECRET = parser.get('reddit', 'reddit_secret_key')
CLIENT_ID = parser.get('reddit', 'reddit_client_id')
USER_AGENT=parser.get('reddit','user_agent')
SEARCH_QUERY=parser.get('reddit','search_query')
SPARK_MASTER = parser.get('spark', 'spark_master')

