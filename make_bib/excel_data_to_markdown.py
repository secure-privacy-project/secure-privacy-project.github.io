#!/usr/bin/python3
import pandas as pd
import sys

DBG = 1

def make_markdown_citation(row):
    d = dict(row)
    d["url"] = d.get("doi または 論文の landing page")
    if d["url"]:
        d["title_url"] = "[{title}]({url})".format(**d)
    else:
        d["title_url"] = title
    print(d)
    return '{authors}. "{title_url}." _{venue}._ {year}.'.format(**d)

def main():
    #in_xlsx = "onedrive/secure-privacy-crest/5Publications/publication.xlsx"
    #out_md = "citations.md"
    in_xlsx = sys.argv[1]
    out_md = sys.argv[2]
    df = pd.read_excel(in_xlsx)
    df = df.fillna('')
    citations = []
    for i, row in df.iterrows():
        citations.append(make_markdown_citation(row))
    wp = open(out_md, "w")
    wp.write("\n".join([f" 1. {citation}" for citation in citations]))
    wp.close()

main()

