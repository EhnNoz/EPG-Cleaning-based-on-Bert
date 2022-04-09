import re
from threading import Thread
import pandas as pd
from collections import Counter
from parsivar import Tokenizer
from sentence_transformers import SentenceTransformer
from data_cleaning_code import MainClean
from data_similarity_code import SimilarityVector
from data_substitution_code import SubstitutionText
from data_vectorization_code import VectorizeText
from exceptions_program_code import ExceptionsProgram
from num2fawords import words, ordinal_words

def executive_clean(main_file, target_channel, fa_target_channel, en_target_channel, target_month):
    df = pd.read_csv('{}'.format(main_file), index_col=False)
    filter_df = df[df['نام شبکه'] == '{}'.format(target_channel)]
    filter_df = filter_df[filter_df['ردیف'] == target_month]
    # filter_df = pd.read_excel(r'F:\sourcecode\CleanEpg\check19.xlsx', index_col=False)
    # model= SentenceTransformer(r'F:\sourcecode\CleanEpg\all-mpnet-base-v2')
    model = SentenceTransformer('F:\sourcecode\CleanEpg\distilbert-base-nli-mean-tokens')
    column_name = 'نام برنامه اولیه'
    column_hour = 'ساعت'
    column_opt = 'اپراتور'
    number_of_repetitions = 3
    High_limit_sim = 1.05
    low_limit_sim = 0.9
    low_limit_intersection_sim = 0.25
    channel_name = '{x}'.format(x=fa_target_channel)
    tk = Tokenizer()

    stp_wrd_df = pd.read_excel('stop_word2.xlsx', index_col=False)
    stp_wrd_filter = stp_wrd_df[stp_wrd_df['ch'] == '{}'.format(target_channel)]
    item_name = stp_wrd_filter['name'].tolist()
    with open(r'C:\Users\User\AppData\Roaming\nltk_data\corpora\stopwords\stp_wrd', 'w', encoding='utf8') as f:
        for item in item_name:
            f.write(item + '\n')

    for i in range(0,number_of_repetitions):
        call_main_clean = MainClean(filter_df, column_name)
        # call_main_clean = MainClean(filter_df, 'cls2' )
        # call_spell_check = call_main_clean.spell_check()
        get_text_normalize = call_main_clean.text_normalize()
        get_remove_bracket = call_main_clean.remove_bracket()
        get_remove_bracket = call_main_clean.remove_extra_words2()
        get_convert_number = call_main_clean.convert_number()
        get_text_normalize = call_main_clean.text_normalize()
        get_remove_vain = call_main_clean.remove_extra_words(channel_name)
        get_remove_sign = call_main_clean.remove_sign()
        get_text_normalize = call_main_clean.text_normalize()
        get_remove_stopwords = call_main_clean.remove_stopwords()
        # get_stems_word = call_main_clean.stems_word()
        # get_text_normalize = call_main_clean.text_normalize()
        get_output_show = call_main_clean.output_show()

        get_output_show_count = Counter(get_output_show)
        get_output_show_kw = list(map(lambda x: MainClean.check_repeat_sentence(x, get_output_show_count, get_output_show), get_output_show))
        get_count_name = MainClean.count_name(get_output_show_kw)
        tokenize_output_show = list(map(lambda x: tk.tokenize_words(x), get_output_show_kw))
        get_check_repeat = list(map(lambda x: MainClean.check_repeat(x, get_count_name, 0.1/(i+1)), tokenize_output_show))

        get_check_repeat = list(
            map(lambda x: x[0] if x[0] else x[1], zip(get_check_repeat, filter_df['نام برنامه اولیه'].tolist())))

        call_vectorize_text = VectorizeText(get_check_repeat, model)
        get_encoder_text = call_vectorize_text.bert_encoder_text()

        call_similarity_vector = SimilarityVector(get_encoder_text)
        get_cosine_sim = call_similarity_vector.cosine_sim()
        get_value_filter = list(map(lambda x: SimilarityVector.value_filter(low_limit_sim, High_limit_sim, x, get_output_show), get_cosine_sim))
        get_jaccard_sim = list(map(lambda x: list(map(lambda y: SimilarityVector.jaccard_set(y[1], x[-1][1]), x)), get_value_filter))
        get_best_choice = list(map(lambda x: SimilarityVector.check_intersection(x[0], x[1], low_limit_intersection_sim), zip(get_jaccard_sim, get_value_filter)))

        call_substitution_text = SubstitutionText(get_output_show, get_best_choice)
        get_recom_list = call_substitution_text.substitution()
        filter_df['get_recom_list']=get_recom_list
        column_name = 'get_recom_list'

    column_name = 'نام برنامه اولیه'
    call_exceptions_program = ExceptionsProgram(filter_df, column_name, column_hour, column_opt)
    get_news = call_exceptions_program.news()
    # print(get_news)
    # get_news = set(get_news)
    get_news_dict = list(map(lambda x: {str(x[1]):str(x[0])}, get_news))
    get_news_dict = ExceptionsProgram.create_dict(get_news_dict)
    get_news_list = filter_df['نام برنامه اولیه'].apply(lambda x: ExceptionsProgram.check_pattern(x, get_news_dict,'خبر|اخبار'))


    final_value = list(map(lambda x: x[0] if x[0] else x[1], zip(get_news_list, get_recom_list)))
    final_value = list(
        map(lambda x: x[0] if x[0] else x[1], zip(final_value, filter_df['نام برنامه اولیه'].tolist())))

    filter_df['final_value']=final_value
    filter_df['get_value_filter'] = get_value_filter
    filter_df['get_jaccard_sim'] = get_jaccard_sim
    filter_df['get_check_repeat'] = get_check_repeat
    filter_df.to_excel('check__{x}_{y}.xlsx'.format(x=target_month, y=en_target_channel))


