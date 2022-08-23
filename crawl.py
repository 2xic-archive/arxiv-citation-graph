import argparse
import random
import time
import urllib.request
import os
import glob
import re
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def get_download_path(name):
    if "/" in name:
        return name
    return os.path.join(
        os.path.dirname(__file__),
        "download",
        name
    )


def download_raw(name):
    path = get_download_path("{}.pdf".format(name))
    if not os.path.isfile(path):
        url = "https://arxiv.org/pdf/{}.pdf".format(name)
        print("Downloading {}".format(url))
        urllib.request.urlretrieve(
            url, path)
        return path
    return path


def download_process(name):
    doc_name = download_raw(name)
    if not doc_name is None and not os.path.isfile(doc_name.replace(".pdf", ".txt")):
        os.system("pdftotext {} {}".format(
            doc_name, doc_name.replace(".pdf", ".txt")))
        # a nice crawler that takes a break
        time.sleep(random.randint(2, 5))


def return_citation(doc):
    doc_name = "{}.txt".format(doc) if not ".txt" in doc else doc
    text = open(get_download_path(doc_name), "r").read()
    citation = re.findall(r"arXiv:\d*.\d*", text)
    for i in citation:
        yield i.replace("arXiv:", "")


def create_txt():
    for docs in glob.glob(get_download_path("*.pdf")):
        if not os.path.isfile(docs.replace(".pdf", ".txt")):
            os.system("pdftotext {} {}".format(
                docs, docs.replace(".pdf", ".txt")))


def crawl_some(max=100):
    downloads = 0
    while True:
        for docs in glob.glob(get_download_path("*.txt")):
            for citation in return_citation(docs):
                download_process(citation)
                downloads += 1

            if downloads < max:
                break
        downloads += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Crawl arxiv papers from citations')
    parser.add_argument('seed', type=str,
                        metavar='seed',  nargs='+',
                        help='seed papers')
    parser.add_argument('--max-crawl', dest='max',
                        help='max papers to download',
                        required=True)

    args = parser.parse_args()

    for i in args.seed:
        download_process(i)

    crawl_some(int(args.max))
