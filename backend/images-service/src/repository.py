import requests


class ImageRepository():
    def __init__(self, config):
        try:
            self.provider = BingImagesCrawlerProvider(**config['bing'])
        except KeyError:
            pass
            
        
    def search(self, term):
        return self.provider.search(term)

class BingImagesCrawlerProvider:
    URL = 'https://api.cognitive.microsoft.com/bingcustomsearch/v7.0/images/search'
    
    def __init__(self, api_key, custom_config_id, max_results=200, group_size=50):
        self.api_key = api_key
        self.custom_config_id = custom_config_id
        self.max_results = max_results
        self.group_size = min(group_size,max_results)
    
    def search(self, term):
        results = []
        offset = 0
        while len(results) < self.max_results:
            (fragment, totalEstimatedMatches) = self.search_fragment(term, offset)
            results += fragment
            if ((offset+1)*self.group_size) >= totalEstimatedMatches:
                break            
            offset += 1
        return results
    
    def search_fragment(self, term, offset=0):
        headers = {"Ocp-Apim-Subscription-Key" : self.api_key}
        params = {"q": term, "offset": offset, "count": self.group_size, "customConfig": self.custom_config_id}
        search = requests.get(self.URL, headers=headers, params=params)
        if search.status_code == 200:
            res = search.json()
            return ([v['contentUrl'] for v in res['value']], res['totalEstimatedMatches'])
        return ([], 0) # Raise Exception