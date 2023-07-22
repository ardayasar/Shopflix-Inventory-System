import json

settings = {
    'dataset': 'priceList.json'
}

dataset = open(settings['dataset'], 'r')
datasetRaw = dataset.read()
datasetJSON = json.loads(datasetRaw)
total = 0
for category in datasetJSON:
    print(category, len(datasetJSON[category]['products']))
    total += len(datasetJSON[category]['products'])

print('Total: ', total)