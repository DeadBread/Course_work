# -*- coding: utf-8 -*-

from gensim.models import KeyedVectors
from nltk.stem.snowball import SnowballStemmer
from pymystem3 import Mystem
from sklearn import linear_model

f = open("../output1.txt")
file = f.read()
f = file.split('\n')

pronoun_text_list = ["он", "его", "него", "ему", "нему", "им", "ним", "нем", "нём",
                     "она", "ее", "её", "нее", "неё", "ей", "ней", "ею", "нею",
                     "оно",
                     "они", "их", "них", "им", "ним", "ими", "ними"]

pronoun_feature_list = {}

pronoun_feature_list["он"] = "Animacy=Anim|Case=Nom|Gender=Masc|Number=Sing"
pronoun_feature_list["него"] = "Animacy=Anim|Case=AccGen|Gender=MascNeut|Number=Sing"
pronoun_feature_list["его"] = "Animacy=Anim|Case=AccGen|Gender=MascNeut|Number=Sing"
pronoun_feature_list["ему"] = "Animacy=Anim|Case=Dat|Gender=MascNeut|Number=Sing"
pronoun_feature_list["нему"] = "Animacy=Anim|Case=Dat|Gender=MascNeut|Number=Sing"
pronoun_feature_list["им"] = "Animacy=Anim|Case=DatIns"
pronoun_feature_list["ним"] = "Animacy=Anim|Case=InsDat|Gender=MascNeut"
pronoun_feature_list["нем"] = "Animacy=Anim|Case=Loc|Gender=MascNeut|Number=Sing"
pronoun_feature_list["нём"] = pronoun_feature_list["нем"]

pronoun_feature_list["она"] = "Animacy=Anim|Case=Nom|Gender=Fem|Number=Sing"
pronoun_feature_list["ее"] = "Animacy=Anim|Case=AccGen|Gender=Fem|Number=Sing"
pronoun_feature_list["её"] = pronoun_feature_list["ее"]
pronoun_feature_list["нее"] = "Animacy=Anim|Case=AccGen|Gender=Fem|Number=Sing"
pronoun_feature_list["неё"] = pronoun_feature_list["нее"]
pronoun_feature_list["ей"] = "Animacy=Anim|Case=DatIns|Gender=Fem|Number=Sing"
pronoun_feature_list["ею"] = "Animacy=Anim|Case=Ins|Gender=Fem|Number=Sing"
pronoun_feature_list["ней"] = "Animacy=Anim|Case=InsLoc|Gender=Fem|Number=Sing"
pronoun_feature_list["нею"] = "Animacy=Anim|Case=InsLoc|Gender=Fem|Number=Sing"

pronoun_feature_list["оно"] = "Animacy=Inan|Case=Nom|Gender=Neut|Number=Sing"

pronoun_feature_list["они"] = "Case=Nom|Number=Plur"
pronoun_feature_list["их"] = "Case=AccGen|Number=Plur"
pronoun_feature_list["них"] = "Case=AccGenLoc|Number=Plur"
# pronoun_feature_list["им"] = "Case=DatIns"
# pronoun_feature_list["ним"] = "Case=Dat|Number=Plur"
pronoun_feature_list["ими"] = "Animacy=Anim|Case=Ins|Number=Plur"
pronoun_feature_list["ними"] = "Animacy=Anim|Case=Ins|Number=Plur"


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
        # print self.list

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

    def occ_num(self, word_text):
        i = 0;
        for word in self.get_list():
            if word_text == word.field('text'):
                i += 1
        return i


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

    def get_word_frequency(self, word_text):
        return sum([sent.occ_num(word_text) for sent in self.get_sent_list()])


