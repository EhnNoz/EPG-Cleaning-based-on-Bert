from collections import Counter


class SubstitutionText:
    '''
    Inputs are:
    initial_list = list
    secondary_list = tuple of Recommended name and Value of Similarity
    '''

    def __new__(cls, initial_list, secondary_list, *args, **kwargs):
        if isinstance(secondary_list[0], tuple):
            return super().__new__(cls,*args, **kwargs)
        return None

    def __init__(self, initial_list, secondary_list):
        self.initial_list = initial_list
        self.initial_list_copy = initial_list
        self.secondary_list = secondary_list
        self.counter_dict = dict(Counter(self.initial_list))
        self.recom_list = list(map(lambda x: eval(str(x))[1], self.secondary_list))


    def substitution(self):
        for index, item in enumerate(self.initial_list):
            item = self.initial_list[index]
            com_name = self.recom_list[index]
            rep_item = self.counter_dict.get(str(item))
            if rep_item is None:
                rep_item = 1
            rep_com = self.counter_dict.get(str(com_name))
            if rep_com is None:
                rep_com = 1
            if rep_item > rep_com:
                out_name = item
                self.initial_list = list(map(lambda x: x.replace(com_name, out_name), self.initial_list))
                self.recom_list = list(map(lambda x: x.replace(com_name, out_name), self.recom_list))
            else:
                out_name = com_name
                self.initial_list = list(map(lambda x: x.replace(item, out_name), self.initial_list))
                self.recom_list = list(map(lambda x: x.replace(item, out_name), self.recom_list))

        return self.recom_list
