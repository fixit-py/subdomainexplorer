import argparse
import requests
import re
import urllib.parse as urlparse

class Crawl:
    def __init__(self, target_url):
        self.target_url = target_url
        self.target_links = []

    def extract_links_from(self, url):
        try:
            response = requests.get(url)
            return re.findall(r'href=["\'](https?://[^"\'>]+)', response.content.decode(errors="ignore"))
        except Exception as e:
            print("Error:", str(e))
            return []

    def crawl(self, url):
        href_links = self.extract_links_from(url)

        for link in href_links:
            link = urlparse.urljoin(url, link)

            if "#" in link:
                link = link.split("#")[0]

            if self.target_url in link and link not in self.target_links:
                self.target_links.append(link)
                print(link)
                self.crawl(link)

    def run(self):
        self.crawl(self.target_url)

class Spider:
    def __init__(self, target_url):
        self.target_url = target_url
        self.path = []

    def request(self, url):
        try:
            return requests.get("http://" + url)
        except requests.exceptions.ConnectionError:
            pass

    def dirdiscover(self, url):
        with open("common_dir.txt", "r") as wordlist_file:
            for line in wordlist_file:
                word = line.strip()
                test_url = url + "/" + word
                response = self.request(test_url)
                if response:
                    print("[+] Discovered URL ----> " + test_url)
                    self.path.append(word)

    def start(self):
        self.dirdiscover(self.target_url)

        for paths in self.path:
            self.dirdiscover(self.target_url + "/" + paths)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl or Spider a website")
    parser.add_argument('-c', '--crawl', dest='crawl_url', help='Crawl a website')
    parser.add_argument('-s', '--spider', dest='spider_url', help='Spider a website')

    args = parser.parse_args()

    if args.crawl_url:
        crawl_instance = Crawl(args.crawl_url)
        crawl_instance.run()
    elif args.spider_url:
        spider_instance = Spider(args.spider_url)
        spider_instance.start()
    else:
        parser.print_help()
