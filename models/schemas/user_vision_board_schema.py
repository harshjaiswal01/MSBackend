from marshmallow import Schema, fields

class UserVisionBoardSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    vision_board_id = fields.Int(required=True)

user_vision_board_schema = UserVisionBoardSchema()
user_vision_boards_schema = UserVisionBoardSchema(many=True)
