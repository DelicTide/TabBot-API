import os
import json
import requests
import base64
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import time

# Load environment variables
load_dotenv()

class EbayBrowseAPI:
    def __init__(self):
        self.app_id = os.getenv('EBAY_APP_ID')
        self.cert_id = os.getenv('EBAY_CERT_ID')
        self.token = None
        
        # Get root directory (going up from scripts folder)
        self.root_dir = Path(__file__).parent.parent
        
        # Set paths relative to root
        self.image_log_file = self.root_dir / 'image_log.json'
        self.images_dir = self.root_dir / 'static' / 'images'
        
        self.downloaded_images = self.load_image_log()
        
        # Default search parameters
        self.default_keyword = "beverage can"
        self.default_category = "564"  # Other Collectible US Beer Cans
        
        # Create images directory if it doesn't exist
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
    def load_image_log(self):
        try:
            with open(self.image_log_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_image_log(self):
        with open(self.image_log_file, 'w') as f:
            json.dump(self.downloaded_images, f, indent=4)

    def get_oauth_token(self):
        url = "https://api.ebay.com/identity/v1/oauth2/token"
        
        credentials = base64.b64encode(
            f"{self.app_id}:{self.cert_id}".encode()).decode()
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {credentials}"
        }
        
        data = {
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope"
        }
        
        response = requests.post(url, headers=headers, data=data)
        self.token = response.json().get("access_token")
        return self.token

    def search_items(self, keyword=None, category_id=None):
        if not self.token:
            self.get_oauth_token()
            
        url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
        }
        
        params = {
            "limit": 100,  # Maximum items per request
            "fieldgroups": "EXTENDED"  # To get additional images
        }
        
        if keyword:
            params["q"] = keyword
        if category_id:
            params["category_ids"] = category_id
            
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def get_item_details(self, item_id):
        """Get detailed item information including all images"""
        if not self.token:
            self.get_oauth_token()
            
        url = f"https://api.ebay.com/buy/browse/v1/item/{item_id}"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
        }
        
        response = requests.get(url, headers=headers)
        return response.json()

    def download_image(self, image_url, item_id, image_number=0):
        """Download an image and save it with appropriate naming"""
        image_key = f"{item_id}_{image_number}"
        
        if image_key in self.downloaded_images:
            print(f"Image {image_number} for item {item_id} already downloaded.")
            return False
            
        safe_filename = item_id.replace('|', '_').replace('/', '_')
        # Use Path for reliable path joining
        filename = self.images_dir / f"{safe_filename}_{image_number}.jpg"
                
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            self.downloaded_images[image_key] = {
                "download_date": datetime.now().isoformat(),
                "image_url": image_url
            }
            self.save_image_log()
            return True
        return False

def main():
    api = EbayBrowseAPI()
    
    print("Welcome to the Royal eBay Image Collector, Your Majesty!")
    print("\nWould you like to search by:")
    print("1. Keyword")
    print("2. Category")
    print("3. Both")
    
    search_type = input("\nEnter choice (1-3): ")
    
    keyword = None
    category_id = None
    
    if search_type in ['1', '3']:
        use_default = input("Use default keyword 'Us can'? (Y/n): ").lower() != 'n'
        keyword = api.default_keyword if use_default else input("Enter keyword: ")
        
    if search_type in ['2', '3']:
        use_default = input("Use default category 'Other Collectible US Beer Cans'? (Y/n): ").lower() != 'n'
        category_id = api.default_category if use_default else input("Enter category ID: ")

    print("\nSearching with:")
    if keyword:
        print(f"Keyword: {keyword}")
    if category_id:
        print(f"Category ID: {category_id}")
        
    results = api.search_items(keyword, category_id)
    
    if 'itemSummaries' not in results:
        print("No items found or API error occurred.")
        return
        
    items = results['itemSummaries']
    print(f"\nFound {len(items)} items")
    
    downloaded_count = 0
    for item in items:
        print(f"\nProcessing item: {item['title'][:50]}...")
        
        # Get detailed item information
        item_details = api.get_item_details(item['itemId'])
        
        # Download primary image
        if 'image' in item_details and 'imageUrl' in item_details['image']:
            if api.download_image(item_details['image']['imageUrl'], item['itemId'], 0):
                downloaded_count += 1
                print("Primary image downloaded successfully")
        
        # Download additional images
        if 'additionalImages' in item_details:
            for idx, add_image in enumerate(item_details['additionalImages'], 1):
                if 'imageUrl' in add_image:
                    if api.download_image(add_image['imageUrl'], item['itemId'], idx):
                        downloaded_count += 1
                        print(f"Additional image {idx} downloaded successfully")
                        time.sleep(0.5)  # Small delay between image downloads
                
        time.sleep(1)  # Delay between items
                
    print(f"\nDownload complete! {downloaded_count} new images downloaded.")
    print(f"Total images in collection: {len(api.downloaded_images)}")

if __name__ == "__main__":
    main()