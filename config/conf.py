conf = {
    'articles': []
}

# data structure [{'filename', 'title', 'timestmap', 'tags', 'desc'}]

enviroment = {
    'prod': {
        'port': 8081,
        'level': "info",
        'debug': False
    },
    'dev': {
        'port': 8081,
        'level': "debug",
        'debug': True
    }
}
