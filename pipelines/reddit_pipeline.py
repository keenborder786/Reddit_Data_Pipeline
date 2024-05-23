from typing import Dict,List
import sys
sys.path.insert(0,'/opt/airflow')
from utils.constants import SPARK_MASTER,SECRET,CLIENT_ID,USER_AGENT,SEARCH_QUERY
from datetime import datetime
import praw
from pyspark.sql import SparkSession

def extract_reddit_post(client_id:str,client_secret:str,user_agent:str,
                    search_query:str) -> List[Dict[str,str]]:
    reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
    all_post_data = []
    for post in reddit.subreddit(search_query).top(time_filter="day"):
        metadata = {
            "post_subreddit": post.subreddit_name_prefixed,
            "post_title": post.title,
            "post_content":post.selftext,
            "post_score": post.score,
            "post_id": post.id,
            "post_url": post.url,
            "post_author": post.author,
        }
        all_post_data.append(metadata)
    return all_post_data


def spark_process_load_reddit_post(master_name:str,
                                   client_id:str,
                                   client_secret:str,
                                   user_agent:str,
                                   search_query:str):
    spark = SparkSession.builder.master(f"spark://{master_name}").getOrCreate()
    data = extract_reddit_post(client_id,client_secret,user_agent,search_query)
    spark.sql("""CREATE DATABASE IF NOT EXISTS reddit 
    """)
    spark.sql("""CREATE TABLE IF NOT EXISTS reddit.posts (
                post_subreddit STRING,
                post_title STRING,
                post_content STRING,
                post_score STRING,
                post_id STRING,
                post_url STRING,
                post_author STRING,
                created_at TIMESTAMP
            )""")
    df = spark.sql('SELECT * FROM reddit.posts').show()
    for instance in data:
        spark.sql(f"""
        INSERT INTO reddit.posts 
        (post_subreddit, post_title, post_content, post_score, post_id, post_url, post_author, created_at)
        VALUES (
        '{instance['post_subreddit']}', 
        '{instance['post_title']}', 
        '{instance['post_content']}', 
        {instance['post_score']}, 
        '{instance['post_id']}',
        '{instance['post_url']}', 
        '{instance['post_author']}',
        TO_TIMESTAMP('{datetime.now()}','yyyy-MM-dd HH:mm:ss.SSSSSS')
        )
        """)
    df = spark.sql('SELECT * FROM reddit.posts LIMIT 1').show()
    return df

if __name__ == '__main__':
    spark_process_load_reddit_post(SPARK_MASTER,
                                   CLIENT_ID,
                                   SECRET,
                                   USER_AGENT,
                                   SEARCH_QUERY
                                   )
    


