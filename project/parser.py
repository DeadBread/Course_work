# -*- coding: utf-8 -*-

f = open("../output.txt")

class Sentence:
    def __init__(self, words_list):
        self.list = words_list

    def get_list(self):
        return self.list

    def find_word(self, word_id):
        tmp_list = [i for i in self.list if i['index'] == word_id]
        if tmp_list:
            return tmp_list[0]
        else:
            return None


class Text:
    def __init__(self, sentences_list):
        self.sent_list = sentences_list

    def find_word(self, word_id):
        for sent in self.sent_list:
            tmp = sent.find_word(word_id)
            if tmp is not None:
                return tmp
            else:
                pass
        return None

    def get_sent_list(self):
        return self.sent_list


sentences = []
tmp_sent = []
words_count = 0

for i, line in enumerate(f):

    spl = line.split()

    if len(spl) < 1:
        continue

    # print spl[9]

    # tmp_sent = []

    tmp_word = dict()
    tmp_word['index'] = i
    tmp_word['index in sentence'] = spl[0]
    tmp_word['text'] = spl[1]
    tmp_word['postag'] = spl[3]
    tmp_word['punct text'] = spl[4]
    tmp_word['morph features'] = spl[5]
    tmp_word['head'] = spl[6]
    tmp_word['deprel'] = spl[7]
    tmp_word['sentence'] = len(sentences)

    tmp_sent.append(tmp_word)

    if int(spl[0]) == 1:
        if i > 0:
            sentences.append(Sentence(tmp_sent))
        tmp_sent = []


text = Text(sentences)

# print text.find_word(200)
# print sentences[4].find_word(160)

pronoun_list = ["он", "она", "оно", "они"
                "его", "ее", "её", "их"
                "ему", "ей", "им",
                "нем", "ней", "них"]

pronoun_info = {}

pronoun_info["он"] = ["Animacy=Anim", "Case=Nom", "Gender=Masc", "Number=Sing"]
pronoun_info["она"] = ["Animacy=Anim", "Case=Nom", "Gender=Fem", "Number=Sing"]
pronoun_info["оно"] = ["Animacy=Inan", "Case=Nom", "Gender=Neut", "Number=Sing"]
pronoun_info["они"] = ["Case=Nom",  "Number=Plur"]
pronoun_info["его"] = ["Case=Acc", "Case=Gen", "Gender=Masc", "Gender=Neut", "Number=Sing"]
pronoun_info["еe"] = ["Animacy=Anim", "Case=Acc", "Case=Gen", "Gender=Fem", "Number=Sing"]
pronoun_info["её"] = pronoun_info["еe"]
pronoun_info["их"] = ["Case=Acc", "Case=Gen",  "Number=Plur"]
pronoun_info["ему"] = ["Case=Dat", "Gender=Masc", "Gender=Neut", "Number=Sing"]
pronoun_info["ей"] = ["Animacy=Anim", "Case=Dat", "Case=Ins", "Gender=Fem", "Number=Sing"]
pronoun_info["им"] = ["Case=Dat", "Number=Plur", "Gender=Masc", "Case=Ins", "Number=Sing"]
pronoun_info["нем"] = ["Case=Loc", "Gender=Masc", "Gender=Neut", "Number=Sing"]
pronoun_info["ней"] = ["Animacy=Anim", "Case=Loc", "Gender=Fem", "Number=Sing"]
pronoun_info["них"] = ["Case=Loc", "Number=Plur"]

# print pronoun_info



class Classifier:

    def __init__(self, text, way):
        self.text = text
        self.way = way

    def predict_word(self, num_word, num_prep):
        word = self.text.find_word(num_word)
        prep = self.text.find_word(num_prep)
        sent_num = word['sentence']
        area = self.text.get_sent_list()[sent_num - 7 : sent_num + 2]
        candidates = [w for w in area if self.is_word_acceptable(prep, w)]


    def is_word_acceptable(self, prep, candidate):
        #arguments dependancy
        if prep['head'] == candidate['head']:
            return False

        elif


    #
    # def __is_acceptable (self, num_word, )

    # def predict(self, num_sentence):
