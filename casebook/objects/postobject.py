class PostObject:
    def __init__(self, input_tuple):
        self.id, self.username, self.time, self.title, self.body = input_tuple

    def to_dict(self):
        return {'id': self.id,
                'author_username': self.username,
                'time': self.time,
                'title': self.title,
                'body': self.body}
