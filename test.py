import requests
import re
from bs4 import BeautifulSoup

def run_comparison_test():
    """
    Compares the result of an AJAX request with and without a security nonce
    to demonstrate why the original request fails.
    """
    session = requests.Session()
    ajax_url = 'https://hiperdex.com/wp-admin/admin-ajax.php'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # --- Test 1: The "Original" Request (without nonce) ---
    print("--- 🧪 Test 1: Running ORIGINAL Request (No Nonce) ---")
    
    original_payload = {
        'action': 'madara_load_more',
        'page': '2',
        'template': 'madara-core/content/content-archive',
        'vars[paged]': '1',
        'vars[posts_per_page]': '10',
        'vars[orderby]': 'meta_value_num',
        'vars[post_type]': 'wp-manga',
        'vars[meta_key]': '_wp_manga_views'
    }

    try:
        response_original = session.post(ajax_url, data=original_payload, headers=headers, timeout=15)
        response_original.raise_for_status()
        
        # Check the response content
        if not response_original.text or response_original.text == '0':
            print("▶️  Result: Request Succeeded, but the server returned an EMPTY response.")
            print("✅ Conclusion: As expected, the request without a nonce was rejected by the server.\n")
        else:
            print("▶️  Result: Server returned data unexpectedly.")
            print("⚠️  Conclusion: The server may have changed its security, but this is unlikely.\n")

    except requests.exceptions.RequestException as e:
        print(f"▶️  Result: Request failed with an error: {e}\n")

    # --- Test 2: The "Updated" Request (with nonce) ---
    print("--- 🧪 Test 2: Running UPDATED Request (With Nonce) ---")
    
    try:
        # Step A: Get a fresh nonce first
        print("   -> Fetching homepage to get nonce...")
        homepage_url = 'https://hiperdex.com/'
        response_home = session.get(homepage_url, headers=headers, timeout=15)
        response_home.raise_for_status()
        script_tag = BeautifulSoup(response_home.text, 'html.parser').find('script', id='wp-manga-login-ajax-js-extra')
        nonce = re.search(r'"nonce"\s*:\s*"([a-zA-Z0-9]+)"', script_tag.string).group(1)
        print(f"   -> Found nonce: {nonce}")

        # Step B: Build the payload WITH the nonce
        updated_payload = original_payload.copy() # Start with the same payload
        updated_payload['nonce'] = nonce          # Add the crucial nonce

        # Step C: Send the request
        print("   -> Sending AJAX request with nonce...")
        response_updated = session.post(ajax_url, data=updated_payload, headers=headers, timeout=15)
        response_updated.raise_for_status()

        if response_updated.text and response_updated.text != '0':
            print("▶️  Result: Server returned HTML content.")
            print("✅ Conclusion: The request with a valid nonce was accepted by the server.")
            # print("\n--- Response Snippet ---")
            # print(response_updated.text[:300]) # Optional: uncomment to see the HTML
        else:
            print("▶️  Result: Request Succeeded, but the server returned an EMPTY response.")
            print("⚠️  Conclusion: The request failed even with a nonce. The nonce key or another param might be wrong.")

    except requests.exceptions.RequestException as e:
        print(f"▶️  Result: Request failed with an error: {e}")
    except AttributeError:
        print("▶️  Result: Could not find the nonce on the homepage. The website structure may have changed.")


if __name__ == "__main__":
    run_comparison_test()