# -*- coding: utf-8 -*-

import argparse
import os
import csv

from tqdm import tqdm

csv.field_size_limit(1000000000)

if __name__ == '__main__':

    TARGET_SITES = ["engadget", "researchblogging", "techcrunch", "wired"]

    parser = argparse.ArgumentParser(description="make single csv file from scraped data")
    parser.add_argument("site", choices=TARGET_SITES)
    args = parser.parse_args()

    target_dir = args.site + "_data"
    target_dir_path = os.path.join(os.path.dirname(os.path.realpath("__file__")), target_dir)

    files = os.listdir(target_dir_path)
    scraped_data_list = []
    print("[ LOAD ] Load from scraped data.")
    for file in tqdm(files):
        with open(os.path.join(target_dir_path, file), "r") as rf:
            reader = csv.reader(rf)

            for row in reader:
                scraped_data_list.append(row)

    print("[ CLEAN ] strip '\\n' symbols.")
    for i, scraped_data in tqdm(enumerate(scraped_data_list)):
        scraped_data_list[i][2] = scraped_data[2].replace("\n", " ")

    output_file = "merged_" + args.site + "_data.csv"
    print("[ DUMP ] Dump scraped data to single csv file.")
    with open(output_file, "w") as wf:
        writer = csv.writer(wf)

        for scraped_data in tqdm(scraped_data_list):
            writer.writerow(scraped_data)
