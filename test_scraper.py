from scraper import selenium_scrape
try:
    result = selenium_scrape('python')
    print("Result:", result)
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()