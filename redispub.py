from redis import client

r = client.Redis()
r.publish('topic', 'message body')
r.publish('topic2', 'message body')