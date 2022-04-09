import re
from sklearn.metrics.pairwise import cosine_similarity


class SimilarityVector:
    '''
    Input is 2D List of List of Vector Arrays
    Output of cosine_sim def is 2D List of Simalarity Values
    Output of value_filter def is Maximum Cosine Similarity
    Output of jaccard_set def is Jaccard Similarity
    '''

    def __init__(self, vector_list):
        self.vector_list = vector_list

    def cosine_sim(self):
        calc_cosine = list(map(lambda x: (cosine_similarity([x], self.vector_list[0:])).tolist()[0], self.vector_list))
        return calc_cosine

    @staticmethod
    def value_filter(low, high, vector_list, com_list):
        sticky_name = set(map(tuple, zip(vector_list, com_list)))
        separation_name = list(filter(lambda x: low < x[0] < high, sticky_name))
        sort_name = sorted(separation_name, key= lambda x:x[0])
        return sort_name


    @staticmethod
    def jaccard_set(list1, list2):
        li1 = re.sub(' ','', list1)
        li2 = re.sub(' ','', list2)
        intersection = len(list(set(li1).intersection(li2)))
        union = (len(set(li1)) + len(set(li2))) - intersection
        try:
            result = float(intersection) / union
        except ZeroDivisionError:
            result = 0
        if result == 1:
            return result
        li1 = list1.split(' ')
        li2 = list2.split(' ')
        intersection = len(list(set(li1).intersection(li2)))
        union = (len(set(li1)) + len(set(li2))) - intersection
        result = float(intersection) / union
        if union <= 4:
            if intersection:
                common = list(set(li1).intersection(li2))[-1]
                index_num_1 = li1.index(common)
                index_num_2 = li2.index(common)
                # print(index_num_2)
                # print(index_num_1)
                if index_num_1 == 0 and index_num_2 == 0:
                    # print(result)
                    return result
                else:
                    return result / 2
        return result

    @staticmethod
    def check_intersection(lista, listb, bound):
        if len(lista) > 1:
            i = 1
            while True:
                i = i + 1
                if lista[-i] >= bound:
                    return listb[-i]
                    break
                elif len(lista) == i:
                    return listb[-1]
                    break
        return listb[-1]
