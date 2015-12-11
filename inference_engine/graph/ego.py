# Title: Egonet
# Version 0.1
# Andrew Conway <conway_andrew@bah.com>
# Description: Extracts the Egonet of a given node.  An egonet is
# the subgraph induced by the set of a focal's neighbors. That is the network
# that consists of all the neighbors and the connections between them.
# G = Input network
# n = focal node of egonet extract
# focal = Boolean to include focal network in extract, default=True
__author__ = """Andrew Conway (conway_andrew@bah.com)"""

# DW: modifications to work with new networkx API, use edge weights

import networkx as nx

def egonet(G,n,focal=True):
    H = nx.Graph()                          # Subgraph to be returned
    neig = G.neighbors(n)       # Set of n's neighbors
    H.add_nodes_from(neig)

    star = G.edges(n)      # Edges connecting n to neighbors
    star_ebunch = [(e[0], e[1], G.get_edge_data(e[0], e[1])['weight']) for e in star]
    H.add_weighted_edges_from(star_ebunch)

    # Add edges among ego's neighbors (alters)
    peripheral_ebunch = []
    for i in range(0,len(neig)):
        v = neig[i]
        v_n = G.neighbors(v)
        for j in range(0,len(v_n)):
            if v_n[j] in neig:
                peripheral_ebunch.append((v, v_n[j], G.get_edge_data(v, v_n[j])['weight']))

    H.add_weighted_edges_from(peripheral_ebunch)

    if focal:
        return H
    else:
        H.remove_node(n)
        return H