class Classifier:

    def __init__(self, text, pronoun_list):
        self.text = text
        self.pronoun_list = pronoun_list
        # self.way = way
        self.associations = dict()
        self.model = KeyedVectors.load_word2vec_format('/home/gand/lib/word2vec/ruscorpora.model.bin', binary=True)
        # self.stemmer = SnowballStemmer('russian')
        self.mystem = Mystem()

        self.s_dist_list = []


        # purity = 52.2%
        # self.coefficients = [-0.05,-1,3,2,2,2,5,3]

        # purity = 57%
        # self.coefficients = [-0.5, 0, 3, 2, 2, 2, 5, 3, 5]

        # purity > 62%
        # purity = 65.2% with area = 10
        self.coefficients = [-0.5, 0, 3, 1, 1, 1, 0.65, 0, 5]

        # purity = 55.1%
        # self.coefficients = [-1, 0, 1, 1, 1, 1, 1, 1, 1]

        self.classifier = linear_model.LogisticRegression(solver='liblinear', verbose=0)
        # self.classifier = svm.SVC(C = 10, probability=True)
        # self.classifier = tree.DecisionTreeClassifier(class_weight={0:1, 1:10}, max_depth=4)

    def import_answers(self, file):
        file = open(file)
        self.answer_list = []
        self.answer_dict = dict()
        for line in file:
            line = line.split()
            self.answer_list.append(int(line[1]))
            self.answer_dict[int(line[0])] = int(line[1])

    def build_prediction_list(self):
        self.pred_list = []
        for sentence in self.text.get_sent_list():
            for word in sentence.get_list():
                if word.field('text').lower() in pronoun_text_list:
                    self.pred_list.append(word)

    def predict(self):
        i = 0.0
        self.build_prediction_list()
        for pronoun in self.pred_list:
            tmp = self.predict_word(pronoun.field('index'))
            print pronoun.field('text'), pronoun.field('index'), "refers to", tmp.field('text'), tmp.field('index')
            if self.answer_dict[pronoun.field('index')] == tmp.field('index'):
                i += 1.0
            else:
                print "wrong! ", tmp.field('index'), "instead of", self.answer_dict[pronoun.field('index')]

        print "purity",  i / len(self.answer_list)



        return (i, len(self.answer_list))

    def candidates_list(self, pronoun):
        sent_num = pronoun.field('sentence')
        area = self.text.get_sent_list()[max(sent_num - 10, 0): min(sent_num + 1, len(self.text.get_sent_list()))]

        # print pronoun.field('text')
        candidates = []
        for sentence in area:
            tmp = sentence.get_list()
            for word in tmp:
                if self.is_word_acceptable(pronoun, word):
                    candidates.append(word)
        return candidates

    def predict_word(self, num_pron):
        # word = self.text.find_word(num_word)
        pronoun = self.text.find_word(num_pron)
        # print num_pron, pronoun.field('text')
        sent_num = pronoun.field('sentence')

        candidates = self.candidates_list(pronoun)

        self.features = {}
        for candidate in candidates:
            self.features[candidate] = self.get_features_list(candidate, pronoun)


        antecedent = self.get_right_word(pronoun)
        self.associations[pronoun] = antecedent

        pronoun.field('string')[9] = "refto_" + str(antecedent.field('index') + 1)

        self.features = dict()

        return antecedent
            # print candidate.field('text'), self.features[candidate]

    def get_right_word(self, pronoun):
        score_list = []
        for candidate in self.features.keys():
            if candidate.field('index') in self.associations.values():    #coreference!
                tmp_distances = []
                tmp_s_distances = []
                tmp = [i for i in self.associations.keys() if self.associations[i] == candidate]
                for pron2 in tmp:
                    if self.coreference(pronoun, pron2):
                        return candidate
                    tmp_distances.append(pronoun.field('index') - pron2.field('index'))
                    tmp_s_distances.append(pronoun.field('sentence index') - pron2.field('sentence index'))

                new_distance = min(tmp_distances)
                new_s_distance = min(tmp_s_distances)
                self.features[candidate][0] = new_distance
                self.features[candidate][1] = new_s_distance

            tmp_features = [a * b for (a, b) in zip(self.features[candidate], self.coefficients)]

            score = sum(tmp_features)
            score_list.append(score)

        res = self.features.keys()[score_list.index(max(score_list))]

        self.s_dist_list.append(self.features[res][1])

        # print self.features[res], "- features of candidate, score =", max(score_list)
        try:
            ans_feat = self.features[self.text.find_word(self.answer_list[self.pred_list.index(pronoun)])]
            # print ans_feat, "features of answer, score = ", sum([a * b for (a, b) in zip(ans_feat, self.coefficients)])
        except:
            print "not found in candidate list!"


        return res

    def coreference(self, left_pron, right_pron):

        if left_pron.field('head') == right_pron.field('head') and \
                left_pron.field('sentence') == right_pron.field('sentence'):
            return False

        set1 = ["он", "его", "него", "ему", "нему", "им", "ним", "нем", "нём"]
        set2 =  ["она", "ее", "её", "нее", "неё", "ей", "ней", "ею", "нею"]

        if left_pron.field("sentence") == right_pron.field('sentence'):
            if left_pron.field('text') in set1 and right_pron.field('text') in set1 or \
                    left_pron.field('text') in set2 and right_pron.field('text') in set2:
                return True

        if left_pron.field("sentence") == right_pron.field('sentence') - 1:
            if left_pron.field('text') == right_pron.field('text'):
                return True
        else:
            return False

    def get_features_list(self, candidate, pronoun):

        pronoun_info = [i for i in self.pronoun_list if i.get_text() == pronoun.field('text')][0]
        features_list = []

        # distance between candidate and pronoun. Might be negative, if candidate is further then the pronoun
        delta = 0
        if candidate.field('index') in self.associations.keys():
            tmp = self.associations[candidate.field('index')]
            delta = pronoun.field('index') - tmp.field('index')
        else:
            delta = pronoun.field('index') - candidate.field('index')

        if delta < 0:
            delta = - delta * 3
        features_list.append(delta)

        #number of sentences between candidate and pronoun. Also might be negative
        sent_delta = 0
        if candidate.field('sentence') in self.associations.keys():
            tmp = self.associations[candidate.field('sentence')]
            sent_delta = pronoun.field('sentence') - tmp.field('sentence')
        else:
            sent_delta = pronoun.field('sentence') - candidate.field('sentence')

        if sent_delta < 0:
            sent_delta = - sent_delta * 3
        features_list.append(sent_delta)

        #feature connected with candidates position in a sentence
        pos_feature = 0
        if candidate.field('deprel') == 'nsubj' or candidate.field('postag') == 'nsubjpass':
            pos_feature = 2
        elif candidate.field('deprel') == 'dobj':
            pos_feature = 1

        features_list.append(pos_feature)

        # :TODO frequency feature might be implemented
        # :TODO add word2vec feature if there will be any time left

        # feature connected with the case of pronoun and it's antecedent
        # It's written like "in" here, because each pronoun may have several  variants of case
        case_feature = 0
        if candidate.get_feature('Case') is not None:
            if candidate.get_feature('Case') in pronoun_info.get_feature('Case'):
                case_feature = 1
        features_list.append(case_feature)

        #feature connected with animacy of candidate
        animacy_feature = 0
        if pronoun.get_feature('Animacy') is not None and candidate.get_feature('Animacy') is not None:
            if candidate.get_feature('Animacy') in pronoun_info.get_feature('Animacy'):
                animacy_feature = 1
        features_list.append(animacy_feature)


        #simple parallelism feature
        synt_parallel_feature = 0
        if candidate.field("deprel") == pronoun.field("deprel"):
            synt_parallel_feature = 1
            head_pron = self.text.get_sentence(pronoun.field('sentence')).find_in_sentence(pronoun.field('head'))
            head_candidate = self.text.get_sentence(candidate.field('sentence')).find_in_sentence(candidate.field('head'))
            if head_candidate is not None and head_pron is not None and head_candidate.field('deprel') == head_pron.field('deprel'):
                synt_parallel_feature = 3
                if head_pron.field('deprel') == 'ROOT':
                    synt_parallel_feature = 6
        features_list.append(synt_parallel_feature)

        #Frequency feature
        frequency_feature = self.text.get_word_frequency(self.mystem.lemmatize(candidate.field('text'))[0])
        # frequency_feature = self.text.get_word_frequency(self.stemmer.stem(candidate.field('text').decode('utf8')).encode('utf8'))
        features_list.append(frequency_feature)

        #Using Word2Vec
        similarity_feature = 0
        left_neighbour = self.text.find_word(pronoun.field('index') - 1)

        if left_neighbour.field('punct text') != '_':
            left_neighbour = self.text.find_word(pronoun.field('index') - 2)

        right_neighbour = self.text.find_word(pronoun.field('index') + 1)
        if right_neighbour.field('punct text') != '_':
            right_neighbour = self.text.find_word(pronoun.field('index') + 2)

        try:
            left_neighbour_lemma = self.mystem.lemmatize(left_neighbour.field('text'))[0]
            right_neighbour_lemma = self.mystem.lemmatize(right_neighbour.field('text'))[0]

            candidate_lemma = self.mystem.lemmatize(candidate.field('text'))[0]

            if left_neighbour_lemma is not None:
                similarity_feature += self.model.similarity(candidate_lemma.decode('utf8'),
                                                            left_neighbour_lemma.decode('utf8'))
            if right_neighbour_lemma is not None:
                similarity_feature += self.model.similarity(candidate_lemma.decode('utf8'),
                                                            right_neighbour_lemma.decode('utf8'))
        except:
            pass

        features_list.append(similarity_feature)

        tmp = [i for i in self.associations.keys() if self.associations[i].field('index') == candidate.field('index')]
        coreference_feature = len(tmp)
        features_list.append(coreference_feature)

        # gender_feature = 0
        # if candidate.get_feature('Gender') and pronoun_info.get_feature('Gender') is not None:
        #     if features_list.append(candidate.get_feature('Gender') in pronoun_info.get_feature('Gender')):
        #         gender_feature = 1
        # features_list.append(gender_feature)


        # print len(features_list)

        return features_list

    def is_word_acceptable(self, pron, candidate):

        condition_list = []

        # leave nouns only

        if candidate.field('postag') != 'NOUN':
            return False

        pronoun_info = [i for i in pronoun_list if i.get_text() == pron.field('text')][0]

        # pronoun and antecedent should be the same number
        if candidate.get_feature('Number') and pronoun_info.get_feature('Number') is not None:
            condition_list.append(candidate.get_feature('Number') in pronoun_info.get_feature('Number'))

        # need to do something with that. In syntaxnet gender doesn't always work correctly
        if candidate.get_feature('Gender')and pronoun_info.get_feature('Gender') is not None:
            condition_list.append(candidate.get_feature('Gender') in pronoun_info.get_feature('Gender'))

        tmp_word = self.text.get_sentence(candidate.field('sentence')).find_in_sentence(candidate.field('head'))

        # arguments dependancy
        arg_dep = pron.field('head') != candidate.field('head') or \
                    pron.field('sentence') != candidate.field('sentence')

        condition_list.append(arg_dep)

        # NP dependancy
        # np_dep = True
        # if tmp_word is not None:
        #     np_dep = pron.field('head') != tmp_word.field('head') or \
        #                           tmp_word.field('deprel') != "nmod" or \
        #                           tmp_word.get_feature("Case") != "Gen" or \
        #                           pron.field('sentence') != candidate.field('sentence')
        #     condition_list.append(np_dep)

        for i, cond in enumerate(condition_list):
            if not cond:
                # if candidate.field('index') == 209:
                #     print "stopped here!", i
                return False
        return True

    def output(self, file):
        for sentence in self.text.get_sent_list():
            for word in sentence.get_list():
                file.write(reduce((lambda x, y: x + " " + y), word.field('string')) + '\n')


