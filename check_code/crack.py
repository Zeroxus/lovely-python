from PIL import Image
import time,hashlib,os,math
from VectorCompare import VectorCompare


class checkHack:
    def __init__(self,im):
        self.im = im

    def getPixel(self):
        values = {}
        self.im.convert("P")
        hist = self.im.histogram()
        for i in range(256):
            values[i] = hist[i]
        for j,k in sorted(values.items(),key=lambda x:x[1],reverse=True)[:10]:
            print(j,k)
        return hist

    def getBinary(self):
        hist = self.getPixel()
        im2 = Image.new("P",self.im.size,255)

        for x in range(self.im.size[1]):
            for y in range(self.im.size[0]):
                pix = self.im.getpixel((y,x))
                if pix == 220 or pix == 227 or pix == 234:
                    im2.putpixel((y,x),0)
        im2.show()
        return im2

    def getCharacter(self,im2):
        inletter = False
        foundletter = False
        start = 0
        end = 0
        letters = []
        for y in range(im2.size[0]):
            for x in range(im2.size[1]):
                pix = im2.getpixel((y,x))
                if pix !=255:
                    inletter=True
            if foundletter == False and inletter == True:
                foundletter = True
                start = y
            if foundletter == True and inletter == False:
                foundletter = False
                end = y
                letters.append((start,end))
            inletter = False
        count = 0
        for letter in letters:
            m = hashlib.md5()
            im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))
            m.update("{}{}".format(time.time(), count).encode('utf8'))
            # im3.save("./{}.gif".format(m.hexdigest()))
            count += 1
        return letters

    def getVector(self,im):
        d1 = {}
        count = 0
        for i in im.getdata():
            d1[count] = i
            count += 1
        return d1

    def predict(self,letters):
        # 加载训练集
        # v = VectorCompare()
        iconset = ['0','1','2','3','4','5','6','7','8','9','0','a',
                   'b','c','d','e','f','g','h','i','j','k','l','m',
                   'n','o','p','q','r','s','t','u','v','w','x','y','z']
        imageset = []
        for letter in iconset:
            for img in os.listdir('./python_captcha/iconset/{}/'.format(letter)):
                temp = []
                if img != "Thumbs.db" and img != ".DS_Store":
                    temp.append(self.getVector(Image.open("./python_captcha/iconset/{}/{}".format(letter, img))))
                imageset.append({letter: temp})
        v = VectorCompare()
        count = 0
        # 对验证码图片进行切割
        for letter in letters:
            m = hashlib.md5()
            im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))
            im3 = self.getVector(im3)
            guess = []

            # 将切割得到的验证码小片段与每个训练片段进行比较
            for image in imageset:
                for x, y in image.items():
                    if len(y) != 0:
                        # print(im3)
                        # print(y[0])
                        # time.sleep(2)
                        guess.append((v.relation(concordance1=y[0], concordance2=im3), x))

            guess.sort(reverse=True)
            print("", guess[0])
            count += 1


if __name__=='__main__':
    im = Image.open("captcha.gif")
    check = checkHack(im)
    im2 = check.getBinary()
    letters = check.getCharacter(im2)
    check.predict(letters)