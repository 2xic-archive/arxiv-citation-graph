import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import re
import glob
import os
from graphviz import Digraph
import networkx as nx
import matplotlib.pyplot as plt
import os
import urllib.request
import time
import random
from graphviz import Graph

def download_name(name):
	if not os.path.isfile("{}.pdf".format(name)):
		url = "https://arxiv.org/pdf/{}.pdf".format(name)
		print("Downloading {}".format(url))
		urllib.request.urlretrieve(url, "{}.pdf".format(name))
		return "{}.pdf".format(name)
	return None

def return_citation(doc):
	doc_name = "{}.txt".format(doc) if not ".txt" in doc else doc
	text = open(doc_name, "r").read()
	citation = re.findall(r"arXiv:\d*.\d*", text)
	for i in citation:
		yield i.replace("arXiv:", "")

def create_txt():
	for docs in glob.glob("*.pdf"):
		if not os.path.isfile(docs.replace(".pdf", ".txt")):
			os.system("pdftotext {} {}".format(docs, docs.replace(".pdf", ".txt")))

def crawl_some():
	for docs in glob.glob("*.txt"):
		for citation in return_citation(docs):
			doc_name = download_name(citation)
			if not doc_name is None:
				os.system("pdftotext {} {}".format(doc_name, doc_name.replace(".pdf", ".txt")))
				# a nice crawler that takes a break
				time.sleep(random.randint(2, 5))

def page_rank():
	docs_citation = {

	}
	doc_rank = {

	}
	for docs in glob.glob("*.txt"):
		docs = docs.replace(".txt", "")
		docs_citation[docs] = list(return_citation(docs))
		doc_rank[docs] = 1

	for docs, citations in docs_citation.items():
		new_rank = 0.2
		for citation_doc in citations:
#			print(citation_doc)
			if not citation_doc in docs_citation:
				continue
			citation_doc_rank = doc_rank[citation_doc]
			citaiton_count = len(docs_citation[citation_doc])
			new_rank += (0.8) * (citation_doc_rank / citaiton_count)
		doc_rank[docs] = new_rank
	return doc_rank

def create_grapth():
	G = Graph('ER', filename='er.gv', engine='neato',
		graph_attr=dict(nodesep='12', edgesep="10", concentrate="true", overlap="scale"),#, splines="true"),
		node_attr=dict(style="filled",fillcolor="white"))

	weigth = {
		
	}
	for i in range(2):
		for docs in glob.glob("*.txt"):
			docs = docs.replace(".txt", "")
			for edge in return_citation(docs):
				if docs == edge:
					continue
				if i == 1:
					G.edge(str(docs), str(edge))
				else:
					weigth[edge] = weigth.get(edge, 0) + 1
	G.save("readme.png")

	count = 10
	print("=" * 12)
	for i in sorted(weigth.items(), key=lambda x: x[1], reverse=True)[:count]:
		print(i)
	print("=" * 12)
	for i in sorted(page_rank().items(), key=lambda x: x[1], reverse=True)[:count]:
		print(i)
	print("=" * 12)

if __name__ == "__main__":
	#crawl_some()
	#create_txt()
	create_grapth()