#:TODO distribute the code to different files

pronoun_list = [Pronoun(i, pronoun_feature_list[i]) for i in pronoun_text_list]


def get_text(file):
    sentences = []
    tmp_sent = []
    words_count = 0

    i = 0
    for line in file:
        spl = line.split()

        if len(spl) < 1:
            continue

        tmp_word = dict()
        tmp_word['string'] = spl
        tmp_word['index'] = i
        tmp_word['index in sentence'] = spl[0]
        tmp_word['text'] = spl[1].decode('utf8').lower().encode('utf8')
        tmp_word['postag'] = spl[3]
        tmp_word['punct text'] = spl[4]
        tmp_word['morph features'] = spl[5]
        tmp_word['head'] = spl[6]
        tmp_word['deprel'] = spl[7]
        tmp_word['sentence'] = len(sentences)

        new_word = Word(tmp_word)

        if int(spl[0]) == 1:
            if i > 0:
                sentences.append(Sentence(tmp_sent))
            tmp_sent = []

        tmp_sent.append(new_word)

        i += 1

    sentences.append(Sentence(tmp_sent))

    return Text(sentences)

train_file = open("../output1.txt")
file = train_file.read()
train_file = file.split('\n')

text = get_text(train_file)

cls = Classifier(text, pronoun_list)
cls.import_answers("../answers")


output_file = open("../result", 'w')

cls.import_answers("../answers")
a1 = cls.predict()

# cls.output(output_file)

print a1

train_file = open("../output2.txt")
file = train_file.read()
train_file = file.split('\n')

text = get_text(train_file)

cls.text = text

cls.import_answers("../answers2")

a2 = cls.predict()

print a2

print "purity = ", (a1[0] + a2[0]) / (a1[1] + a2[1])


