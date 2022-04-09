import collections
import re


class ExceptionsProgram:

    def __init__(self, dataframe, name_column, time_column, opt_column):
        self.input = list(zip(dataframe[name_column], dataframe[time_column], dataframe[opt_column]))

    def news(self):
        def spliter(text, time, opt):
            if re.findall(r'خبر|اخبار', text):
                # print(text)
                if re.findall(r'\d\d|\d', text):
                    play_time = re.findall(r'\d\d|\d', text)[0]
                    # print(play_time)
                    return [text, play_time]
                else:
                    if opt != 'تلوبیون':
                        return [text, time]
                    else:
                        return False
            else:
                return False

        extract = list(map(lambda x: spliter(x[0], x[1], x[2]), self.input))
        output = list(filter(lambda x: x != False, extract))
        return output
        # extract = list(filter(lambda x: re.findall(r'خبر|اخبار', x[0]), self.input))
        # time = list(map(lambda x: re.findall(r'\d\d|\d', x[0])[0] if re.findall(r'\d\d|\d', x[0]) and x[2] == 'تلوبیون' else 'Null' , extract))
        # output = list(map(lambda x: ((x[0])[0], x[1]) if x[1] != 'Null' else x[0], zip(extract,time)))
        # # output = list(map(lambda x: x, zip(extract, time)))
        # return output

    @staticmethod
    def create_dict(list_dct):
        result = collections.defaultdict(list)
        for elem in list_dct:
            key, value = next(iter(elem.items()))  # best way to extract data from your strange format
            if value not in result[key]:
                result[key].append(value)
        result = [dict(result)]
        return result

    @staticmethod
    def check_pattern(x, dct, patten):
        if re.findall(patten, x):
            for key, value in dct[0].items():
                try:
                    exit_x = value.index(x)
                    return min(value, key=len)
                except:
                    pass
