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

def xxx_format_work(work):
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

def xxx_format_work_dict(doi, work):
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

def xxx_read_dois_from_excel(xlsx):
    df = pd.read_excel(xlsx)
    dois = list(df["doi または 論文の landing page"])
    return dois

def xxx_find_col(work, col):
    if col == "title":
        return work.get("title")
    elif col == "year":
        return work.get("publication_year")
    elif col == "venue":
        prim_loc = work.get("primary_location")
        if prim_loc is None:
            return None
        source = prim_loc.get("source")
        if source is None:
            return None
        return source.get("display_name")
    elif col == "authors":
        authors = [author['author']['display_name'] for author in work.get("authorships", [])]
        authors = ", ".join(authors)
        return authors
    else:
        assert(0), col

def any_data_missing(row, cols):
    for col in cols:
        if pd.isnull(row[col]):
            return 1
    return 0

def lookup_database(row, cols):
    doi = row["doi または 論文の landing page"]
    work = find_work_of_doi(doi)
    if work is None:
        return row
    if DBG>=1:
        ym = yaml.dump(work["locations"], Dumper=yaml.CDumper)
        print(ym)
    for col in cols:
        if pd.isnull(row[col]):
            row[col] = find_col(work, col)
    return row

def complement_bib(df):
    """
    complement missing cells in the bibliography dataframe
    """
    rows = []
    necessary_cols = ["title", "year", "venue", "authors"]
    for i, row in df.iterrows():
        if any_data_missing(row, necessary_cols):
            new_row = lookup_database(row, necessary_cols)
        else:
            new_row = row
        rows.append(new_row)
    return pd.DataFrame(rows)

def main():
    # in_xlsx = "onedrive/secure-privacy-crest/5Publications/publications.xlsx"
    # out_xlsx = "onedrive/secure-privacy-crest/5Publications/publications_output.xlsx"
    in_xlsx = sys.argv[1]
    out_xlsx = sys.argv[2]
    in_df = pd.read_excel(in_xlsx)
    out_df = complement_bib(in_df)
    out_df.to_excel(out_xlsx, index=False)
    
main()
