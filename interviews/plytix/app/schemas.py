"""Schemas for IO validation/serialization."""
from marshmallow import Schema, fields


class WordSchema(Schema):
    """Word schenma."""

    word = fields.Str(required=True)
    position = fields.Int(required=True)


word_schema = WordSchema()
