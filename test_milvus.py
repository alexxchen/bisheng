from pymilvus import connections
connections.connect(
    alias='test',
    user='minoadmin',
    password='',
    host='127.0.0.1',
    port='19530'
)
print(connections.list_connections)