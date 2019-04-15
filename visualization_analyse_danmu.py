# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.misc import imread
from wordcloud import WordCloud
import jieba
import jieba.posseg as pseg
import math
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def danmu_compress_plot(data, num):
    plt.cla()
    plt.xlabel(u"视频时间", fontproperties='SimHei')
    plt.ylabel(u"弹幕量", fontproperties='SimHei')
    plt.title(u'类别{}_时间轴弹幕变化'.format(num), fontproperties='SimHei')

    keys = [item for item in data.index]

    values = [item for item in data.dtTime]

    """弹幕密度折线图
    """
    plt.plot(keys, values)
    plt.show()


def danmu_compress(data):
    df = data.drop_duplicates()
    dd = df.copy()
    dd['dtTime_new'] = [math.floor(item) for item in dd.dtTime]
    dc = dd.groupby('dtTime_new').count()
    result = dc.sort_index()
    print(result)
    return (result)


def extract_words(data, num):

    df = data.drop_duplicates()
    dd = df.copy()
    message_list = [str(item) for item in dd.message]

    stop_words = set(line.strip()
                     for line in open('stopwords.txt', encoding='utf-8'))

    newslist = []
    for subject in message_list:
        if subject.isspace():
            continue
        # segment words line by line
        word_list = pseg.cut(subject)
        for word, flag in word_list:
            if not word in stop_words and flag == 'n':
                newslist.append(word)

    d = os.path.dirname(__file__)
    mask_image = imread(os.path.join(d, "qiaodan.png"))
    content = ' '.join(newslist)
    wordcloud = WordCloud(font_path='simhei.ttf', background_color="grey",
                          mask=mask_image, max_words=40).generate(content)

    # Display the generated image:
    file_name = u"类别{}_热词云.jpg".format(num)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title(file_name, fontproperties='SimHei')
    wordcloud.to_file(file_name)
    plt.show()
    plt.cla()
    plt.close()


def static_danmu_length(data):
    df = data.drop_duplicates()
    dd = df.copy()
    dd['message_len'] = [len(str(item)) for item in df.message]  # 统计每条弹幕的长度
    d1 = dd.loc[:, ['userID', 'message', 'message_len', 'episode']]
    dr = d1.copy()
    return (dr)


def every_episode_usersort(data):
    df = data.drop_duplicates()
    dd = df.groupby("userID").count()
    user_sort = dd.sort_values(
        by='episode', ascending=False).loc[:, ['episode']]
    return (user_sort)


def every_episode_user(data):
    '''共有多少用户发弹幕
    '''
    df = data.drop_duplicates()
    dd = df.groupby("userID").count()
    user_sum = len(dd)
    return (user_sum)


def every_episode_comment(data):
    '''共有多少弹幕发出
    '''
    df = data.drop_duplicates()
    danmu_sum = len(df)
    return (danmu_sum)


def top_user_danmu(data):
    plt.cla()
    ing = range(5)
    x = data.head(5).episode.index
    y = data.head(5).episode.values
    plt.xticks(ing, x, rotation=30)
    plt.xlabel(u"用户ID", fontproperties='SimHei')
    plt.ylabel(u"发弹幕数量", fontproperties='SimHei')
    plt.title(u"发弹幕数top5用户", fontproperties='SimHei')
    plt.bar(ing, y)
    plt.show()


def every_episode_comment_change(episode_comment_dic):
    plt.cla()
    ing = range(2)
    x = ["剧情向",  "非剧情向"]
    plt.xticks(ing, x, rotation=30)
    plt.xlabel(u"电影", fontproperties='SimHei')
    plt.ylabel(u"弹幕量", fontproperties='SimHei')
    plt.title(u'每类弹幕总量变化', fontproperties='SimHei')
    keys = range(1, len(episode_comment_dic)+1)
    values = []
    for i in keys:
        values.append(episode_comment_dic[i])

    """每类弹幕总量的分布图
    """
    plt.bar(ing, values)
    plt.show()


def every_episode_danmu_pie(d_tmp, num):

    a1 = float(len(d_tmp[(d_tmp.episode >= 1) & (d_tmp.episode <= 2)]))
    a2 = len(d_tmp[(d_tmp.episode >= 3) & (d_tmp.episode <= 8)])
    a3 = len(d_tmp[(d_tmp.episode >= 9) & (d_tmp.episode <= 20)])
    a4 = len(d_tmp[(d_tmp.episode >= 21)])

    s = a1 + a2 + a3 + a4
    s = float(s)
    li = [a1, a2, a3, a4]
    xp = []
    for i in li:
        i = float(i)
        if i <= 0:
            t = 0
            xp.append(t)
        else:
            t = (i/s*100)
            xp.append(t)

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    plt.figure(figsize=(6, 9))
    labels = [u'1-2条', u'3-8条', u'9-20条', u'21条以上']
    sizes = xp
    colors = ['red', 'yellow', 'gray', 'lightskyblue']
    explodes = [0, 0, 0, 0.6]

    plt.axis('equal')
    plt.title(u'类别{}_用户发送弹幕数量百分比分布图'.format(num))
    plt.pie(sizes,  labels=labels, explode=explodes, colors=colors, labeldistance=0.5,
            autopct='%2.2f%%', startangle=90, pctdistance=0.8)

    plt.show()
    plt.close()


