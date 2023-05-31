from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Comment, Favourite, Rating

class AbstractListSerializer(serializers.ListSerializer):
    pass



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'article', 'text', 'created_at']
        
        read_only_fields = ['user', 'created_at',]
    
    def save(self, **kwargs):
        user = self.context.get('request').user
        self.validated_data['user'] = user
        return super().save(**kwargs)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['article'] = instance.article.title
        representation['user'] = instance.user.username
        return representation
    list_serializer_class = AbstractListSerializer


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'
        read_only_fields = ['user']
        
    def validate(self, attrs):
        user = self.context.get('request').user
        article = attrs.get('article')
        rate = Favourite.objects.filter(user=user, article=article)
        if rate.exists():
            raise serializers.ValidationError('Rate already exists')
        return super().validate(attrs)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        representation['article'] = instance.article.title
        return representation
    
    def save(self, **kwargs):
        user = self.context.get('request').user
        self.validated_data['user'] = user
        return super().save(**kwargs)
    
    list_serializer_class = AbstractListSerializer


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['user']
    

    def save(self, **kwargs):
        user = self.context.get('request').user
        self.validated_data['user'] = user
        return super().save(**kwargs)

    def validate(self, attrs):
        user = self.context.get('request').user
        article = attrs.get('article')
        rate = Rating.objects.filter(user=user, article=article)
        if rate.exists():
            raise serializers.ValidationError('Rate already exists')
        return super().validate(attrs)

    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['user'] = instance.user.username
        representation['article'] = instance.article.title
        return representation

