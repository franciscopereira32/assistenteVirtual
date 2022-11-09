import yaml
import numpy as np

data = yaml.safe_load(open('nlu\\trem.yml', 'r', encoding='utf-8').read())

inputs, outputs = [], []

for command in data['commands']:
    inputs.append(command['input'].lower())
    outputs.append('{}\{}'.format(command['entity'], command['action']))

#processar texto

chars = set()

for input in inputs + outputs:
    for ch in input:
        if ch not in chars:
            chars.add(ch)

#mapear char-idx

chr2idx= {}
idx2chr= {}

for i, ch in enumerate(chars):
    chr2idx[ch] = i 
    idx2chr[i]  = ch

#print("Numero de caracterares: ", len(chars))
   
max_seq = max([len(x) for x in inputs])

print("Numero de cahrs: ", len(chars))
print("Maior seq: ", max_seq)

#criar dataset one-hot(numero de exemplo, tamanho da seq, num caracteres)

input_data = np.zeros((len(inputs), max_seq, len(chars)), dtype='int32')     

for i, input in enumerate(inputs):
    for k, ch in enumerate(input):
        input_data[i, k, chr2idx[ch]] = 1.0

print(input_data[0])