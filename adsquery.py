#import ads.sandbox as ads
import ads
import os
import datetime
import unicodedata
import sys

tfile = os.path.expanduser("~/.ads/dev_key") # ADS recommended dev key location. go to https://ui.adsabs.harvard.edu, set up an account, and get your own API token

# get current year to filter papers
curryear = int(datetime.date.today().year)

search_year = curryear

# if no year passed into command-line, search all SEEC papers until present
if len(sys.argv) > 1:
	search_year = sys.argv[1]
else:
	print("no year given, assuming current year")

datestr = str(search_year)

# function to strip accented characters out of ads name
def strip_accents(string):
	try:
		text = unicode(string, 'utf-8')
	except NameError:
		pass
	except TypeError:
		pass

	text = unicodedata.normalize('NFD', string).encode('ascii', 'ignore').decode("utf-8")

	return str(text)


authors = [
	"Brande, Jonathan",
]

# load api key
with open(tfile) as f:
	ads.config.token = f.readline()
	f.close()

# keywords to use to find papers
keywords = [
	"exoplanet",
	"exoplanets",
	"exoplanetary",
	"habitable",
	"habitability",
	"flare",
	"biosignature",
	"HZ",
	"early Earth",
	"hot Jupiter",
	"hot Jupiters",
	"secondary eclipse",
	"transit",
	"transits",
	"transiting",
	"transmission spectrum",
	"transmission spectra",
	"extrasolar planet",
	"extrasolar planets",
	"earth-like",
	"direct imaging",
	"planetary-mass",
	"super-earth",
	"super Earth",
	"neptune-sized",
	"earth-sized",
	"neptune-size",
	"earth-size",
]

# construct keyword query
qr = '('
for i in range(0, len(keywords)):
	if i < len(keywords) - 1:
		qr = qr + 'abs:"{}" OR '.format(keywords[i])
	else:
		qr = qr + 'abs:"{}")'.format(keywords[i])

papers = []
codes = []

# loop through authors, do a query for each author + keyword list
for auth in authors:
	if len(sys.argv) > 1:
		q = ads.SearchQuery(author=auth, q=qr, property="refereed", fl=['author', 'title', 'abstract', 'pub', 'pubdate', 'bibcode'], pubdate="{}".format(datestr))
	else:
		q = ads.SearchQuery(author=auth, q=qr, property="refereed", fl=['author', 'title', 'abstract', 'pub', 'pubdate', 'bibcode'])
	
	for paper in q:
		auth = paper.author
		title = paper.title
		abstract = paper.abstract
		journ = paper.pub
		date = paper.pubdate
		url = paper.bibcode

		if url in codes:
			pass
		else:
			papers.append({"authors": auth, "title": title, "abstract": abstract, "journal": journ, "date": date, "url": url})
			codes.append(url)
		

print(q.response.get_ratelimits())
print("bibcodes: {} papers: {}".format(len(codes), len(papers)))

for paper in papers:
	for field in paper:
		if paper[field] is None:
			paper[field] = ""

with open("publications.txt", "w+") as f:
	# print entries in some readable format
	for paper in papers:
		entry = '"{}"|{}|{} et al.|Contributing Authors: '.format(paper["title"][0].encode("utf-8"), paper["abstract"].encode("utf-8"), paper["authors"][0].encode("utf-8"))
		for name in paper["authors"][0:]:
			name = strip_accents(name)
			for author in authors:
				if (name.split(",")[0].lower() == author.split(",")[0].lower()) and (name.split(",")[1][:2].lower() == author.split(",")[1][:2].lower()):
					entry = entry + "{}; ".format(author)
		entry = entry + '|{}|{}|https://ui.adsabs.harvard.edu/#abs/{}\n'.format(paper['journal'].encode("utf-8"), paper["date"][:4], paper["url"].encode("utf-8"))
		
		f.write("{}".format(entry))
f.close()