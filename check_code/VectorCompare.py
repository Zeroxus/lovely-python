import math


class VectorCompare:
    def __init__(self):
        pass

    #计算矢量大小
    def magnitude(self,concordance):
        total = 0
        for word,count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    #计算矢量之间的 cos 值
    def relation(self,concordance1, concordance2):
        relevance = 0
        topvalue = 0
        for word, count in concordance1.items():
            if concordance2.get(word):
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))
