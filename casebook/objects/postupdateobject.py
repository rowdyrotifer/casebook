class PostUpdateObject:
    def __init__(self, *args):
        self.id = args[0]['id']
        self.title = args[0]['title']
        self.body = args[0]['body']