if __name__ == "__main__":
    # df_tmp = pd.read_csv(r'F:\tmp\sarasari_1.csv', index_col= False)
    # set_ch_name = set(df_tmp['نام شبکه'])
    set_ch_name = {'شبکه 3','شبکه 1'}
    # set_ch_name = {'تماشا'}
    i=0
    threads = []
    for ch_name in set_ch_name:
        print(ch_name)
        try:
            fa_ch_name = lambda x: ' '.join([x.split(' ')[0], words(re.findall('\d', x)[0])])
        except IndexError:
            fa_ch_name = 'شبکه' + ' ' + ch_name

        i = i+1
        # i = 41
        t1 = Thread(target=executive_clean, args=(r'F:\tmp\sarasari_1.csv', ch_name, fa_ch_name, 'Ch{}'.format(i), 42))
        t1.start()
        if i > 6:
            break
    # creating thread
    # t1 = Thread(target=executive_clean, args=(r'F:\tmp\sarasari_1.csv', 'شبکه 1', 'شبکه یک','ChOne', 42))
    # t2 = Thread(target=executive_clean, args=(r'F:\tmp\sarasari_1.csv', 'شبکه 2', 'شبکه دو', 'ChTwo', 42))
    # t3 = Thread(target=executive_clean, args=(r'F:\tmp\sarasari_1.csv', 'شبکه 3', 'شبکه سه', 'ChThree', 42))
    # t4 = Thread(target=executive_clean, args=(r'F:\tmp\sarasari_1.csv', 'شبکه 4', 'شبکه چهار', 'ChFour', 42))
    # t5 = Thread(target=executive_clean, args=(r'F:\tmp\sarasari_1.csv', 'شبکه 5', 'شبکه پنج', 'ChFive', 42))
    # t6 = Thread(target=executive_clean, args=(r'F:\tmp\sarasari_1.csv', 'خبر', 'شبکه خبر', 'ChKhabar', 42))
    # t7 = Thread(target=executive_clean, args=(r'F:\tmp\sarasari_1.csv', 'ورزش', 'شبکه ورزش', 'ChVarzesh', 42))
    # t8 = Thread(target=executive_clean, args=(r'F:\tmp\sarasari_1.csv', 'امید', 'شبکه امید', 'ChOmid', 42))
    #
    # t9 = Thread(target=executive_clean, args=(r'F:\tmp\sarasari_1.csv', 'شبکه 1', 'شبکه یک','ChOne', 42))
    # t10 = Thread(target=executive_clean, args=(r'F:\tmp\sarasari_1.csv', 'شبکه 2', 'شبکه دو', 'ChTwo', 42))
    # t11 = Thread(target=executive_clean, args=(r'F:\tmp\sarasari_1.csv', 'شبکه 3', 'شبکه سه', 'ChThree', 42))
    # t12 = Thread(target=executive_clean, args=(r'F:\tmp\sarasari_1.csv', 'شبکه 4', 'شبکه چهار', 'ChFour', 42))
    # t13 = Thread(target=executive_clean, args=(r'F:\tmp\sarasari_1.csv', 'شبکه 5', 'شبکه پنج', 'ChFive', 42))
    # t14 = Thread(target=executive_clean, args=(r'F:\tmp\sarasari_1.csv', 'خبر', 'شبکه خبر', 'ChKhabar', 42))
    # t15 = Thread(target=executive_clean, args=(r'F:\tmp\sarasari_1.csv', 'ورزش', 'شبکه ورزش', 'ChVarzesh', 42))
    # t16 = Thread(target=executive_clean, args=(r'F:\tmp\sarasari_1.csv', 'امید', 'شبکه امید', 'ChOmid', 42))
    #
    #
    # t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
    # t5.start()
    # t6.start()
    # t7.start()
    # t8.start()
# , 'ورزش', 'پرس تی وی', 'شما', 'پویا'