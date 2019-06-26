# encoding: utf-8

"""
@author: 王良
@license: Apache Licence
@contact: 744516468@qq.com
@file: worldcloud.py
@time: 2018/12/24 9:36
"""

from wordcloud import WordCloud,ImageColorGenerator
import jieba
import psycopg2
import numpy as np
from PIL import Image
import random
from PIL import ImageFilter
import datetime


hsl= [(0,0,100),(86,61,60),(186,79,72),(32,42,75),(55,53,69)]


def random_color_func(word=None, font_size=None, position=None,
                      orientation=None, font_path=None, random_state=None):
    value = hsl[random.randint(0, 4)]
    return "hsl({}, {}%, {}%)".format(value[0], value[1], value[2])


def stop_words(content):
    words_list = []
    word_generator = jieba.cut(content, cut_all=False)
    with open('file/stopwords_cn.txt', encoding='UTF-8') as f:
        stopwords = f.read().splitlines()
        f.close()
    for word in word_generator:
        if word.strip() not in stopwords:
            words_list.append(word)
    return ' '.join(words_list)


def setoutline(backImg, wcImg):
    backImg = backImg.filter(ImageFilter.CONTOUR)
    wcImg = Image.open(wcImg)
    L, H = backImg.size
    color_0 = backImg.getpixel((0, 0))
    # print(color_0)
    for h in range(H):
        for l in range(L):
            dot = (l, h)
            color_1 = backImg.getpixel(dot)
            if color_1 != color_0:
                # color_1 = color_1[:-1] + (0,)
                # print(color_1)
                wcImg.putpixel(dot, (59,163,251))
    return wcImg


font_path = 'file/simhei.TTF'
keywords = {}
start = '东坝社区“东坝社区”是北京东坝地区第一个微信公众平台，专注本地及周边新闻资讯，网罗吃喝玩乐信息，第一时间爆料你不知道的事儿！'
end = '东坝近期重要信息一览'
conn = psycopg2.connect(database="grid_yq", user="grid_yq", password="mapapp", host="192.168.46.237", port="5432")
cur = conn.cursor()
date = datetime.datetime.now()
days = (7, 30, 90, 365)
for day in days:
    sql = "select * from yq_hotnews where hot_date >='"+(date - datetime.timedelta(days=day)).strftime("%Y-%m-%d %H:%M:%S")+"'"
    print(sql)
    cur.execute(sql)
    content = ''
    for row in cur.fetchall():
        if row[5]:
            content += row[5]
        if row[6]:
            cityCases = row[6].split(',')
            for i in cityCases:
                keywords[i] = keywords[i] + 1 if i in keywords else 1

    content = content.replace('dongbacom', '')
    jieba.load_userdict('file/userdict.txt')
    text = stop_words(content)
    # print(text)
    # img = Image.open('file/back01.png')
    # img1 = getbackoutline(img)
    # background_Image = np.array(img)
    # img_colors = ImageColorGenerator(background_Image)
    stopwords = set('')
    wc = WordCloud(
        width=640,
        height=300,
        font_path=font_path,
        margin=10,
        # mask=background_Image,
        scale=1,
        max_words=500,
        min_font_size=8,
        stopwords=stopwords,
        random_state=5,
        background_color='#031139',
        # background_color=None,
        max_font_size=54,
        colormap='hsv',
        # mode='RGBA'
    )
    process_word = WordCloud.process_text(wc, text)
    frequencies = dict(process_word.items())
    for i in keywords:
        if i in process_word:
            process_word[i] = 25 + process_word[i] * keywords[i]
    # 处理事件关键词
    sort = sorted(process_word.items(), key=lambda e: e[1], reverse=True)
    process_word = dict(sort)
    if len(process_word):
        print(process_word)
        wc.generate_from_frequencies(process_word)
        for i in range(10):
            filename = 'result/'+str(day)+'东坝词云'+str(i+1)+'.png'
            wc.recolor(color_func=random_color_func)
            wc.to_file(filename)
        # wcImg = setoutline(img, filename)
        # wcImg.save('result/' + str(day) + '东坝词云-加边线' + str((i + 1)) + '.png')
    # img = Image.open(filename)
    # img = img.convert('RGBA')
    # img1 = img1.convert('RGBA')
    # r, g, b, alpha = img1.split()
    # alpha = alpha.point(lambda i: i > 0 and 255)
    # image = img.copy()
    # image.paste(img1, (0,0), alpha)
    # # img = Image.composite(img1, img2, alpha)
    # # image.show()
# cmaps = ['viridis', 'plasma', 'inferno', 'magma',
#              'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
#              'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
#              'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
#              'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
#              'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
#              'hot', 'afmhot', 'gist_heat', 'copper',
#              'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
#              'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic',
#              'Pastel1', 'Pastel2', 'Paired', 'Accent',
#              'Dark2', 'Set1', 'Set2', 'Set3',
#              'tab10', 'tab20', 'tab20b', 'tab20c',
#              'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
#              'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv',
#              'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']
# for i in range(len(cmaps)):
#     filename = 'result/东坝词云'+str((i+1))+'.png'
#     wc.recolor(colormap=cmaps[i])
#     wc.to_file(filename)
    # img1 = Image.open(filename)
    # img1 = img1.convert('RGBA')
    # img2 = Image.open("file/back2.png ")
    # img2 = img2.convert('RGBA')
    # r, g, b, alpha = img1.split()
    # alpha = alpha.point(lambda i: i > 0 and 255)
    # image = img2.copy()
    # image.paste(img1, (30,65), alpha)
    # # img = Image.composite(img1, img2, alpha)
    # # image.show()
    # image.save('result/东坝词云-效果'+str((i+1))+'.png')

