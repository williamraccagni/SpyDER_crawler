import re
import hyperlink
import validators

def get_url_origin(url):

    url_obj = hyperlink.URL.from_text(url)

    result = url_obj.scheme + '://' + url_obj.host
    if(url_obj.port != 80 and url_obj.port != 443): result = result + ':' + str(url_obj.port)


    return result

def fs_url_filter(urls : list):

    filtered_urls = []

    for url in urls:

        if url != '': # remove empty strings

            # normalization
            normalized_url = hyperlink.URL.from_text(url).normalize().to_text()

            extensions = ["gif", "js", "jpg", "png", "pdf", "mp3", "mp4", "ico", "svg", "css", "xml"]
            pattern = ".*("
            for elem in extensions:
                pattern += "\." + elem + "|\." + elem.upper() + "|"
            pattern = pattern[:-1] + ')'

            if(not re.search(pattern, normalized_url)):

                if(url[0:8] != 'https://' and url[0:7] != 'http://'):
                    normalized_url = 'https://' + normalized_url


                if(validators.url(normalized_url)==True and normalized_url not in filtered_urls): filtered_urls.append(normalized_url)


    return filtered_urls

def urls_completation(cur_url ,urls : list):

    new_urls = []

    for url in urls:

        if url != '':

            if(url[0:8] == 'https://' or url[0:7] == 'http://'):
                new_urls.append(url)
            else:
                if(url[0] == '/'):
                    new_urls.append(get_url_origin(cur_url)+url)
                else:
                    if (url[0:2] == './'):
                        new_urls.append(get_url_origin(cur_url) + url[1:len(url)])
                    else:
                        new_urls.append(get_url_origin(cur_url) + '/' + url)

    return new_urls


