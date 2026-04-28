import feedparser
import httpx
from database import SessionLocal, init_db, engine
from src.ingestion.database import SessionLocal
from src.models.intelligence_report import IntelligenceReport

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
FEEDS = {
    "Gov Policy" : "https://www.gov.uk/search/policy-papers-and-consultations.atom",
    "MoD News" : "https://www.gov.uk/search/news-and-communications.atom?organisations%5B%5D=ministry-of-defence",
    "Defence Blog" : "https://defence-blog.com/topics/uk/feed/",
    # "Think Defence": "https://www.thinkdefence.co.uk/feed/",
    "Defence Viewpoints" : "https://www.defenceviewpoints.co.uk/rss"
}

def save_to_db(entries, source_name):
    session = SessionLocal()
    new_count = 0

    for entry in entries:
        link = entry.get('link')

        linkExists = session.query(IntelligenceReport).filter_by(link=link).first()
        if linkExists:
            print(f"Report with link {link} already exists. Skipping.")
            continue
        else:
            report = IntelligenceReport(
                title = entry.get('title'),
                link = link,
                source = source_name,
                content = entry.get('summary', '')
            )

            session.add(report)
            new_count += 1

    session.commit()
    session.close()
    if new_count > 0:
        print(f"Added {new_count} new reports from {source_name}.")

def run_scraper():
    init_db()

    with httpx.Client(headers=HEADERS, follow_redirects=True, verify=False) as client:
        # context = ssl._create_unverified_context()
        for name, url in FEEDS.items():
            print(f"\n--- Scraping {name} ---")
            try:
                response = client.get(url)
                response.raise_for_status()

                feed = feedparser.parse(response.text)

                if not feed.entries:
                    print(f"Feed {name} loaded but no entries found. Status code: {response.status_code}")
                    continue

                # Use .get() to avoid KeyErrors
                title = feed.feed.get('title', 'No Title Found')
                print(f"Checking feed: {title}")

                for entry in feed.entries[:3]:
                    print(f"\n[Title]: {entry.get('title', 'N/A')}")
                    print(f"[Link]: {entry.get('link', 'N/A')}")
                    date = entry.get('updated') or entry.get('published') or 'N/A'
                    print(f"[Date]: {date}")

                save_to_db(feed.entries, name)

            except Exception as e:
                print(f"An error occurred while scraping {name}: {e}")


if __name__ == "__main__":
    run_scraper()
