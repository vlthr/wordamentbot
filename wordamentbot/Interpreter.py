from PIL import ImageGrab, ImageOps, ImageFilter, ImageEnhance
from wordamentbot.pytesser import pytesser
import re
from wordamentbot.datatypes import Board, BoardUnit 

def prompt_classify(image):
    image.show()
    classification = input("Input correct reading: ")
    return classification.strip()

if __name__ == '__main__':
    image = enhance(grab_value(0,0))
    # image = grab_value(3,3)
    # image.show()
    for x in range(0,4):
        for y in range(0,4):
            image = grab_value(x,y)
            classification = classify(image)
            print(classification)
            # image.show()
class Interpreter(object):
    def __init__(self, scout,config):
        self.scout = scout
        self.config = config
    def get_tile_score(self,x,y):
        classification = self.score_classify(self.scout.grab_score(x,y))
        return int(classification)
    def get_tile_value(self,x,y):
        classification = self.classify(self.scout.grab_value(x,y))
        return classification
    def get_values(self):
        tiles = []
        for y in range(0,self.config.N):
            for x in range(0, self.config.N):
                tiles.append(self.get_tile_value(x,y))
        return tiles
    def get_board(self):
        board = Board(self.get_values(), self.get_scores(), self.config.N)
        return board
    def classify(self):
        pass
    def get_scores(self):
        scores = []
        for y in range(0,self.config.N):
            for x in range(0, self.config.N):
                scores.append(self.get_tile_score(x,y))
        return scores
    def get_time(self):
        pass
    def get_points(self):
        pass
    def get_words(self):
        pass
class PytesserInterpreter(Interpreter):
    def enhance(self,image):
        # image = image.filter(ImageFilter.MedianFilter())
        # image.show()
        enhancer = ImageEnhance.Contrast(image)
        # image.show()
        image = enhancer.enhance(5)
        # image.show()
        # image.show()
        image = image.convert('L')
        image = ImageOps.invert(image)
        image = image.point(lambda x: 0 if x<100 else 255, '1')
        # image.show()
        return image

    def classify(self,image):
        image = self.enhance(image)
        classification = pytesser.image_to_string(image)
        if re.match("\s+", classification):
            # classification = prompt_classify(image)
            classification = 'I'
        return classification.strip()
    def score_classify(self, image):
        image = self.enhance(image)
        classification = pytesser.image_to_string(image)
        if re.match("\s+", classification):
            # classification = prompt_classify(image)
            classification = '0'
        return classification.strip()

    def time_classify(self, image):
        image = self.enhance(image)
        classification = pytesser.image_to_string(image)
        minutes, seconds = classification.strip().split(":")
        return int(minutes) * 60 + int(seconds)

    def get_time(self):
        image = self.scout.grab_clock()
        time = self.time_classify(image)
        return time
    def get_points(self):
        pass
    def get_words(self):
        pass
