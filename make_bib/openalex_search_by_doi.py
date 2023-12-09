#!/usr/bin/python3
import requests
import json
import yaml
import sys
import pandas as pd

DBG = 1

# write a Python program that downloads an Excel document in my OneDrive folder

def openalex_query(url, query, limit=None):
    if DBG>=1:
        print(f"query url={url}, query={query}")
    per_page = 200
    if limit is not None:
        per_page = min(per_page, limit)
    cursor = "*"
    count = 0
    results = []
    i = 0
    while 1:
        if cursor is None:
            print(f"reply['meta'] has no next_cursor field: {rep}")
            break
        q = { "page" : None, "per-page": per_page, "cursor" : cursor }
        q.update(query)
        rep = requests.get(url, q).json()
        meta = rep.get("meta")
        if DBG>=2:
            print(f"meta {i} {count} = {meta}")
        if meta is None:
            if DBG>=2:
                print(f"reply has no meta field: {rep}")
            break
        cursor = meta.get("next_cursor")
        rep_results = rep.get("results")
        if rep_results is None:
            print(f"reply has no results field: {rep}")
            break
        if len(rep_results) == 0:
            break
        for result in rep_results:
            # results.append(result)
            yield result
            count += 1
            if count == limit:
                break
        if count == limit:
            break
        i += 1
    return results

def find_work_of_doi(doi, limit=None):
    works = openalex_query('https://api.openalex.org/works',
                           { "filter" : f"doi:{doi}" },
                           limit=limit)
    works = list(works)
    n_works = len(works)
    if n_works == 0:
        print(f"work of doi:{doi} not found", file=sys.stderr)
        return None
    if n_works > 1:
        print(f"{n_works} (> 1) works of doi:{doi} found, take the first", file=sys.stderr)
    return works[0]

def format_work(work):
    if DBG>=1:
        ym = yaml.dump(work["locations"], Dumper=yaml.CDumper)
        print(ym)
    title = work.get("title", "(unknown title)")
    pub_year = work.get("publication_year", "(unknown publication year)")
    prim_loc = work.get("primary_location", {})
    source = prim_loc.get("source", {})
    if source is None:
        venue_name = "?"
    else:
        venue_name = source.get("display_name", "?")
    authors = [author['author']['display_name'] for author in work.get("authorships", [])]
    authors = ", ".join(authors)
    return f"{authors}. _{title}_. {venue_name}. {pub_year}"

def format_work_dict(doi, work):
    if DBG>=1:
        ym = yaml.dump(work["locations"], Dumper=yaml.CDumper)
        print(ym)
    title = work.get("title")
    pub_year = work.get("publication_year")
    prim_loc = work.get("primary_location", {})
    source = prim_loc.get("source", {})
    if source is None:
        venue_name = "?"
    else:
        venue_name = source.get("display_name", "?")
    authors = [author['author']['display_name'] for author in work.get("authorships", [])]
    authors = ", ".join(authors)
    return {"doi" : doi, "title" : title, "year" : pub_year, "venue" : venue_name, "authors" : authors}

def read_dois_from_excel(xlsx):
    df = pd.read_excel(xlsx)
    dois = list(df["doi または 論文の landing page"])
    return dois

def main():
    dois = [
        "10.14778/3587136.3587141",
        "10.14778/3603581.3603583",
        "10.1587/transinf.2022DAP0011",
        "10.3390/app131810132",
        "10.1587/transinf.2023EDP7050",
        "10.1007/978-3-031-37586-6_12",
        "10.1109/CSF57540.2023.00034",
        "10.1145/3580305.3599889",
        "10.1109/ICASSP49357.2023.10096844",
        "10.1145/3581784.3607049",
        "10.1109/ICDEW58674.2023.00026",
    ]
    xlsx = "onedrive/secure-privacy-crest/共有情報/publication.xlsx"
    dois = read_dois_from_excel(xlsx)
    works = []
    for i, doi in enumerate(dois):
        print(f"=== {i} ===")
        work = find_work_of_doi(doi)
        works.append(format_work_dict(doi, work))
    df = pd.DataFrame(works)
    df.to_excel("bib_data.xlsx")

main()


