from typing import Dict,List
from utils.constants import SPARK_MASTER,SECRET,CLIENT_ID,USER_AGENT,SEARCH_QUERY
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
    spark = SparkSession.builder.remote(f"sc://{master_name}:7077").getOrCreate()
    data = extract_reddit_post(client_id,client_secret,user_agent,search_query)
    spark.sql("""CREATE DATABASE IF NOT EXISTS reddit 
    """)
    spark.sql("""CREATE TABLE IF NOT EXISTS reddit.posts
                post_subreddit string,
                post_title string,
                post_content string,
                post_score string,
                post_id string,
                post_url string,
                post_author string,
              "created_at" timestamp    
    """)
    df = spark.sql('SELECT * FROM reddit.posts').show()
    return df

if __name__ == '__main__':
    spark_process_load_reddit_post(SPARK_MASTER,
                                   CLIENT_ID,
                                   SECRET,
                                   USER_AGENT,
                                   SEARCH_QUERY
                                   )
    


