import yaml
import numpy as np

data = yaml.safe_load(open('nlu\\trem.yml', 'r', encoding='utf-8').read())

inputs, outputs = [], []

for command in data['commands']:
    inputs.append(command['input'].lower())
    outputs.append('{}\{}'.format(command['entity'], command['action']))

#processar texto

chars = set()

ch = inputs + outputs

for input in inputs + outputs:
    if input not in ch:
       chars.add(ch)

print(inputs)
print(outputs)
print('Número de chars: ', len(chars))





'''
print(inputs)
print(outputs)
'''