from rest_framework import serializers


class BaseUserRecipeRelationSerializer(serializers.ModelSerializer):
    model = None
    error_message = "Объект уже существует"

    class Meta:
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data['user']
        recipe = data['recipe']

        if self.model.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(self.error_message)

        return data
