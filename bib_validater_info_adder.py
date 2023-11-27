import bibtexparser
import requests
import json

def search_crossref(title, authors):
    """
    Search CrossRef for the given title and authors.
    Returns the DOI if a match is found, otherwise returns None.
    """
    try:
        query = f"title:{title} AND author:{authors}"
        url = f"https://api.crossref.org/works?query.bibliographic={query}"
        response = requests.get(url, timeout=10)  # Adding a timeout of 10 seconds
        if response.status_code == 200:
            data = response.json()
            items = data.get("message", {}).get("items", [])
            if items:
                # Assuming the first match is the correct one
                return items[0].get("DOI")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return None


def is_valid_entry(entry):
    title = entry.get('title')
    authors = ' and '.join(entry.get('author', '').split(' and '))  # Format authors for query
    if not title or not authors:
        return False, "Missing title or authors"

    doi = entry.get('doi')
    crossref_doi = search_crossref(title, authors)

    if crossref_doi:
        if doi != crossref_doi:
            entry['doi'] = crossref_doi  # Adding or updating DOI
            return True, "DOI added or updated"
        return True, "Valid"
    else:
        return False, "No match found in CrossRef"

def validate_bibtex_file(file_path):
    with open(file_path, encoding='utf-8') as bibtex_file:
        bibtex_database = bibtexparser.load(bibtex_file)

    for entry in bibtex_database.entries:
        is_valid, reason = is_valid_entry(entry)
        if not is_valid:
            print(f"Entry '{entry.get('ID', 'Unknown ID')}' is invalid: {reason}")

    # Writing back the entries with updated DOIs
    with open(file_path, 'w', encoding='utf-8') as bibtex_file:
        bibtexparser.dump(bibtex_database, bibtex_file)

# Replace 'your_bibtex_file.bib' with the path to your BibTeX file
validate_bibtex_file('ref copy.bib')
