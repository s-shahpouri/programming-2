from crawler import Crawler


def main():
    crawler = Crawler()
    for x in range(5):
        print(str(next(crawler)))


if __name__ == "__main__":
    main()
