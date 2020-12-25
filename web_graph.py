import json

class Web_graph:
    '''A simple web_graph for web-crawling'''

    # This structure manages the Web graph generated during the visit and includes some methods,
    # written with the functional paradigm of python, for the calculation of the associated centralities.

    def __init__(self):
        self.nodes = {}

    def insert(self, url_key : str, ref_urls : list):
        self.nodes[url_key] = ref_urls

    def get_graph(self): return self.nodes

    def print_graph(self):
        for key in list(self.nodes.keys()):
            print('Node ' + key + ' refers:')
            print(self.nodes[key])

    def print_metrics(self):

        centralities = {}

        for key in list(self.nodes.keys()):
            centralities[key] = {'indegree' : self.indegree_metric(key), 'closeness' : self.closeness_metric(key), 'harmonic_centrality' : self.harmonic_centrality_metric(key)}
            print(key + ' indegree is: ' + centralities[key]['indegree'])
            print(key + ' closeness is: ' + centralities[key]['closeness'])
            print(key + ' harmonic_centrality is: ' + centralities[key]['harmonic_centrality'])

        with open('centralities.txt', 'w') as file:
            json.dump(obj=centralities, indent=4, sort_keys=True, fp=file)


    def indegree_metric(self, key):
        return len([x for x in list(self.nodes.keys()) if key in self.nodes[x]])

    def closeness_metric(self, key):
        return 1/self.no_zero(sum([self.distance(x,key,[]) for x in list(self.nodes.keys()) if x != key and self.distance(x,key,[]) is not None]))

    def harmonic_centrality_metric(self, key):
        return sum([ (1/self.distance(x, key,[])) for x in list(self.nodes.keys()) if x != key and self.distance(x, key,[]) is not None])




    def distance(self,x,y,visited_nodes):
        #distance from x to y, y target

        #exit conditions:
        if x not in list(self.nodes.keys()): return None
        if not self.nodes[x]: return None

        if x in visited_nodes: return None


        if x == y: return 0

        if(y in self.nodes[x]): #atomic case
            return 1
        else:
            return self.sum_or_none(1,[self.distance(x_son, y, visited_nodes + [x]) for x_son in self.nodes[x] if self.distance(x_son, y, visited_nodes + [x]) is not None])

    def no_zero(self, x):
        if x==0:
            return -1
        else:
            return x

    def sum_or_none(self, x, y : list):
        if y:
            return x + min(y)
        else:
            return None