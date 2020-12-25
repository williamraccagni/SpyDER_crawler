import requests

def request_page(url : str):

    try:
        r = requests.get(url)
    except:
        return None

    if(r.status_code == 200):
        return r
    else:
        return None
