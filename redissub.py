from redis import client

conn_pool = client.ConnectionPool()
sub = client.PubSub(conn_pool)

sub.subscribe('topic')
sub.subscribe('topic2')
for msg in sub.listen():
    print msg
