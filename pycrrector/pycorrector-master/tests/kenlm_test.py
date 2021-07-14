# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import kenlm

import jieba

from pycorrector import language_model_path

model = kenlm.Model(language_model_path)

sentence = '盘点不怕被税的海淘网站❗️海淘向来便宜又保真！'
sentence_char_split = ' '.join(list(sentence))
sentence_word_split = ' '.join(jieba.lcut(sentence))


def test_score():
    print('Loaded language model: %s' % language_model_path)

    print(sentence)
    print(model.score(sentence))
    print(list(model.full_scores(sentence)))
    for i, v in enumerate(model.full_scores(sentence)):
        print(i, v)

    print(sentence_char_split)
    print(model.score(sentence_char_split))
    print(list(model.full_scores(sentence_char_split)))
    split_size = 0
    for i, v in enumerate(model.full_scores(sentence_char_split)):
        print(i, v)
        split_size += 1
    assert split_size == len(sentence_char_split.split()) + 1, "error split size."

    print(sentence_word_split)
    print(model.score(sentence_word_split))
    print(list(model.full_scores(sentence_word_split)))
    for i, v in enumerate(model.full_scores(sentence_word_split)):
        print(i, v)


def test_full_scores_chars():
    print('Loaded language model: %s' % language_model_path)
    # Show scores and n-gram matches
    words = ['<s>'] + list(sentence) + ['</s>']
    for i, (prob, length, oov) in enumerate(model.full_scores(sentence_char_split)):
        print('{0} {1}: {2}'.format(prob, length, ' '.join(words[i + 2 - length:i + 2])))
        if oov:
            print('\t"{0}" is an OOV'.format(words[i + 1]))

    print("-" * 42)
    # Find out-of-vocabulary words
    oov = []
    for w in words:
        if w not in model:
            print('"{0}" is an OOV'.format(w))
            oov.append(w)
    assert oov == ["❗", "️", "！"], 'error oov'


def test_full_scores_words():
    print('Loaded language model: %s' % language_model_path)
    # Show scores and n-gram matches
    words = ['<s>'] + sentence_word_split.split() + ['</s>']
    for i, (prob, length, oov) in enumerate(model.full_scores(sentence_word_split)):
        print('{0} {1}: {2}'.format(prob, length, ' '.join(words[i + 2 - length:i + 2])))
        if oov:
            print('\t"{0}" is an OOV'.format(words[i + 1]))

    print("-" * 42)
    # Find out-of-vocabulary words
    oov = []
    for w in words:
        if w not in model:
            print('"{0}" is an OOV'.format(w))
            oov.append(w)
    assert oov == ["盘点", "不怕", "网站", "❗", "️", "海淘", "向来", "便宜", "保真", "！"], 'error oov'


def test_full_scores_chars_length():
    """test bos eos size"""
    print('Loaded language model: %s' % language_model_path)
    r = list(model.full_scores(sentence_char_split))
    n = list(model.full_scores(sentence_char_split, bos=False, eos=False))

    print(r)
    print(n)
    assert len(r) == len(n) + 1
    print(len(n), len(sentence_char_split.split()))
    assert len(n) == len(sentence_char_split.split())
    k = list(model.full_scores(sentence_char_split, bos=False, eos=True))
    print(k, len(k))


def test_ppl_sentence():
    """测试句子粒度的ppl得分"""
    sentence_char_split1 = ' '.join('先救挨饿的人，然后治疗病人。')
    sentence_char_split2 = ' '.join('先就挨饿的人，然后治疗病人。')
    n = model.perplexity(sentence_char_split1)
    print('1', n)
    n = model.perplexity(sentence_char_split2)
    print(n)

    part_char_split1 = ' '.join('先救挨饿的人')
    part_char_split2 = ' '.join('先就挨饿的人')
    n = model.perplexity(part_char_split1)
    print('2', n)
    n = model.perplexity(part_char_split2)
    print(n)

    part_char_split1 = '先救挨'
    part_char_split2 = '先就挨'
    n1 = model.perplexity(part_char_split1)
    print('3', n1)
    n2 = model.perplexity(part_char_split2)
    print(n2)
    assert n1 == n2

    part_char_split1 = '先 救 挨'
    part_char_split2 = '先 就 挨'
    n1 = model.perplexity(part_char_split1)
    print('4', n1)
    n2 = model.perplexity(part_char_split2)
    print(n2)

    part_char_split1 = '先 救 挨 饿 的 人'
    part_char_split2 = '先 就 挨 饿 的 人'
    n1 = model.perplexity(part_char_split1)
    print('5', n1)
    n2 = model.perplexity(part_char_split2)
    print(n2)

    part_char_split1 = '先 救 挨 饿 的 人 ，'
    part_char_split2 = '先 就 挨 饿 的 人 ，'
    n1 = model.perplexity(part_char_split1)
    print('6', n1)
    n2 = model.perplexity(part_char_split2)
    print(n2)

    part_char_split1 = '先 救 挨 饿 的 人 ， 然 后 治 疗 病 人'
    part_char_split2 = '先 就 挨 饿 的 人 ， 然 后 治 疗 病 人'
    n1 = model.perplexity(part_char_split1)
    print('7', n1)
    n2 = model.perplexity(part_char_split2)
    print(n2)

    part_char_split1 = '先 救 挨 饿 的 人 ， 然 后 治 疗 病 人 。'
    part_char_split2 = '先 就 挨 饿 的 人 ， 然 后 治 疗 病 人 。'
    n1 = model.perplexity(part_char_split1)
    print('8', n1)
    n2 = model.perplexity(part_char_split2)
    print(n2)
