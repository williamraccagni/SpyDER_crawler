# SpyDER: an Academic Web Crawler written in python 3.x

# Non-python files explanation:
# - pages directory is used for temporary store and parsing of webpages fetched by threads
# - robots directory is used for temporary store and parsing of robots.txt files associated to hosts fetched by threads
# - The thread status folder collects files in chronological order that describe the thread work involved
#   in executing and retrieving urls from the frontier execution queue.
# - seed.txt contains the starting urls from which to start the execution.
#   The topic chosen for the test is the coronavirus pandemic.
# - keys.txt contains the keywords related to the topic chosen for the search of the pages,
#   these must contain at least one keyword within the text to be considered valid.
#   The topic chosen for the test is the coronavirus pandemic.
# - robots_parser.awk is an awk script for extracting robots.txt rules
#   which describe the pages accessible for a given host.
# - href_urls_extractor.awk is an awk script for extracting href url from a page.
# - centralities.txt contains the results of the centralities of the Web Graph nodes.



import seed_loader as sl
import sieve as sv
import frontier as fr
import url_filter as uf
import web_graph as wg

if __name__ == '__main__':

    #Parameters
    sieve_limit = 10 # max number of urls in the sieve
    host_politeness = 60.0 # seconds to wait before visit the host again, float type
    requests_number = 5 # max number of urls, associated with an host, to visit
    number_of_threads = 4 # max number of active threads

    # Data structures instantiation
    seed = uf.fs_url_filter(sl.load('seed.txt')) # Seed instantiation and loading
    web_graph = wg.Web_graph() # WebGraph instantiation for Centralities

    frontier = fr.Frontier(sv.Sieve(seed, sieve_limit), host_politeness, requests_number, web_graph) # Frontier instantiation with data structures and Parameters


    # Execution
    print('Crawler Execution\n')
    frontier.execute(number_of_threads)



    #Centrality Measures
    print('\nCentralities:\n')
    web_graph.print_metrics()




