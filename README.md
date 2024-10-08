# bijous

寻找文本中的 bijous，包括：新词发现、同义词分析、语义搜索、命名实体识别、关系与事件提取、文本自动摘要等。

## 新词发现

使用 `bijous.extractors.oov`：

```python
file = '/data/comments.txt'

TOP = 10000
MAX_LEN = 5
MIN_FREQ = 10
WITH_SCORE = True

extracted = extract_words(file, TOP, max_len=MAX_LEN, min_count=MIN_FREQ, with_score=WITH_SCORE)
print(len(extracted))

for k, score in extracted:
    if is_in_jieba(k):
        continue
    print(k, score)
```

去掉已知的英文词及结巴词典中的词后，前 200 个词大概是：

```吐槽, 闺蜜, 寺山修司, 蔷薇岛屿, 波洛, 冯唐, 琵琶鼠, 杨德昌, 闰土, 囧叔, 柯南, 宋清佑, 炸牡蛎, 赖声川, 施小炜, 刘墉, 刘瑜, 傲娇, 李敖, 杰姬, 丁丁哥哥, 马普尔小姐, 洪水勐兽, 林夕, 坑爹, 孟孟, 郭德纲, 模煳, XX, 装逼, 刘五洲, 珊珊, 抖机灵, 张嘉佳, 陆子野, 傻逼, 牛逼, 毒舌, 涨姿势, 熊培云, APP, 暴风雪山庄, 炒饼, 脑洞, 熊逸, 签售, 诺奖, 微博, 康永哥, 萌萌哒, 韩寒, 雾霾, 王朔, 李海鹏, 唿吸, ING, 林内特, 村上君, 琳内特, 臭牛逼, 《常识》, 安妮宝贝, QAQ, 卖萌, 刘茵茵, 脑残粉, 海豹油, 董桥, 语文老师, 《我执》, 梁文道, 《读者》, YY, 西蒙, 超级马拉松, 嵴背发凉, 柯南道尔, 靠谱, blog, app, 煳涂, 独唱团, 带着, 梁左, 《三重门》, 白富美, 玛吉, 康永, 罗杰疑案, 唿吁, 臭贫, 挪威的森林, 量子物理, 拧巴, 迷迷煳煳, 潘恩, 梅根, 爷爷的塔吊, 腰封, 毛姆, 炒饼公主, 兜兜转转, 东野圭吾, 畅快淋漓, 打发时间, 凑字数, 孤岛模式, 蛋疼, 并没有, 尼罗河惨案, 蔡崇达, 凯撒沙拉, 单向街, 马家辉, 温水煮青蛙, 《呐喊》, 恋恋风尘, 玄幻, 瞎编乱造, 张晓晗, 逛书店, 精神病患者, 快手刘五洲, 东方列车, 碎碎念, 渣男, 挪威森林, 放在床头, 吴念真, 董青青, 笑出声, 迅哥儿, 韩三篇, 剧透, 公众号, 细思极恐, 接地气, 叨逼叨, 艺术加工, 冷知识, 夕爷, 李零, 负能量, 翻译腔, 波洛系列, 锵锵三人行, XD, 集结成册, 程雨城, 奶粉钱, 出场人物, 戾气, 功力深厚, 晦涩难懂, 怒其不争, 余杰, 紧张刺激, 《独唱团》, 《一一》, 豆瓣评分, 膝盖受伤, 耍贫, 许知远, 吊诡, 纸质版, PS:, 门下走狗, 长安乱, 作案手法, 拿出来, 素履之往, TM, 卡佛, 阅读体验, 厕所读物, 诙谐幽默, 门外青山, 《一个》, 《长安乱》, 柴静, 沈宏非, 浪漫骑士, 庄老师, 牛逼哄哄, 犯罪手法, 消磨时间, 稀里煳涂, 腹黑, 月棠记, 唿唤, 吹牛逼, 西西弗, 必读书目, 反复咀嚼, 哀其不幸, 牵着鼻子走, 《青春》, 品三国, 罗兰巴特, 社会现象, 疯子和天才, 淡淡的忧伤, 铁腿马三义, 希腊城邦, 金句```

## 句子相似度

可考虑使用 [sentence_bert_chinese](https://github.com/renmada/sentence_bert_chinese)，它使用 `STS` 和 `NLI` 任务的数据集在 [sentence-transformers](https://github.com/UKPLab/sentence-transformers) 上训练，对于句子的向量化效果优于 [RoFormer-Sim](https://kexue.fm/archives/8454) 模型。

示例（在鲁迅的25.8k个句子中寻找最相似者）：

```text
query: 其实世上本来没有路，走的人多了，才有了路。
result: 这正如地上的路；其实地上本没有路，走的人多了，也便成了路。（呐喊/故乡）
score: 0.9319522

query: 而且他对于我，渐渐地成为一种威压，甚至要榨出皮袍下面的小来。
result: 而且他对于我，渐渐的又几乎变成一种威压，甚而至于要榨出皮袍下面藏着的“小”来。（呐喊/一件小事）
score: 0.93162566

query: 这时，众人哄笑起来，店内充满快活的空气。
result: 在这时候，众人也都哄笑起来：店内外充满了快活的空气。(呐喊/孔乙己)
score: 0.918087

query: 到第二学年结束，我便去找藤野先生，告诉他我未来不再学习医学，离开仙台。
result: 到第二学年的终结，我便去寻藤野先生，告诉他我将不学医学，并且离开这仙台。(朝花夕拾/藤野先生)
score: 0.86963964

query: 茴香豆是怎样写的？
result: 茴香豆的茴字，怎样写的？” (呐喊/孔乙己)
score: 0.7946927
```
## 文本分类

### 使用 LSTM 实现简单二分类任务

```
label: 0, prob: 0.005,  史上最烂的电影，没有之一
label: 1, prob: 0.997,  我最喜欢的电影，太棒了
label: 0, prob: 0.012,  不打一星对不起我的电影票钱
label: 0, prob: 0.008,  无语
label: 0, prob: 0.010,  无力吐槽
label: 0, prob: 0.231,  不是我喜欢的类型
label: 1, prob: 0.968,  要推荐给所有朋友
label: 0, prob: 0.229,  不会推荐给任何朋友
label: 1, prob: 0.935,  居然看哭了！
label: 0, prob: 0.039,  我想我以后不会再看这个导演的作品了
```

