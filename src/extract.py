import json


from extraction import *

path = 'data/raw'

chars = chars_from_pages("book.pdf", 3, 12)
tokens = list(get_tokens(chars))
entries = parse_index(tokens)

index = {}
for e in entries:
    if e[0].type == Literals.BOLD_ITALIC:
        index[e[0].text] = int(e[-1].text)
    else:
        index["[" + e[1].text + "]"] = int(e[-1].text)



with open(f'{path}/index.json', 'w') as f:
    json.dump(index, f)



items = list(index.items())

results = {}

for i in range(len(items)):
    start = items[i][1] + 22
    end = items[i+1][1] + 21 if i < len(items) - 1 else 1334
    chars = chars_from_pages("book.pdf", start, end)
    tokens = get_tokens(chars)

    offset = 0
    total = 0
    for j, t in enumerate(tokens):
        if t.text == 'Taxones:' or t.text == 'excluidos:':
            total += int(tokens[j + 2].text.strip('.'))

        if t.text == 'joangelitog@gmail.com':
            offset = j
            break




    plants = get_plants(tokens[offset + 2:])
    # print(str(start) + " - " + str(end))
    # print(items[i][0])
    # print(len(plants))
    # print(total)
    print(str(i) + ' --- ' + items[i][0])
    results[items[i][0]] = plants
    if (i != 223):
        assert len(plants) == total

with open(f'{path}/raw_data.json', 'w') as f:
    json.dump(results, f)