from marshmallow import Schema, fields

class UserSubscriptionSchema(Schema):
    id = fields.Int(dump_only=True)
    newsletter_subscription = fields.Bool(required=True)
    text_subscription = fields.Bool(required=True)
    user_id = fields.Int(required=True)

user_subscription_schema = UserSubscriptionSchema()
