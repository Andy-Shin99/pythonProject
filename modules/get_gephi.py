import pandas as pd
import numpy as np
import networkx as nx
import operator

class MakeGraphml:
    def make_graphml(self, pair_file, graphml_file):
        out = open(graphml_file, 'w', encoding = 'utf-8')
        entity = []
        e_dict = {}
        count = []
        for i in range(len(pair_file)):
            e1 = pair_file.iloc[i,0]
            e2 = pair_file.iloc[i,1]
            #frq = ((word_dict[e1], word_dict[e2]),  pair.split('\t')[2])
            frq = ((e1, e2), pair_file.iloc[i,2])
            if frq not in count: count.append(frq)   # ((a, b), frq)
            if e1 not in entity: entity.append(e1)
            if e2 not in entity: entity.append(e2)
        print('# terms: %s'% len(entity))
        #create e_dict {entity: id} from entity
        for i, w in enumerate(entity):
            e_dict[w] = i + 1 # {word: id}
        out.write(
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?><graphml xmlns=\"http://graphml.graphdrawing.org/xmlns\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://graphml.graphdrawing.org/xmlnshttp://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd\">" +
            "<key id=\"d1\" for=\"edge\" attr.name=\"weight\" attr.type=\"double\"/>" +
            "<key id=\"d0\" for=\"node\" attr.name=\"label\" attr.type=\"string\"/>" +
            "<graph id=\"Entity\" edgedefault=\"undirected\">" + "\n")
        # nodes
        for i in entity:
            out.write("<node id=\"" + str(e_dict[i]) +"\">" + "\n")
            out.write("<data key=\"d0\">" + i + "</data>" + "\n")
            out.write("</node>")
        # edges
        for y in range(len(count)):
            out.write("<edge source=\"" + str(e_dict[count[y][0][0]]) + "\" target=\"" + str(e_dict[count[y][0][1]]) + "\">" + "\n")
            out.write("<data key=\"d1\">" + str(count[y][1]) + "</data>" + "\n")
            #out.write("<edge source=\"" + str(count[y][0][0]) + "\" target=\"" + str(count[y][0][1]) +"\">"+"\n")
            #out.write("<data key=\"d1\">" + str(count[y][1]) +"</data>"+"\n")
            out.write("</edge>")
        out.write("</graph> </graphml>")
        print('now you can see %s' % graphml_file)
        #pairs.close()
        out.close()

duration_list = ['20160101to20161231', '20170101to20171231', '20180101to20181231', '20190101to20191231','20200101to20201231', '20210101to20211231', '20220101to20221231', '20230101to20231110']

for duration in duration_list :
    count = {}

    f = open('results//title_results_new//' + duration[:4] + '.txt', 'r', encoding='utf-8')
    for line in f :
        line = line.strip()
        (k, v) = line.split(': ')
        k = k.strip("() \'")
        k = k.split("\', '")
        print(k)
        a = k[0]
        b = k[1]
        count[(a, b)] = int(v)

    df = pd.DataFrame.from_dict(count, orient='index')
    list1 = []
    for i in range(len(df)) :
        list1.append([df.index[i][0], df.index[i][1], df[0][i]])

    df2 = pd.DataFrame(list1, columns = ['term1', 'term2', 'freq'])
    df3 = df2.sort_values(by=['freq'], ascending=False)

    len((np.where(df3['freq']>=5))[0])

    G=nx.Graph()
    for i in range(len(df3)):
        #print(pair)
        G.add_edge(df3['term1'][i], df3['term2'][i], weight=int(df3['freq'][i]))
    
    # Compute centralities for nodes.
    # The degree centrality values are normalized by dividing by the maximum possible degree in a simple graph n-1 where n is the number of nodes in G.
    dgr = nx.degree_centrality(G)
    btw = nx.betweenness_centrality(G)
    cls = nx.closeness_centrality(G)

    # itemgetter(0): key 또는 itemgetter(1): value로 sort key, reverse=True (descending order)
    sorted_dgr = sorted(dgr.items(), key=operator.itemgetter(1), reverse=True)
    sorted_btw = sorted(btw.items(), key=operator.itemgetter(1), reverse=True)
    sorted_cls = sorted(cls.items(), key=operator.itemgetter(1), reverse=True)
    print("** degree **")
    for x in range(4):
        print(sorted_dgr[x])
    print("** betweenness **")
    for x in range(4):
        print(sorted_btw[x])
    print("** closeness **")
    for x in range(4):
        print(sorted_cls[x])

        gm = MakeGraphml()
        graphml_file = 'results//graphml_results//' + duration[:4] + '.graphml'

        gm.make_graphml(df3.iloc[0:len(df3),:], graphml_file)