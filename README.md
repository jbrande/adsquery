# ADS Query Script Guide

### Description:
"adsquery.py" is a Python 2 script used to query the SAO/NASA Astrophysics Data System (https://ui.adsabs.harvard.edu/) for all refereed papers first-authored or coauthored by a specific scientist or list of scientists. This script also uses a list of keywords to search each author's abstracts to make sure the returned results are topical, or relate to the correct author (if two authors have the same names but work in different subfields). Author names as returned from ADS are also scrubbed of special characters to make sure names are properly matched.

Originally, this was written to query all papers by the members of the Sellers Exoplanet Environments Collaboration (https://seec.gsfc.nasa.gov). SEEC specific info has been scrubbed in favor of general information.

### Dependencies: 
- ads 			(https://ads.readthedocs.io/en/latest/)
- os 			(Python Standard Library)
- datetime		(Python Standard Library)
- unicodedata	(Python Standard Library)
- sys 			(Python Standard Library)

This script also requires the presence of a file containing the ADS API key. This key should not be exposed to non-SEEC users (i.e. accidentally uploaded to GitHub or other public repositories). If this happens, generate a new API key by following the instructions at the ADS website (IIRC, this needs to happen while logged in to the ADS site under the SEEC account). Currently, the script expects the file location "~/.ads/dev_key", where "dev_key" is a file containing only the API key.

### Usage:
The script can be run by the command "python adsquery.py YYYY", where YYYY is an optional argument specifying the 4 digit year to search. If no year is given, the script will automatically search the current year.

### Outputs:
The output is a text file (publications.txt) containing the returned papers in a particular file format:
- Title|Abstract|First Author et al.|Contributing Authors: List of Authors|Journal|Year|URL

Each entry is printed on a new line, which can then be parsed to get individual entries on the SEEC website.