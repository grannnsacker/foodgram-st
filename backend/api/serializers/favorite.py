from api.serializers import BaseUserRecipeRelationSerializer
from api.text import ERROR_REC_ALREADY_IS_IN_FAV
from grannsacker_foodgram.models import Favorite

class FavoriteSerializer(BaseUserRecipeRelationSerializer):
    model = Favorite
    error_message = ERROR_REC_ALREADY_IS_IN_FAV

    class Meta(BaseUserRecipeRelationSerializer.Meta):
        model = Favorite
