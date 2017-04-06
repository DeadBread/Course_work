# -*- coding: utf-8 -*-

f = open("../output.txt")

class AbstractWord:
    def __init__(self):
        pass

    def __parse_features__(self, morph_features):
        features = morph_features.split('|')
        parsed_features_tmp = [f.split('=') for f in features]
        parsed_features = {key:value for key, value in parsed_features_tmp}
        return parsed_features

    def get_feature(self, feature):
        return self.parsed_features.get(feature)

class Word(AbstractWord):
    def __init__(self, word_dict):
        self.word_dict = word_dict
        self.parsed_features = self.__parse_features__(self.word_dict['morph features'])

    def field(self, field):
        return self.word_dict[field]

class Pronoun(AbstractWord):
    def __init__(self, text, features):
        self.text = text
        self.parsed_features = self.__parse_features__(features)

    def get_text(self):
        return self.text

class Sentence:
    def __init__(self, words_list):
        self.list = words_list

    def get_list(self):
        return self.list

    def find_word(self, word_id):
        tmp_list = [i for i in self.list if i.field('index') == word_id]
        if tmp_list:
            return tmp_list[0]
        else:
            return None

    def find_in_sentence(self, sent_word_id):
        tmp_list = [i for i in self.list if i.field('index in sentence') == sent_word_id]
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

    def get_sentence(self, sent_num):
        return self.sent_list[sent_num]

    def get_sent_list(self):
        return self.sent_list


sentences = []
tmp_sent = []
words_count = 0

for i, line in enumerate(f):

    spl = line.split()

    if len(spl) < 1:
        continue

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

    new_word = Word(tmp_word)

    tmp_sent.append(new_word)

    if int(spl[0]) == 1:
        if i > 0:
            sentences.append(Sentence(tmp_sent))
        tmp_sent = []


text = Text(sentences)


pronoun_text_list = ["он", "она", "оно", "они",
                     "его", "ее", "её", "их",
                     "ему", "ей", "им",
                     "нем", "ней", "них"]

pronoun_feature_list = {}

pronoun_feature_list["он"] = "Animacy=Anim|Case=Nom|Gender=Masc|Number=Sing"
pronoun_feature_list["она"] = "Animacy=Anim|Case=Nom|Gender=Fem|Number=Sing"
pronoun_feature_list["оно"] = "Animacy=Inan|Case=Nom|Gender=Neut|Number=Sing"
pronoun_feature_list["они"] = "Case=Nom|Number=Plur"
pronoun_feature_list["его"] = "Case=AccGen|Gender=MascNeut|Number=Sing"
pronoun_feature_list["ее"] = "Animacy=Anim|Case=AccGen|Gender=Fem|Number=Sing"
pronoun_feature_list["её"] = pronoun_feature_list["ее"]
pronoun_feature_list["их"] = "Case=AccGen|Number=Plur|Gender=Masc"
pronoun_feature_list["ему"] = "Case=Dat|Gender=MascNeut|Number=Sing"
pronoun_feature_list["ей"] = "Animacy=Anim|Case=DatIns|Gender=Fem|Number=Sing"
pronoun_feature_list["им"] = "Case=DatIns|Number=Plur"
pronoun_feature_list["нем"] = "Case=Loc|Gender=Masc|Gender=Neut|Number=Sing"
pronoun_feature_list["ней"] = "Animacy=Anim|Case=Loc|Gender=Fem|Number=Sing"
pronoun_feature_list["них"] = "Case=Loc|Number=Plur"

pronoun_list = [Pronoun(i, pronoun_feature_list[i]) for i in pronoun_text_list]

class Classifier:

    def __init__(self, text, way):
        self.text = text
        self.way = way

    def build_prediction_list(self):
        self.pred_list = []
        for sentence in text.get_sent_list():
            for word in sentence.get_list():
                if word.field('text') in pronoun_text_list:
                    self.pred_list.append(word)

    def predict_word(self, num_word, num_pron):
        # word = self.text.find_word(num_word)
        pronoun = self.text.find_word(num_pron)
        sent_num = pronoun.field('sentence')
        area = self.text.get_sent_list()[max (sent_num - 5, 0) : sent_num + 2]

        print pronoun.field('text')
        candidates = []
        for sentence in area:
            tmp = sentence.get_list()
            for word in tmp:
                if self.is_word_acceptable(pronoun, word):
                    candidates.append(word)
                    print word.field('text')

        print len(candidates)

    def is_word_acceptable(self, pron, candidate):

        condition_list = []

        # leave nouns only
        if candidate.field('postag') != 'NOUN':
            return False

        pronoun_info = [i for i in pronoun_list if i.get_text() == pron.field('text')][0]

        # pronoun and atecedent should be the same number
        condition_list.append( candidate.get_feature('Number') == pronoun_info.get_feature('Number') )

        tmp_word = self.text.get_sentence(candidate.field('sentence')).find_in_sentence(candidate.field('head'))

        # arguments dependancy
        condition_list.append( pron.field('head') != candidate.field('head') )

        # NP dependancy
        if tmp_word is not None:
            condition_list.append( pron.field('head') != tmp_word.field('head') and \
                                  tmp_word.field('deprel') != "nmod" and \
                                  tmp_word.get_feature("Case") != "Gen" )

        for i, cond in enumerate(condition_list):
            if not cond:
                return False

        return True



cls = Classifier(text, 0)

cls.build_prediction_list()
cls.predict_word(0, cls.pred_list[4].field('index'))
    #
    # def __is_acceptable (self, num_word, )

    # def predict(self, num_sentence):
