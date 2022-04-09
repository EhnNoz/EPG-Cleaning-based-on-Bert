import re
from collections import Counter
from itertools import chain
from nltk.corpus import stopwords
from num2fawords import words
from parsivar import SpellCheck, Normalizer, FindStems, Tokenizer


class MainClean:
    """
    Input is DataFrame & Column Name
    Output is List of Clean Programs Name
    """

    def __init__(self, dataframe, column_name):
        self.pro_name = dataframe[column_name].values.tolist()

    def spell_check(self):
        spell_checker = SpellCheck()
        self.pro_name = list(map(lambda x: spell_checker.spell_corrector(x), self.pro_name))
        return self.pro_name

    def text_normalize(self):
        text_normalizer = Normalizer()
        self.pro_name = list(map(lambda x: text_normalizer.normalize(x), self.pro_name))
        return self.pro_name

    def remove_extra_words2(self):
        pattern01 = '\s+(قسمت)\s+(\d)'
        pattern02 = '\s+(قسمت)\s+(نخست|آخر|اول)'
        pattern03 = '\s+(قسمت)(\d)'
        self.pro_name = list(map(lambda x: re.sub(pattern01,'', x), self.pro_name))
        self.pro_name = list(map(lambda x: re.sub(pattern02, '', x), self.pro_name))
        self.pro_name = list(map(lambda x: re.sub(pattern03, '', x), self.pro_name))
        return self.pro_name

    def remove_extra_words(self, channel_name):
        # pattern = '\([^)]*\)'
        pattern01 = '(\(|")(\s+)(زنده|تکرار|باز پخش|بازپخش|نیمه اول|نیمه دوم|نیمه اول فوتبال|نیمه دوم فوتبال|کارشناسی)(\s+)(\)|")'
        pattern02 = '(-|_)(\s+)(زنده|تکرار|باز پخش|بازپخش|نیمه اول|نیمه دوم|نیمه اول فوتبال|نیمه دوم فوتبال|کارشناسی)$'
        pattern03 = '^(زنده|تکرار|باز پخش|بازپخش|نیمه اول|نیمه دوم|نیمه اول فوتبال|نیمه دوم فوتبال|کارشناسی)(\s+)(-|_)'
        pattern04 = '(^سریال|مجموعه تلویزیونی|مجموعه|سریال تلویزیونی|تلویزیونی|مسابقه|برنامه|تقدیم‌برنامه| فیلم |فیلم سینمایی|فیلم|سینمایی|سینمایی |مستند| مستند )(\s+)'
        pattern05 = '[^\w]'
        pattern06 = channel_name
        sub_list = list(map(lambda x: re.sub(pattern01, '', x), self.pro_name))
        sub_list = list(map(lambda x: re.sub(pattern02, '', x), sub_list))
        sub_list = list(map(lambda x: re.sub(pattern03, '', x), sub_list))
        sub_list = list(map(lambda x: re.sub(pattern04, '', x), sub_list))
        sub_list = list(map(lambda x: re.sub(pattern06, '', x), sub_list))
        self.pro_name = list(map(lambda x: re.sub(pattern05, ' ', x), sub_list))
        return self.pro_name


    def convert_number(self):
        def recognition(input):
            find_digit = re.findall('\d+', input)
            if find_digit:
                digit = find_digit[0]
                if len(input.split(' ')) != 1:
                    if int(digit) < 1001:
                        word_digit = ' ' + words(digit)
                        text = re.sub(digit, word_digit, input)
                    else:
                        text = re.sub(digit, digit, input)
                else:
                    word_digit = ' ' + words(digit)
                    text = re.sub(digit, word_digit, input)

                if len(find_digit) == 2:
                    digit = find_digit[1]
                    if int(digit) < 1001:
                        word_digit = ' ' + words(digit)
                        text = re.sub(digit, word_digit, text)
                    else:
                        text = re.sub(digit, digit, input)
            else:
                text = input
            return text
        self.pro_name = list(map(lambda x: recognition(x), self.pro_name))
        self.pro_name = list(map(lambda x: re.sub('یکهزار|یک هزار','هزار', x), self.pro_name))
        self.pro_name = list(map(lambda x: re.sub('یکصد|یک صد', 'صد', x), self.pro_name))
        return self.pro_name

    def remove_sign(self):
        pattern = r'@|"|/\|/|/_|:|\d+'
        self.pro_name = list(map(lambda x: re.sub(pattern, '', x), self.pro_name))
        return self.pro_name

    def remove_stopwords(self):
        def get_text(text):
            tokens = text.split()
            stop_words = set(stopwords.words('stp_wrd'))
            tokens = [w for w in tokens if not w in stop_words]
            text = ' '.join(tokens)
            return text
        self.pro_name = list(map(lambda x: get_text(x), self.pro_name))
        return self.pro_name

    def stems_word(self):
        stemmer = FindStems()
        def get_text(text):
            tokens = text.split()
            tokens = [stemmer.convert_to_stem(w) for w in tokens]
            text = ' '.join(tokens)
            return text
        self.pro_name = list(map(lambda x: get_text(x), self.pro_name))
        return self.pro_name

    def remove_bracket(self):
        def len_bracket(text):
            pattern = '\((.*?)\)'
            extract_str = re.findall(pattern, text)
            if extract_str:
                convert_str = (extract_str[0]).split(' ')
                len_str = len(convert_str)
            else:
                len_str = 5
            return len_str
        self.pro_name = list(map(lambda x: x if len_bracket(x) > 4 else re.sub('\(.*?\)', '', x), self.pro_name))
        return self.pro_name

    def output_show(self):
        return self.pro_name

    @staticmethod
    def count_name(rep_name):
        tk = Tokenizer()
        tk_list = list(map(lambda x: tk.tokenize_words(x), rep_name))
        tk_list = list(chain.from_iterable(tk_list))
        count_list = Counter(tk_list)
        count_dict = dict(count_list)
        return count_dict
        # e = mean(count_dict[k] for k in count_dict)

    @staticmethod
    def check_repeat(text, dct, low_limit):
        i = 0
        num_flag = 0
        check_list = []
        # print(text)
        while True:
            try:
                value = dct[text[i]]
            except IndexError:
                break
            # print([value, text[i]])
            check_list.append([value, text[i]])
            i = i + 1
        try:
            max_num, name = zip(*check_list)
            max_list = max(max_num)
            result = list(filter(lambda x: x[0] > low_limit * max_list, check_list))
            sec_1, sec_2 = zip(*result)
            sec_2 = ' '.join(sec_2)
            return sec_2
        except ValueError:
            return text

    @staticmethod
    def check_repeat_sentence(text, dct, prg_name):
        x_split = text.split(' ')
        i = 0
        while True:
            try:
                value = dct[x_split[i]]
                if value > 3:
                    try:
                        next_item = x_split[i + 1]
                        try:
                            next_item_item = x_split[i + 2]
                        except:
                            next_item_item = 'list_end'

                        pattern = '\s{var}\s|^{var}\s|\s{var}$'.format(var=next_item)
                        find_list = list(filter(lambda x: re.findall(pattern, x), prg_name))
                        split_list = list(map(lambda x: re.split(' ', x), find_list))
                        index_list = list(map(lambda x: x.index(next_item), split_list))

                        def find_next_item(text_list, index_num):
                            try:
                                out = text_list[index_num + 1]
                            except IndexError:
                                out = ''
                            return [out]

                        sim_list = list(map(lambda x: find_next_item(x[0], x[1]), zip(split_list, index_list)))
                        sim_list.append([next_item_item])

                        if len(set(map(tuple, sim_list))) == 1:
                            break
                        else:
                            return x_split[i]
                    except IndexError:
                        try:
                            pre_item = x_split[i - 1]
                            try:
                                pre_pre_item = x_split[i - 2]
                            except:
                                pre_pre_item = 'end_list'

                            pattern = '\s{var}\s|^{var}\s|\s{var}$'.format(var=pre_item)
                            find_list = list(filter(lambda x: re.findall(pattern, x), prg_name))
                            split_list = list(map(lambda x: re.split(' ', x), find_list))
                            index_list = list(map(lambda x: x.index(pre_item), split_list))

                            def find_pre_item(text_list, index_num):
                                try:
                                    out = text_list[index_num - 1]
                                except IndexError:
                                    out = ''
                                return [out]

                            sim_list = list(map(lambda x: find_pre_item(x[0], x[1]), zip(split_list, index_list)))
                            sim_list.append([pre_pre_item])

                            if len(set(map(tuple, sim_list))) == 1:
                                break
                            else:
                                return text
                        except IndexError:
                            break
                else:
                    i += 1
                    if i == len(text):
                        break
            except:
                i += 1
                if i == len(text):
                    break
        return text
