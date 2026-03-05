import urllib3
import ast

def get_all_attractions():
    http = urllib3.PoolManager()
    
    response = http.request('GET', "https://touringplans.com/magic-kingdom/attractions.json")
    
    mk_attractions = response.data.decode("utf-8")
    
    mk_attractions = ast.literal_eval(mk_attractions)
    
    return mk_attractions

mk_attractions = get_all_attractions()

attraction_names = [attraction['permalink'] for attraction in mk_attractions]


def get_attraction_info(attraction):
    http = urllib3.PoolManager()
    url = f"https://touringplans.com/magic-kingdom/attractions/{attraction}.json"
    response = http.request('GET', url)
    output = response.data.decode("utf-8").replace("null", "0").replace("true", "True").replace("false", "False")
    return ast.literal_eval(output)