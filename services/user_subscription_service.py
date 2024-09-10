from database import db
from models.user_subscription import UserSubscription
from models.schemas.user_subscription_schema import user_subscription_schema
from marshmallow import ValidationError

def create_or_update_subscription(user_id, subscription_data):
    try:
        subscription_data['user_id'] = user_id
        validated_data = user_subscription_schema.load(subscription_data)
    except ValidationError as err:
        return None, err.messages

    subscription = db.session.query(UserSubscription).filter_by(user_id=user_id).first()
    
    if subscription:
        subscription.newsletter_subscription = validated_data['newsletter_subscription']
        subscription.text_subscription = validated_data['text_subscription']
    else:
        subscription = UserSubscription(
            newsletter_subscription=validated_data['newsletter_subscription'],
            text_subscription=validated_data['text_subscription'],
            user_id=user_id
        )
        db.session.add(subscription)
    
    db.session.commit()
    return user_subscription_schema.dump(subscription), None

def get_subscription(user_id):
    subscription = db.session.query(UserSubscription).filter_by(user_id=user_id).first()
    
    if not subscription:
        return None, {"message": "Subscription not found"}
    
    return user_subscription_schema.dump(subscription), None