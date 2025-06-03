from api.text import ERROR_REC_ALREADY_IS_IN_CART
from grannsacker_foodgram.models import Cart
from api.serializers import BaseUserRecipeRelationSerializer


class CartSerializer(BaseUserRecipeRelationSerializer):
    model = Cart
    error_message = ERROR_REC_ALREADY_IS_IN_CART

    class Meta(BaseUserRecipeRelationSerializer.Meta):
        model = Cart
