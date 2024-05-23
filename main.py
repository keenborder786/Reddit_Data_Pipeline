import praw
reddit = praw.Reddit(
        client_id='ZzVY5KrsCcxcqeJVJr4YOQ',
        client_secret='CmOuJLlvJPI7cw_H2jJ6al2CmRn3SA',
        user_agent='extraction_by_keenborder'
    )
all_post_data = []
for post in reddit.subreddit('Langchain').top(time_filter="day"):
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
print(all_post_data[0]['post_content'])