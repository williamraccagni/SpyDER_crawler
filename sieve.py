import threading
import robots_manager as rm

class Sieve:
    '''A simple sieve for web-crawling'''

    # This ADT has the function of a sieve: it is basically a FIFO queue that releases each element only once.

    def __init__(self, seed : list, limit : int):
        self.limit = limit # max number of elements
        self.pointer = 0
        self.urls = {}
        self.manager = rm.Robots_Manager() # This object manages the robots.txt rules of each host

        self.insert_lock = threading.Lock() # This object manages thread logons to maintain data consistency.

        self.insert('main', seed)





    def count_keys(self): return len(list(self.urls.keys()))

    def get_limit(self): return self.limit

    def get_pointer(self): return self.pointer

    def is_full(self): return ( self.count_keys() >= self.limit )

    def is_discharged(self): return (self.pointer >= self.limit)

    def get_manager(self): return self.manager



    def insert(self, thread_name : str, new_urls : list): # insert urls
        with self.insert_lock:

            self.manager.insert(thread_name, new_urls) # insert new urls in the robots manager
            filtered_urls = self.manager.filter(thread_name, new_urls) # filter urls based on robots.txt rules

            for new_url in filtered_urls:
                if ( (self.is_full()==False) and (new_url not in list(self.urls.keys())) ):
                    self.urls[new_url] = None



    def get_url(self): # release urls
        if ( (self.is_discharged() == False) and (self.pointer < self.count_keys()) ):
            self.pointer += 1
            return list(self.urls.keys())[self.pointer-1]

        return None



    def print_keys(self):
        for i, url in enumerate(list(self.urls.keys())):
            print(str(i)+': '+url)

    def print_status(self):
        print('Limit: '+str(self.limit))
        print('Pointer: '+str(self.pointer))
        self.print_keys()


