from marshmallow import Schema, fields

class ContentItemSchema(Schema):
    id = fields.Int(dump_only=True)
    vision_board_id = fields.Int(required=True)
    content_url = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=False)
    created_at = fields.DateTime(dump_only=True)
    main_image_url = fields.Str(required=False)
    content_type = fields.Str(required=True)

content_item_schema = ContentItemSchema()
content_items_schema = ContentItemSchema(many=True)
