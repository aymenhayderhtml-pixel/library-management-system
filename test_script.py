import sys
sys.path.insert(0, 'C:\\Users\\hp\\.openclaw\\workspace')
try:
    import scripts.fetch_gutendex_books
    print("Script imports successfully")
except Exception as e:
    print(f"Import error: {e}")