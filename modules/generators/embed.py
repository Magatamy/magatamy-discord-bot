from disnake import Embed


class EmbedGenerator(Embed):
    """{
        "author_icon_url": "URL",
        "author_url": "URL",
        "author_name": "str",
        "title": "str",
        "description": "str",
        "thumbnail": "URL",
        "image": "URL",
        "footer_text": "str",
        "footer_icon_url": "URL",
        "color": "hex color",
        "fields": [{
            "name": "str",
            "value": "str",
            "inline": "bool"
        }]
    }"""
    def __init__(self, json_schema: dict, *args, **kwargs):
        super().__init__(title=json_schema.get('title', '').format(*args, **kwargs),
                         description=json_schema.get('description', '').format(*args, **kwargs),
                         color=int(json_schema.get('color', '0x000000').format(*args, **kwargs), 16))
        self.set_author(icon_url=json_schema.get('author_icon_url', '').format(*args, **kwargs),
                        url=json_schema.get('author_url', '').format(*args, **kwargs),
                        name=json_schema.get('author_name', '').format(*args, **kwargs))
        self.set_thumbnail(url=json_schema.get('thumbnail', '').format(*args, **kwargs))
        self.set_image(url=json_schema.get('image', '').format(*args, **kwargs))
        self.set_footer(text=json_schema.get('footer_text', '').format(*args, **kwargs),
                        icon_url=json_schema.get('footer_icon_url', '').format(*args, **kwargs))

        for field in json_schema.get('fields', []):
            self.add_field(name=field.get('name', '** **').format(*args, **kwargs),
                           value=field.get('value', '** **').format(*args, **kwargs),
                           inline=field.get('inline', True))
