from marshmallow import Schema, fields

class VisionBoardSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    is_custom = fields.Bool(dump_only=True)
    created_by = fields.Int(dump_only=True)

vision_board_schema = VisionBoardSchema()
vision_boards_schema = VisionBoardSchema(many=True)
