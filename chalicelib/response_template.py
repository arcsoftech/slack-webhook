from jsonmodels import models, fields, errors, validators


class Fields(models.Base):

    title = fields.StringField(required=True)
    value = fields.StringField(nullable=True)
    short = fields.BoolField(required=True)


class Attachment(models.Base):

    fallback = fields.StringField(required=True)
    color = fields.StringField(nullable=True)
    pretext = fields.StringField(required=False)
    fallback = fields.StringField(required=True)
    color = fields.StringField(required=True)
    pretext = fields.StringField(required=False)
    author_name = fields.StringField(required=True)
    author_icon = fields.StringField(nullable=True)
    title = fields.StringField(required=True)
    title_link = fields.StringField(required=True)
    color = fields.StringField(required=True)
    text = fields.StringField(required=False)
    image_url = fields.StringField(required=False)
    thumb_url = fields.StringField(required=False)
    footer_icon = fields.StringField(required=False)
    footer = fields.StringField(required=False)
    ts = fields.FloatField(required=False)
    fields = fields.ListField([Fields], required=False)


class SlackResponse(models.Base):

    response_type = fields.StringField(required=True)
    text = fields.StringField(required=True)
    attachments = fields.ListField([Attachment], nullable=True, required=False)
