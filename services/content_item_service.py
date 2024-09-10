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

YOUTUBE_API_KEY = DevelopmentConfig.YOUTUBE_API_KEY

def fetch_metadata(content_url):
    # If the URL is from YouTube, use yt-dlp to extract metadata
    if "youtube.com" in content_url or "youtu.be" in content_url:
        return fetch_youtube_metadata(content_url)
    
    # Otherwise, use BeautifulSoup to scrape general HTML
    response = requests.get(content_url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Try to extract title from OpenGraph or title tag
    title_tag = soup.find('meta', property='og:title') or soup.find('title')
    title = title_tag['content'] if title_tag and title_tag.has_attr('content') else title_tag.text if title_tag else ''
    
    # Try to extract description from OpenGraph or meta description
    description_tag = soup.find('meta', property='og:description') or soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if description_tag else ''

    # Try to extract main image from OpenGraph
    main_image_tag = soup.find('meta', property='og:image')
    main_image_url = main_image_tag['content'] if main_image_tag else ''

    created_at = datetime.now()

    return {
        "title": title,
        "description": description,
        "main_image_url": main_image_url,
        "created_at": created_at
    }

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
    return {"message": "Content item deleted successfully"}

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