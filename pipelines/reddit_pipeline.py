from typing import Tuple,List
import sys
sys.path.insert(0,'/opt/airflow')
from utils.constants import SPARK_MASTER,SECRET,CLIENT_ID,USER_AGENT,SEARCH_QUERY
from datetime import datetime
import praw
from pyspark.sql import SparkSession

def extract_reddit_post(client_id:str,client_secret:str,user_agent:str,
                    search_query:str) -> List[Tuple[str]]:
    reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
    all_post_data = []
    for post in reddit.subreddit(search_query).top(time_filter="day"):
        all_post_data.append((post.subreddit_name_prefixed,
                              post.title,
                              post.selftext,
                              str(post.score),
                              post.id,
                              post.url,
                              str(post.author),
                              datetime.now()))
    return all_post_data


def spark_process_load_reddit_post(master_name:str,
                                   client_id:str,
                                   client_secret:str,
                                   user_agent:str,
                                   search_query:str):
    spark = SparkSession.builder.master(f"spark://{master_name}").getOrCreate()
    data = extract_reddit_post(client_id,client_secret,user_agent,search_query)
    spark.sql("""CREATE DATABASE IF NOT EXISTS reddit""")
    spark.sql("""CREATE TABLE IF NOT EXISTS reddit.posts (
                post_subreddit STRING,
                post_title STRING,
                post_content STRING,
                post_score STRING,
                post_id STRING,
                post_url STRING,
                post_author STRING,
                created_at TIMESTAMP
            )
            USING iceberg
            PARTITIONED BY (days(created_at))
            """)
    spark.sql('SELECT * FROM reddit.posts LIMIT 1').show()
    schema = spark.table("reddit.posts").schema
    df = spark.createDataFrame(data, schema)
    df.writeTo("reddit.posts").append()
    return

if __name__ == '__main__':
    spark_process_load_reddit_post(SPARK_MASTER,
                                   CLIENT_ID,
                                   SECRET,
                                   USER_AGENT,
                                   SEARCH_QUERY
                                   )
    


