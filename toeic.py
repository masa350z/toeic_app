import pandas as pd
import numpy as np
import random

while True:
    words = pd.read_csv('words.csv')
    words_array = np.array(words)[:,:2]
    words_score = np.array(words['score'], dtype='float64')
    words_correct = np.array(words['correct'])
    words_appear = np.array(words['appear'])

    go = 0
    while go == 0:
        number = int(random.random()*len(words))
        if random.random() >= words_score[number]:
            go = 1

    print(words_array[number][0])
    input('>')
    print(words_array[number][1])
    t_or_f = input('>>>')
    words_appear[number] += 1
    if t_or_f == '':
        words_correct[number] += 1
    correct = words_correct[number]
    appear = words_appear[number]
    score = correct/appear*(1-1/(correct+1))
    words_score[number] = score

    pd_words = pd.DataFrame(words_array,columns=['words','meanings'])
    pd_score = pd.DataFrame(words_score,columns=['score'])
    pd_correct = pd.DataFrame(words_correct,columns=['correct'])
    pd_appear = pd.DataFrame(words_appear,columns=['appear'])

    words = pd.concat([pd_words,pd_score,pd_correct,pd_appear],axis=1)
    words.to_csv('words.csv',index=None,encoding='utf_8_sig')