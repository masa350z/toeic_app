import pandas as pd
import numpy as np
import random


class Word:
    def __init__(self):
        self.words = pd.read_csv('words.csv')
        self.words_array = np.array(self.words)[:, :2]
        self.words_score = np.array(self.words['score'], dtype='float64')
        self.words_correct = np.array(self.words['correct'])
        self.words_appear = np.array(self.words['appear'])

        go = True
        while go:
            self.number = int(random.random()*len(self.words))
            go = False if random.random() >= self.words_score[self.number] else True

    def ret_word(self):
        return self.words_array[self.number][0]

    def ret_answer(self):
        return self.words_array[self.number][1]

    def refresh_states(self,t_or_f):
        self.words_appear[self.number] += 1
        if t_or_f:
            self.words_correct[self.number] += 1
        correct = self.words_correct[self.number]
        appear = self.words_appear[self.number]
        score = correct / appear * (1 - 1 / (correct + 1))
        self.words_score[self.number] = score

        return int(correct/appear*100), appear, round(score,3)

    def to_csv(self):
        pd_words = pd.DataFrame(self.words_array, columns=['words', 'meanings'])
        pd_score = pd.DataFrame(self.words_score, columns=['score'])
        pd_correct = pd.DataFrame(self.words_correct, columns=['correct'])
        pd_appear = pd.DataFrame(self.words_appear, columns=['appear'])

        words = pd.concat([pd_words, pd_score, pd_correct, pd_appear], axis=1)
        words.to_csv('words.csv', index=None, encoding='utf_8_sig')