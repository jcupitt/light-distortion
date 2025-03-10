#!/usr/bin/env python3

import sys
import re
from typing import Tuple, List

import pyvips

Point = List[int]
Couple = tuple[Point, Point]


def shepards(image: pyvips.Image, couples: List[Couple]):
    index = pyvips.Image.xyz(image.width, image.height)
    deltas = []
    weights = []

    for p1, p2 in couples:
        diff = index - p2

        distance = (diff[0]**2 + diff[1]**2)

        weight = (distance < 1.0).ifthenelse(1.0, 1.0 / distance)
        weights.append(weight)

        delta = [(p1[0] - p2[0]), (p1[1] - p2[1])] * weight
        deltas.append(delta)

    # add, normalize
    index += pyvips.Image.sum(deltas) / pyvips.Image.sum(weights)

    return image.mapim(index, interpolate=pyvips.Interpolate.new('bicubic'))


if __name__ == "__main__":
    image = pyvips.Image.new_from_file(sys.argv[1])

    matches = re.findall(r'(\d+),(\d+) (\d+),(\d+)', sys.argv[3])
    couples = [[[int(match[0]), int(match[1])], [int(match[2]), int(match[3])]]
               for match in matches]

    image = shepards(image, couples)
    image.write_to_file(sys.argv[2])
