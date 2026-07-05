from data.Dataset import dataset, label2id

labels = []
texts = []
for item in dataset:

    texts.append(item[ "text" ])

    labels.append(label2id[item["label"]])