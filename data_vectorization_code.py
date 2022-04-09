

class VectorizeText:
    '''
    Input is List of Sentences and Model
    Output is List of Vector Arrays
    '''

    def __new__(cls, clean_list, model, *args, **kwargs):
        if isinstance(clean_list, list):
            return super().__new__(cls, *args, **kwargs)
        else:
            return None

    def __init__(self, clean_list, model):
        self.clean_list = clean_list
        self.model = model

    def bert_encoder_text(self):
        encoded_text = self.model.encode(self.clean_list)
        return encoded_text
