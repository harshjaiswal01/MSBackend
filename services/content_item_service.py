from database import db
from models.content_item import ContentItem
from models.article_body import ArticleBody
from models.schemas.content_item_schema import content_item_schema, content_items_schema
from models.schemas.article_body_schema import article_body_schema, article_bodies_schema
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import yt_dlp
from config import DevelopmentConfig
from slugify import slugify
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

YOUTUBE_API_KEY = DevelopmentConfig.YOUTUBE_API_KEY

def fetch_metadata(content_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # If the URL is from YouTube, use yt-dlp to extract metadata
    if "youtube.com" in content_url or "youtu.be" in content_url:
        return fetch_youtube_metadata(content_url)
    
    try:
        # Try fetching with requests first for simpler websites
        response = requests.get(content_url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        # Fall back to Selenium if requests fail (e.g., for JS-heavy websites)
        soup = fetch_dynamic_content(content_url)

    # Try to extract title from OpenGraph, Twitter, or title tag
    title_tag = (soup.find('meta', property='og:title') or 
                 soup.find('meta', property='twitter:title') or 
                 soup.find('title'))
    title = title_tag['content'] if title_tag and title_tag.has_attr('content') else title_tag.text if title_tag else ''
    
    # Try to extract description from OpenGraph, Twitter, or meta description
    description_tag = (soup.find('meta', property='og:description') or 
                       soup.find('meta', property='twitter:description') or 
                       soup.find('meta', attrs={'name': 'description'}))
    description = description_tag['content'] if description_tag else ''

    # Try to extract main image from OpenGraph or Twitter
    main_image_tag = (soup.find('meta', property='og:image') or 
                      soup.find('meta', property='twitter:image'))
    main_image_url = main_image_tag['content'] if main_image_tag else ''

    # Fallback: Try to get the first <p> tag if no meta description is available
    paragraph_tag = soup.find('p')
    fallback_description = paragraph_tag.text if paragraph_tag else ''
    description = description or fallback_description

    created_at = datetime.now()

    return {
        "title": title,
        "description": description,
        "main_image_url": main_image_url,
        "created_at": created_at
    }

def fetch_dynamic_content(url):
    # Setup Chrome options for headless browsing
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    # Path to your ChromeDriver (ensure it's installed)
    service = Service('/usr/local/bin/chromedriver')  # Update this with your chromedriver path
    driver = webdriver.Chrome(service=service, options=options)
    
    # Load the webpage
    driver.get(url)
    
    # Get the full HTML of the page (including JS-rendered content)
    page_source = driver.page_source
    
    # Close the browser session
    driver.quit()
    
    return BeautifulSoup(page_source, 'html.parser')

# def fetch_metadata(content_url):
#     # If the URL is from YouTube, use yt-dlp to extract metadata
#     if "youtube.com" in content_url or "youtu.be" in content_url:
#         return fetch_youtube_metadata(content_url)
    
#     # Otherwise, use BeautifulSoup to scrape general HTML
#     response = requests.get(content_url, verify=False)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Try to extract title from OpenGraph or title tag
#     title_tag = soup.find('meta', property='og:title') or soup.find('title')
#     title = title_tag['content'] if title_tag and title_tag.has_attr('content') else title_tag.text if title_tag else ''
    
#     # Try to extract description from OpenGraph or meta description
#     description_tag = soup.find('meta', property='og:description') or soup.find('meta', attrs={'name': 'description'})
#     description = description_tag['content'] if description_tag else ''

#     # Try to extract main image from OpenGraph
#     main_image_tag = soup.find('meta', property='og:image')
#     main_image_url = main_image_tag['content'] if main_image_tag else ''

#     created_at = datetime.now()

#     return {
#         "title": title,
#         "description": description,
#         "main_image_url": main_image_url,
#         "created_at": created_at
#     }

# def fetch_metadata(content_url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#     }

#     # If the URL is from YouTube, use yt-dlp to extract metadata
#     if "youtube.com" in content_url or "youtu.be" in content_url:
#         return fetch_youtube_metadata(content_url)
    
#     # Otherwise, use BeautifulSoup to scrape general HTML
#     response = requests.get(content_url, headers=headers, verify=False)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Try to extract title from OpenGraph, Twitter, or title tag
#     title_tag = (soup.find('meta', property='og:title') or 
#                  soup.find('meta', property='twitter:title') or 
#                  soup.find('title'))
#     title = title_tag['content'] if title_tag and title_tag.has_attr('content') else title_tag.text if title_tag else ''
    
#     # Try to extract description from OpenGraph, Twitter, or meta description
#     description_tag = (soup.find('meta', property='og:description') or 
#                        soup.find('meta', property='twitter:description') or 
#                        soup.find('meta', attrs={'name': 'description'}))
#     description = description_tag['content'] if description_tag else ''

#     # Try to extract main image from OpenGraph or Twitter
#     main_image_tag = (soup.find('meta', property='og:image') or 
#                       soup.find('meta', property='twitter:image'))
#     main_image_url = main_image_tag['content'] if main_image_tag else ''

#     # Fallback: Try to get the first <p> tag if no meta description is available
#     paragraph_tag = soup.find('p')
#     fallback_description = paragraph_tag.text if paragraph_tag else ''
#     description = description or fallback_description

#     created_at = datetime.now()

#     return {
#         "title": title,
#         "description": description,
#         "main_image_url": main_image_url,
#         "created_at": created_at
#     }

def fetch_youtube_metadata(youtube_url):
    video_id = youtube_url.split("v=")[-1]
    api_url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={YOUTUBE_API_KEY}&part=snippet"
    
    response = requests.get(api_url)
    data = response.json()

    if 'items' in data and len(data['items']) > 0:
        video_data = data['items'][0]['snippet']
        title = video_data.get('title', '')
        description = video_data.get('description', '')
        main_image_url = video_data.get('thumbnails', {}).get('high', {}).get('url', '')
    else:
        title, description, main_image_url = '', '', ''

    return {
        "title": title,
        "description": description,
        "main_image_url": main_image_url,
        "created_at": datetime.now()
    }


def add_content_item(vision_board_id, content_url, content_type):
    metadata = fetch_metadata(content_url)
    description = metadata['description']
    
    # Truncate description to 255 characters if necessary
    if len(description) > 255:
        description = description[:255]
    content_item = ContentItem(
        vision_board_id=vision_board_id,
        content_url=content_url,
        title=metadata['title'],
        description=metadata['description'],
        created_at=metadata['created_at'],
        main_image_url=metadata['main_image_url'],
        content_type=content_type
    )
    db.session.add(content_item)
    db.session.commit()
    return content_item_schema.dump(content_item), None

def update_content_item(content_item_id, data):
    content_item = db.session.query(ContentItem).filter_by(id=content_item_id).first()
    if not content_item:
        return None, {"error": "Content item not found"}

    content_item.title = data.get('title', content_item.title)
    content_item.description = data.get('description', content_item.description)
    content_item.main_image_url = data.get('main_image_url', content_item.main_image_url)

    db.session.commit()
    return content_item_schema.dump(content_item), None

def delete_content_item(content_item_id):
    content_item = db.session.query(ContentItem).filter_by(id=content_item_id).first()
    if not content_item:
        return None, {"error": "Content item not found"}

    db.session.delete(content_item)
    db.session.commit()
    return {"message": "Content item deleted successfully"}, None

def get_content_items_for_vision_board(vision_board_id, page, per_page):
    query = db.session.query(ContentItem).filter_by(vision_board_id=vision_board_id)
    
    # Apply pagination using the limit and offset based on page and per_page
    paginated_query = query.limit(per_page).offset((page - 1) * per_page).all()

    return content_items_schema.dump(paginated_query), None


def generate_custom_article_url(title):
    slug = slugify(title)
    unique_id = random.randint(100, 999)
    return f"/articles/{slug}-{unique_id}"

def add_custom_article(vision_board_id, title, body, description=None, main_image_url=None):
    # Generate the custom URL for the article
    custom_url = generate_custom_article_url(title)

    # Create the ContentItem
    content_item = ContentItem(
        vision_board_id=vision_board_id,
        content_url=custom_url,
        title=title,
        description=description,
        created_at=datetime.now(),
        main_image_url=main_image_url,
        content_type="custom_article"
    )
    db.session.add(content_item)
    db.session.commit()

    # Create and link the ArticleBody
    article_body = ArticleBody(
        content_item_id=content_item.id,
        body=body
    )
    db.session.add(article_body)
    db.session.commit()

    return {
        "content_item": content_item_schema.dump(content_item),
        "article_body": article_body_schema.dump(article_body),
        "url": custom_url
    }, None