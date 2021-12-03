from marshmallow import Schema, fields


class WordSchema(Schema):
    word = fields.Str(required=True)
    position = fields.Int(required=True)


word_schema = WordSchema()
