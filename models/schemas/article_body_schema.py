from marshmallow import Schema, fields

class ArticleBodySchema(Schema):
    id = fields.Int(dump_only=True)
    content_item_id = fields.Int(required=True)  # Points to the related ContentItem
    body = fields.Str(required=True)  # The article body content

article_body_schema = ArticleBodySchema()
article_bodies_schema = ArticleBodySchema(many=True)
