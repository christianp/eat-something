from textblob import TextBlob
from itertools import groupby
import re
from markdown2 import markdown

measurements = [
    'lb',
    'pound',
    'pounds',
    'g',
    'kg',
    'l',
    'ml',
    'litre',
    'litres',
    'tsp',
    'teaspoon',
    'teaspoons',
    'tbsp',
    'tablespoon',
    'tablespoons',
    'cup',
    'cups',
    'piece',
    'pieces',
]

def analyse_line(line):
    w = TextBlob(line)
    for sentence in w.parse().split():
        out = []
        for word,tag,chunk,relation in sentence:
            #print('\t'.join([word,tag,chunk,relation]))
            chunk = chunk.split('-')[-1]
            relation = relation.split('-')[-1]
            l = None
            if chunk in ['NP','PP'] and relation!='PNP':
                if tag=='CD' or word in measurements:
                    l = 'quantity'
                else:
                    l = 'thing'
            elif tag not in ',.?!':
                l = 'action'

            out.append((word,l))
        yield out

def clean_line(line):
    line = re.sub(r'^\W*\s*','',line)
    line = re.sub(r'^(\d+)(g|kg|l|ml) ',r'\g<1> \g<2> ',line)
    return line
        
def show_bit(g,words):
    text = ' '.join(w[0] for w in words)
    if g is not None:
        return '<span class="{}">{}</span>'.format(g,text)
    else:
        return text

def html_ingredients(text):

    lines = [clean_line(line) for line in text.split('\n') if not re.match('^#',line)]
    lines = text.split('\n')

    out = []
    for line in lines:
        if re.match('^#',line):
            out.append(markdown(line))
        elif line.strip():
            o_line = []
            line = clean_line(line)
            for sentence in analyse_line(line):
                s = ''
                for g,words in groupby(sentence,key=lambda x:x[1]):
                    if s and g is not None:
                        s += ' '
                    s += show_bit(g,words)
                o_line.append(s)
            out.append('<p class="line">{}</p>'.format('. '.join(o_line)))

    return '\n'.join(out)
