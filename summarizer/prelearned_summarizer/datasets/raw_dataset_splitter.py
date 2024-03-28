from io import TextIOWrapper
import os

from tqdm import tqdm

location = os.path.dirname(__file__)

with open(location + "/lenta-ru-news.csv", "r", encoding="utf-8") as input_file:
# with open(location + "/lenta-sample.csv", "r", encoding="utf-8") as input_file:
    with open(location + "/part1.csv", "w", encoding="utf-8") as output_file_1:
        with open(location + "/part2.csv", "w", encoding="utf-8") as output_file_2:
            for i, line in tqdm(enumerate(input_file), total=868645, ncols=100):
                if i < 400000:
                    output_file_1.write(line)
                else:
                    output_file_2.write(line)
