from optimization_utils.graph.PageRank import PageRank
import glob
from crawl import get_download_path, return_citation
from graphviz import Graph
import os


def page_rank():
    page_rank = PageRank()
    for docs in glob.glob(get_download_path("*.txt")):
        docs = os.path.basename(docs).replace(".txt", "")
        page_rank.add_link(docs, list(return_citation(docs)))

    page_rank.calculate()

    return page_rank.node_rank


def create_graph():
    G = Graph('ER', filename='er.gv', engine='neato',
              graph_attr=dict(nodesep='12', edgesep="10",
                              concentrate="true", overlap="scale"),
              node_attr=dict(style="filled", fillcolor="white"))

    weight = {

    }
    for i in range(2):
        for docs in glob.glob("*.txt"):
            docs = os.path.basename(docs).replace(".txt", "")
            for edge in return_citation(docs):
                if docs == edge:
                    continue
                if i == 1:
                    G.edge(str(docs), str(edge))
                else:
                    weight[edge] = weight.get(edge, 0) + 1
    G.save("graph.png")

def get_recommended_papers():
    count = 10
    for i in sorted(page_rank().items(), key=lambda x: x[1], reverse=True)[:count]:
        print(i)
    print("=" * 12)


if __name__ == "__main__":
    #create_graph()
    get_recommended_papers()
