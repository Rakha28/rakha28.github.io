import requests
from bs4 import BeautifulSoup
import pprint

def test_homepage_selectors():
    """
    Fetches the homepage and tests the CSS selectors from the
    JavaScript parser to see what data is being extracted.
    """
    homepage_url = 'https://hiperdex.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"▶️  Fetching homepage: {homepage_url}")
    
    try:
        response = requests.get(homepage_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # --- Selector Testing ---
        # Find all the main item containers
        # Original JS selector: "div.page-item-detail"
        items = soup.select("div.page-item-detail")
        
        if not items:
            print("❌ CRITICAL ERROR: The main selector 'div.page-item-detail' found 0 items.")
            print("   You need to visit the website and find the new correct container class.")
            return

        print(f"✅ Found {len(items)} items using 'div.page-item-detail'. Testing selectors on the first 5...\n")
        
        report = []
        # Limit to the first 5 items for a clean report
        for item in items[:5]:
            # --- Attempt to extract each piece of data ---

            # Title: $("a", $("h3.h5", obj)).last().text()
            title_element = item.select_one("h3.h5 a")
            title = title_element.text.strip() if title_element else "--- NOT FOUND ---"

            # Slug: $("a", $("h3.h5", obj)).attr("href")
            slug = title_element['href'] if title_element else "--- NOT FOUND ---"
            
            # Post ID: $("div", obj).attr("data-post-id")
            # This is tricky. Let's assume it's on a child div. A common parent is .item-thumb
            post_id_element = item.select_one(".item-thumb")
            post_id = post_id_element['data-post-id'] if post_id_element else "--- NOT FOUND ---"

            # Subtitle: $("span.font-meta.chapter", obj).first().text().trim()
            subtitle_element = item.select_one("span.font-meta.chapter")
            subtitle = subtitle_element.text.strip() if subtitle_element else "--- NOT FOUND ---"

            report.append({
                "title": title,
                "slug": slug,
                "post_id": post_id,
                "subtitle": subtitle,
            })
            
        # --- Print the final report ---
        print("--- 🕵️‍♂️ Selector Diagnostic Report ---")
        pprint.pprint(report)
        print("------------------------------------")

    except requests.exceptions.RequestException as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    # Before running, make sure you've installed the required libraries:
    # pip install requests beautifulsoup4
    test_homepage_selectors()