import threading
from datetime import datetime
import url_filter as uf
import time
import subprocess
import host_priority_queue as hpq
from page_from_url import request_page
import json
import topic_matching as tm
import html_filtering as hf



class Frontier:
    '''A simple Frontier for web-crawling'''

    # This ADT retrieves the pages from the sieve one at a time until it is full, redistributes them in the host queue
    # to be repartitioned among the threads. The execute procedure manages a number of threads for fetching and parsing
    # pages in the queue, where each thread manages a specific host. the execution ends when each thread has finished
    # executing, and the sieve and coda are emptied.

    def __init__(self, sieve, host_politeness : float, requests_number : int, web_graph):
        self.sieve = sieve
        self.host_politeness = host_politeness
        self.requests_number = requests_number
        self.host_queue = hpq.HostPriorityQueue()
        self.web_graph = web_graph

    def get_sieve(self):
        return self.sieve

    def load(self) -> bool: #loading urls from the sieve into the queue. Returns True if the sieve releases urls, False otherwise.

        url = self.sieve.get_url()

        if url != None:
            while(url != None):
                self.host_queue.insert_url(uf.get_url_origin(url), url, self.host_politeness)
                url = self.sieve.get_url()
            return True
        else:
            return False

    def execute(self, number_of_threads : int): # execution and management of threads for fetching and parsing of pages.

        threads = []

        while(self.load() or self.host_queue.is_not_empty() or threading.active_count()>1):
            while(threading.active_count() < (self.host_queue.number_of_valid_host() + 1) and threading.active_count() < (number_of_threads + 1) ):

                x = threading.Thread(target=self.work, args=(1,))
                x.start()
                threads.append(x)





    def work(self, a): #thread job

        thread_name = threading.current_thread().name

        fetched_urls = []

        print('\n' + thread_name + ' has just started. Active threads (with main included) are: ' + str(threading.active_count()))


        urls = self.host_queue.get_urls(self.requests_number, thread_name) # recovery of urls
        while(urls == None and self.host_queue.is_not_empty()): urls = self.host_queue.get_urls(self.requests_number, thread_name)

        host = self.host_queue.get_host_by_token(thread_name)['host']

        if(urls != None):

            for url in urls:
                fetched_urls.append(url)

                page = request_page(url) # recovery of page for every url

                ot = time.time()

                if page is not None: self.parser(url, page, thread_name, self.sieve, self.web_graph) # parsing of the page

                while((time.time()-ot)< 1.0): continue # wait 1 sec



            with open('thread_status/' + str(datetime.today()).replace(" ","_").replace(":",".") + thread_name + '_' +'_status.txt', 'w') as file:
                json.dump(obj=self.host_queue.get_status_string(), indent=4, sort_keys=True, fp=file)


            self.host_queue.release_token(self.host_politeness, thread_name) # release of token

            print(thread_name + ' finished executing:\nthis thread managed host '+ host+ ' and retrieved the following urls:')
            print(fetched_urls)




    def parser(self, cur_url : str, page, thread_name : str, sieve, web_graph):


        if tm.topic_related(hf.htmltags_filter(page.text)): #if the page contains a search key

            print(thread_name + ' matched ' + cur_url)

            text_file = open("pages/" + thread_name + "_tmp_page.txt", "w")
            text_file.write(page.text)
            text_file.close()

            # retrieval of urls via AWK
            COMMAND = "gawk -f href_urls_extractor.awk pages/" + thread_name + "_tmp_page.txt"
            filtered_urls = subprocess.check_output(COMMAND, shell=True).decode().split(sep='\n')
            filtered_urls = list(set(uf.fs_url_filter(uf.urls_completation(cur_url, filtered_urls))))



            # update sieve
            sieve.insert(thread_name, filtered_urls)
            # update webgraph
            web_graph.insert(cur_url, filtered_urls)




