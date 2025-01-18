import sqlite3
import os
from tabulate import tabulate  # Install using `pip install tabulate`

class DatabaseChecker:
    def __init__(self, db_path="visits.db"):
        self.db_path = db_path
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file '{db_path}' not found.")

    def connect(self):
        return sqlite3.connect(self.db_path)

    def fetch_and_display(self, query, headers, table_name):
        """Fetch and display data in tabular format."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                print(f"\n{table_name}:\n")
                print(tabulate(rows, headers=headers, tablefmt="grid"))
            else:
                print(f"\nNo data found in {table_name}.")

    def check_campaigns(self):
        """Fetch and display all campaigns from the database."""
        query = "SELECT * FROM campaigns;"
        headers = ["ID", "Name", "Short Code", "Description", "Start Date", "End Date"]
        self.fetch_and_display(query, headers, "Campaigns")

    def check_visits(self):
        """Fetch and display all visits from the database."""
        query = "SELECT * FROM visits;"
        headers = ["ID", "Session ID", "Campaign Code", "User Agent", "Referrer", "Timestamp"]
        self.fetch_and_display(query, headers, "Visits")

    def check_deep_links(self):
        """Fetch and display all deep links from the database."""
        query = "SELECT * FROM deep_links;"
        headers = ["ID", "Short Code", "Target URL", "Android Package", "iOS Bundle"]
        self.fetch_and_display(query, headers, "Deep Links")

if __name__ == "__main__":
    db_checker = DatabaseChecker("visits.db")

    print("Checking database content:")

    # Check campaigns
    db_checker.check_campaigns()

    # Check visits
    db_checker.check_visits()

    # Check deep links
    #db_checker.check_deep_links()
