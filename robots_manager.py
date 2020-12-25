import url_filter as uf
import subprocess
import re
from page_from_url import request_page

def are_same_urls(urlA, url_target):

    try:
        pattern = url_target.replace('*', '.*')
        pattern = re.sub('/', r'\/', pattern)
        pattern = pattern + '.*'

        ob = re.search(pattern, urlA)

        if ob != None:
            return True
        else:
            return False
    except:
        return False


class Robots_Manager:
    '''A simple robot.txt files manager'''

    # This ADT stores the associated robots.txt rules for each host

    def __init__(self):
        self.urls = {}

    def insert(self, thread_name : str, new_urls : list):

        for url in new_urls:

            url_origin = uf.get_url_origin(url)

            if url_origin not in list(self.urls.keys()):

                robots = request_page(url_origin + '/robots.txt') # robots.txt file recovery

                if robots is not None:
                    text_file = open("robots/" + thread_name + "_tmp_robots.txt", "w")
                    text_file.write(robots.text)
                    text_file.close()

                    COMMAND = "gawk -f robots_parser.awk robots/" + thread_name + "_tmp_robots.txt" # rules retrieval with AWK script

                    disallowed_urls = subprocess.check_output(COMMAND, shell=True).decode().split(sep='\n')
                    if (disallowed_urls[-1] == ''): disallowed_urls = disallowed_urls[:-1]

                    self.urls[url_origin] = disallowed_urls # dictionary update with rules
                else:
                    self.urls[url_origin] = None



    def filter(self, thread_name, urls : list) -> list: # filter urls according to the rules

        allowed_urls = []

        for url in urls:
            url_origin = uf.get_url_origin(url)
            not_allowed = False

            if(url_origin not in list(self.urls.keys()) ): self.insert(thread_name, [url])

            if self.urls[url_origin] is not None:

                # Controllo ogni regola
                for na_url in self.urls[url_origin]:

                    not_allowed = are_same_urls(url, (url_origin + na_url))

                    if (na_url == '/'): not_allowed = True
                    if not_allowed == True: break


                if(not_allowed == False): allowed_urls.append(url)

            else:
                allowed_urls.append(url)

        return allowed_urls

    def get_status(self):
        for i, url in enumerate(list(self.urls.keys())):
            print(str(i)+': '+url)
            print(self.urls[url])




