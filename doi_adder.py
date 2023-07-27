import requests
import bibtexparser

def find_doi(title):
    """Find the DOI of a paper given its title by querying the Crossref API."""
    headers = {
        "User-Agent": "My Library Client",
    }
    res = requests.get(f"https://api.crossref.org/works?query.title={title}", headers=headers)
    try:
        doi = res.json()['message']['items'][0]['DOI']
        return doi
    except (KeyError, IndexError):
        print(f"Could not find DOI for title: {title}")
        return None

def add_doi_to_bib(bib_file_path, new_bib_file_path):
    """Open a .bib file, find DOIs for entries, and write to a new .bib file."""
    with open(bib_file_path, 'r', encoding='utf-8') as bib_file:  # specify encoding here
        bib_database = bibtexparser.load(bib_file)

        for entry in bib_database.entries:
            print(entry)
            # If there's already a DOI, skip this entry
            if 'doi' in entry:
                continue
            title = entry.get('title')
            if title:
                doi = find_doi(title)
                if doi:
                    entry['doi'] = doi

    with open(new_bib_file_path, 'w', encoding='utf-8') as new_bib_file:  # and here
        bibtexparser.dump(bib_database, new_bib_file)

# Usage
add_doi_to_bib("your_file_name.bib", "new.bib")
