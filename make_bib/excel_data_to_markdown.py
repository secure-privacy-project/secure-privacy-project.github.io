#!/usr/bin/python3
import pandas as pd

DBG = 1

def make_markdown_citation(row):
    d = dict(row)
    print(d)
    return '{authors}. "{title}." _{venue}._ {year}.'.format(**d)

def main():
    xlsx = "out.xlsx"
    df = pd.read_excel(xlsx)
    citations = []
    for i, row in df.iterrows():
        citations.append(make_markdown_citation(row))
    wp = open("citations.md", "w")
    wp.write("\n".join([f" 1. {citation}" for citation in citations]))
    wp.close()

main()

