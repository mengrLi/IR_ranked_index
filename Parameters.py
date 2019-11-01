class Document:

    def __init__(self, doc_id, doc_content):
        self.id = doc_id
        self.content = doc_content
        self.tokens = None
        self.doc_length = 0
        self.tf = {}


class Term:

    def __init__(self, name):
        self.name = name
        self.posting_list = []
        self.df = 0

    def create_posting_list(self, id):
        if id not in self.posting_list:
            self.posting_list.append(id)
            self.df = len(self.posting_list)
