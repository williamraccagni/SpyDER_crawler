import time
import threading

class HostPriorityQueue:

    # This class manages the hosts and their urls according to an order of time dictated by politeness.
    # Each element of the queue is composed of the host, the list of associated urls, the timestamp,
    # and the token of the thread that is managing the host (null if not associated)

    def __init__(self):
        self.queue = [] #[ {origin 1, associated urls list 1 [], timestamp 1, Token thread} , {..., ....} , ....]
        self.get_lock = threading.Lock() # lock to manage the taking of hosts.
        self.release_lock = threading.Lock() # lock to manage the release of hosts.



    def is_not_empty(self) -> bool:
        for elem in self.queue:
            if elem['urls']:
                return True
        return False

    def number_of_valid_host(self) -> int:
        count = 0
        for elem in self.queue:
            if elem['urls']:
                count += 1
        return count



    def insert_url(self, origin : str, url : str, politeness): # adding new urls to the queue

        if self.queue:
            there_is = False
            for elem in self.queue:
                if elem['host'] == origin:
                    elem['urls'].append(url)
                    there_is = True
                    break
            if not there_is: self.queue.append({ 'host': origin, 'urls': [url], 'timestamp': time.time() + politeness, 'token': None})
        else:
            self.queue.append({ 'host': origin, 'urls': [url], 'timestamp': time.time() + politeness, 'token': None})



    def get_host_by_token(self, token):
        for elem in self.queue:
            if elem['token'] == token:
                return elem

    def get_urls(self, request_number, token): # retrieval of urls from an host taking

        cur_host = None

        with self.get_lock:

            for elem in self.queue:
                if elem['token'] == None and elem['urls']:
                    elem['token'] = token
                    cur_host = elem
                    break

        if(cur_host != None):

            while(cur_host['timestamp'] >= time.time()): continue

            if len(cur_host['urls']) > request_number:
                urls = cur_host['urls'][:request_number]
                del cur_host['urls'][:request_number]
                return urls
            else:
                urls = cur_host['urls']
                cur_host['urls'] = []
                return urls
        else:
            return None



    def release_token(self, politeness, token):

        with self.release_lock:
            for index in range(len(self.queue)):
                if self.queue[index]['token'] == token:

                    host_copy = self.queue[index]
                    host_copy['token'] = None
                    host_copy['timestamp'] = time.time() + politeness
                    del self.queue[index]
                    self.queue.append(host_copy)

                    break



    def get_status(self):
        for i, elem in enumerate(self.queue):
            print(str(i) + ': ' + elem['host'])
            for j, url in enumerate(elem['urls']):
                print('   ' + str(j) + ': ' + elem['urls'][j])
            print('timestamp: ' + str(elem['timestamp']))
            print('token: ' + str(elem['token']))



    def get_status_string(self):
        return self.queue








