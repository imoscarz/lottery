import random
import os
import time
import csv
import codecs
import heapq
from config import *


class Item:
    def __init__(self, item, weight: int, image):
        self.item = item
        self.weight = weight
        self.image = image


def read_from_csv():
    items_converted = []
    with codecs.open('item.csv', encoding='utf-8') as f:
        items = csv.DictReader(f, skipinitialspace=True)
        for i in items:
            items_converted.append(
                Item(i['item'], int(i['weight']), i['image']))
    return items_converted


def a_res(samples, m):
    """
    :samples: [(item, weight), ...]
    :k: number of selected items
    :returns: [(item, weight), ...]
    """
    heap = []  # [(new_weight, item), ...]
    for sample in samples:
        wi = sample[1]
        ui = random.uniform(0, 1)
        ki = ui ** (1/wi)

        if len(heap) < m:
            heapq.heappush(heap, (ki, sample))
        elif ki > heap[0][0]:
            heapq.heappush(heap, (ki, sample))

            if len(heap) > m:
                heapq.heappop(heap)
    return [item[1] for item in heap]


def get_items(n: int):
    items = read_from_csv()
    samples = [(sample, sample.weight) for sample in items]
    return [sample[0] for sample in a_res(samples, n)]


if __name__ == "__main__":
    print(read_from_csv())
    while True:
        l = [i[0].item for i in get_items(2)]
        print(l[0] == l[1])
