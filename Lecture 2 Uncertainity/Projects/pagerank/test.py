from pagerank import transition_model,crawl


if len(sys.argv) != 2:
    sys.exit("Usage: python pagerank.py corpus")
corpus = crawl(sys.argv[1])
print(corpus)
trans = transition_model(corpus,"1.html",0.85)
print(trans)