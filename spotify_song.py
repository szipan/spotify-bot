from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute


class SpotifySongModel(Model):

    class Meta:
        table_name = "spotify-song"
        region = "us-east-1"

    id = UnicodeAttribute(null=False, hash_key=True)
    playCount = NumberAttribute(default_for_new=0)
