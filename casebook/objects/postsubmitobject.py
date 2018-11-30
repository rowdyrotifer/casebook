class PostSubmitObject:
    def __init__(self, **kwargs):
        self.title = kwargs['title']
        self.body = kwargs['body']
