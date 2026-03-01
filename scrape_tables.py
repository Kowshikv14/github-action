from playwright.sync_api import sync_playwright
import re

def scrape_all_numbers():
    seeds = range(73, 83)  # 73 to 82
    base_url = "https://sanand0.github.io/tdsdata/js_table/?seed={}"
    
    total_sum = 0
    successful_scrapes = 0
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for seed in seeds:
            url = base_url.format(seed)
            print(f"\nScraping {url}")
            
            try:
                response = page.goto(url, wait_until="networkidle", timeout=30000)
                
                if response.status != 200:
                    print(f"  ❌ Page returned status {response.status}")
                    continue
                
                # Wait for tables to load (JavaScript rendered)
                page.wait_for_selector("table", timeout=10000)
                
                # Get all table elements
                tables = page.query_selector_all("table")
                print(f"  ✅ Found {len(tables)} tables")
                
                if tables:
                    successful_scrapes += 1
                
                for i, table in enumerate(tables, 1):
                    # Get all text content from the table
                    text = table.inner_text()
                    
                    # Extract all numbers (including decimals and negatives)
                    numbers = re.findall(r'-?\d+\.?\d*', text)
                    
                    table_sum = 0
                    for num_str in numbers:
                        if num_str:  # Skip empty strings
                            try:
                                num = float(num_str)
                                total_sum += num
                                table_sum += num
                            except ValueError:
                                pass
                    
                    if table_sum != 0:
                        print(f"  Table {i} sum: {table_sum}")
                            
            except Exception as e:
                print(f"  ❌ Error: {str(e)[:100]}")
        
        browser.close()
    
    print(f"\n{'='*60}")
    print(f"Successfully scraped: {successful_scrapes}/{len(list(seeds))} pages")
    print(f"{'='*60}")
    return total_sum

if __name__ == "__main__":
    total = scrape_all_numbers()
    print(f"\n{'='*60}")
    print(f"TOTAL SUM OF ALL NUMBERS: {total}")
    print(f"{'='*60}")
