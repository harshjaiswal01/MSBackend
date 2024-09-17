from marshmallow import Schema, fields

class VisionBoardSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    is_custom = fields.Bool(dump_only=True)
    description = fields.Str(required=False)
    created_by = fields.Int(dump_only=True)
    pic_url = fields.Str(required=False)

vision_board_schema = VisionBoardSchema()
vision_boards_schema = VisionBoardSchema(many=True)
