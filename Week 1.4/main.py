from crawler import Crawler

if __name__ == "__main__":
    crawler = Crawler()
    crawler.crawl_site()

    num_iterations = 5
    for _ in range(num_iterations):
        try:
            print(str(next(crawler)))
        except StopIteration:
            break