def danmu_length_pie(d_tmp, num):
    a1 = float(
        len(d_tmp[(d_tmp.message_len >= 1) & (d_tmp.message_len <= 15)]))
    a2 = float(
        len(d_tmp[(d_tmp.message_len >= 16) & (d_tmp.message_len <= 30)]))
    a3 = float(
        len(d_tmp[(d_tmp.message_len >= 31) & (d_tmp.message_len <= 45)]))
    a4 = float(len(d_tmp[(d_tmp.message_len >= 46)]))
    s = a1 + a2 + a3 + a4
    s = float(s)
    li = [a1, a2, a3, a4]
    xp = []
    for i in li:
        i = float(i)
        if i <= 0:
            t = 0
            xp.append(t)
        else:
            t = (i/s*100)
            xp.append(t)

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    plt.figure(figsize=(6, 9))
    labels = [u'1-5个', u'6-10个', u'11-15个', u'16个以上']
    sizes = xp
    colors = ['red', 'yellow', 'gray', 'lightskyblue']
    explodes = [0, 0, 0, 0.09]
    plt.axis('equal')
    plt.title(u'类别{}_用户发送弹幕长度百分比分布图'.format(num))
    plt.pie(sizes,  labels=labels, colors=colors, explode=explodes, labeldistance=0.5,
            autopct='%2.2f%%', startangle=90, pctdistance=0.8)

    plt.show()
    plt.close()


# 秒转换成时间
def sec_to_str(seconds):
    seconds = eval(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    length_time = "%02d:%02d:%02d" % (h, m, s)
    return (length_time)


if __name__ == "__main__":

    path = os.getcwd()
    path_list = []

    for i in range(1, 2):
        path_list.append(path + "/danmu{}.csv".format(i))

    episode_comment_dic = {}
    user_sum_dic = {}
    user_sort_dic = {}
    danmu_length_dic = {}
    danmu_compress_dic = {}
    # reyun_data_dic = {}
    for item in path_list:
        '''读取csv数据源文件，每一类的弹幕都保存在一个csv文件
        '''
        data = pd.read_csv(item.strip(), encoding='utf-8')

        '''统计每一类弹幕总量，保存在字典：{1：323233， 2：212121， .......}
        '''
        episode_comment_dic[data.loc[1, 'episode']
                            ] = every_episode_comment(data)

        '''统计每一类，共有多少用户发了弹幕，保存在字典：{1：3737， 2：34234，......}
        '''
        user_sum_dic[data.loc[1, 'episode']] = every_episode_user(data)

        '''统计每一类的弹幕数量，依据弹幕数量，把用户排序，每类排序后的结果是一个DataFrame,
           user_sort_dic = {1: DataFrame1, 2:DataFrame2, ......, 25: DataFrame25}
        '''
        user_sort_dic[data.loc[1, 'episode']] = every_episode_usersort(data)

        '''统计发送弹幕的字符串长度
        '''
        danmu_length_dic[data.loc[1, 'episode']] = static_danmu_length(data)

        '''统计每类的分词，热词，词云
        '''
        # reyun_data_dic[data.loc[1, 'episode']] = data.copy()

        '''统计每类的弹幕量，电影里的每一秒的弹幕数量，弹幕密度
        '''
        danmu_compress_dic[data.loc[1, 'episode']] = danmu_compress(data)

        del data

    print("弹幕总数")
    print(episode_comment_dic)
    print("用户人数")
    print(user_sum_dic)
    print("用户发送弹幕的数量统计")
    print(user_sort_dic)
    print("用户发送弹幕的长度统计")
    print(danmu_length_dic)
    print("每秒发送弹幕的精度统计")
    print(danmu_compress_dic)

    '''把经过排序统计处理后的所有DataFrame 进行concat。然后就可以统计所有用户
       发送弹幕的数量。最后对用户排序。最终结果：
       d4_alldanmu_sort 是一个DataFrame 变量，将用户按弹幕数，降序排列。
    '''
    d3_all_user = (pd.concat([item for k, item in user_sort_dic.items()]))
    d3_all_user['user'] = d3_all_user.index
    aSer = d3_all_user.groupby('userID').episode.sum()
    d4_alldanmu_sort = pd.DataFrame(aSer).sort_values(
        by='episode', ascending=False)

    # '''绘制折线图：每类弹幕总数
    # '''
    # every_episode_comment_change(episode_comment_dic)

    '''绘制柱状图：发弹幕数量最多的5个用户
    '''
    top_user_danmu(d4_alldanmu_sort)

    '''用户发送弹幕数量的百分比分布图
    '''
    for i in range(1, len(user_sort_dic)+1):
        d_tmp = user_sort_dic[i]
        every_episode_danmu_pie(d_tmp, i)
        del d_tmp

    '''用户发送弹幕的长度分布百分比
    '''
    for i in range(1, len(user_sort_dic)+1):
        d_tmp = danmu_length_dic[i]
        danmu_length_pie(d_tmp, i)
        del d_tmp

    '''分析弹幕密度
    '''
    now_danmu_list = []

    for i in range(1, 2):
        now_danmu_list.append(path + "/danmu{}.csv".format(i))

    danmu_compress_dic = {}
    for item in now_danmu_list:
        data = pd.read_csv(item.strip(), encoding='utf-8')
        danmu_compress_dic[data.loc[1, 'episode']] = danmu_compress(data)

    for num, data in danmu_compress_dic.items():
        danmu_compress_plot(data, num)

    """绘制热词云图
    """
    # for num, data in reyun_data_dic.items():
    #     extract_words(data, num)
