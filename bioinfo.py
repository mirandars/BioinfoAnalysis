import pandas as pd
import matplotlib.pyplot as plt
from Bio.Seq import Seq

amn_list = [['Adenine','A'],
 ['Cytosine','C'],
 ['Guanine','G'],
 ['Thymine','T'],
 ['Uracil','U'],
 ['Purine','A','G'],
 ['Pyrimidines','T','U'],
 ['Non-identified','N']]

codon_list = ['AA','AC','AT']

plot_list = ['Adenine','Cytosine','Guanine','Thymine','Non-identified']

def amino_acids_count(df, amn_list):
    for amn in amn_list:
        df[amn[0]] = 0.0
        for letter in amn[1:]:
            df[amn[0]] = df[amn[0]] + df['Sequence'].apply(lambda seq:seq.count(letter))
        df[amn[0]] = df[amn[0]]/df['Length']
    return df

def split_DNA(seq,n):
    return [seq[i:i+n] for i in range(0, len(seq), n)]

def codon_count(codon_list,seq,n):
    sseq = split_DNA(seq,n)
    return [sum(list(map(lambda x: x.count(codon),sseq))) for codon in codon_list]


def gen_df(infile):
    with open(infile, 'r') as myfile:
        data=myfile.read()
    
    data = data.split('>')
    dic = {}

    for i in range(len(data)):
        data[i] = data[i].split('\n',maxsplit=1)
        if len(data[i]) > 1:
            dic[data[i][0]] = data[i][1].replace('\n','')
    
    df = pd.DataFrame.from_dict(dic,orient='index')
    df.columns = ['Sequence']
    df = df.reset_index()
    df['Accession number'] = df['index'].apply(lambda name: name.split(' ')[0])
    df['Species'] = df['index'].apply(lambda name: name.split(' ')[1] + ' ' + name.split(' ')[2])
    df = df[['Accession number','Species','Sequence']]
    df = df.set_index('Species')
    df.reset_index(level=0, inplace=True)
    df['Species'] = df['Species'].apply(lambda s: s.replace(' ','-'))
    df['Length'] = df['Sequence'].apply(lambda seq: len(seq))
    df = amino_acids_count(df, amn_list)
    df['Split'] = df['Sequence'].apply(lambda seq: split_DNA(seq,300))
    return df 

def amino_plot(plot_list):
    return df[plot_list].plot(kind='bar', title ="V comp", figsize=(15, 10), legend=True, stacked=True,fontsize=12)

def tree_node_names(dnd_file, df):
    with open(dnd_file, 'r') as myfile:
        text=myfile.read()
    rep = df.set_index('Accession number').to_dict()['Species']
    for i, j in rep.items():
        text = text.replace(i, j)
    return text
