from database import db
from models.content_item import ContentItem
from models.schemas.content_item_schema import content_item_schema
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_metadata(content_url):
    response = requests.get(content_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('meta', property='og:title') or soup.find('title')
    description = soup.find('meta', property='og:description')
    main_image = soup.find('meta', property='og:image')
    created_at = datetime.now()

    return {
        "title": title['content'] if title else '',
        "description": description['content'] if description else '',
        "main_image_url": main_image['content'] if main_image else '',
        "created_at": created_at
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
