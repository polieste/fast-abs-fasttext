""" utility functions"""
import re
import os
from os.path import basename

import gensim
import torch
from torch import nn
import fasttext
from huggingface_hub import hf_hub_download

def count_data(path):
    """ count number of data in the given path"""
    matcher = re.compile(r'[0-9]+\.json')
    match = lambda name: bool(matcher.match(name))
    names = os.listdir(path)
    n_data = len(list(filter(match, names)))
    return n_data


PAD = 0
UNK = 1
START = 2
END = 3
def make_vocab(wc, vocab_size):
    word2id, id2word = {}, {}
    word2id['<pad>'] = PAD
    word2id['<unk>'] = UNK
    word2id['<start>'] = START
    word2id['<end>'] = END
    for i, (w, _) in enumerate(wc.most_common(vocab_size), 4):
        word2id[w] = i
    return word2id


def make_embedding(id2word, w2v_file, initializer=None):
    attrs = basename(w2v_file).split('.')  #word2vec.{dim}d.{vsize}k.bin
    #w2v = gensim.models.keyedvectors.KeyedVectors.load_word2vec_format(w2v_file,binary=True).wv
    model_path = hf_hub_download(repo_id="facebook/fasttext-vi-vectors", filename="model.bin")
    w2v = fasttext.load_model(model_path)
    vocab_size = len(id2word)
    emb_dim = 300
    embedding = nn.Embedding(vocab_size, emb_dim).weight
    if initializer is not None:
        initializer(embedding)

    oovs = []
    with torch.no_grad():
        for i in range(len(id2word)):
            # NOTE: id2word can be list or dict
            if i == START:
                embedding[i, :] = torch.Tensor(w2v['CLS'])
            elif i == END:
                embedding[i, :] = torch.Tensor(w2v['SLP'])
            elif id2word[i] in w2v:
                embedding[i, :] = torch.Tensor(w2v[id2word[i]])
            else:
                oovs.append(i)
    return embedding, oovs
