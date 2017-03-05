# -*- coding: utf-8 -*-

f = open("../output.txt")

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

    tmp_sent.append(tmp_word)

    if int(spl[0]) == 1:
        if i > 0:
            sentences.append(tmp_sent)
        tmp_sent = []

print len(sentences[1])

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

print pronoun_info

class Classifier:

    def __init__(self, text, way):
        self.text = text
        self.way = way

    def predict_word(self, num_sentence, num_word):
        pass

    # def predict(self, num_sentence):
