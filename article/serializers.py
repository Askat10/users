from rest_framework import serializers
from typing import List
from .models import Article, Tag
from reviews.serializers import CommentSerializer
from django.db.models import Avg

class ArticleListSerializer(serializers.ListSerializer):
    def to_representation(self, data: List[Article]):
        representation = super().to_representation(data)
        represent = [{'id': article['id'],
                    'title': article['title'],
                    'user': article['user'],
                    'tag': article['tag'],
                    'created_at': article['created_at']
                    } for article in representation]
        return represent
    pass


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'user', 'text', 'created_at', 'updated_at', 'tag', 'status', 'image']
        extra_kwargs = {
            'user': {'read_only': True}, 
            'created_at': {'read_only': True}, 
            'updated_at': {'read_only': True},
                        }
        
        list_serializer_class = ArticleListSerializer
        
    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        return super().create(validated_data)
    
    def to_representation(self, instance: Article):
        representation = super().to_representation(instance)
        representation['tag'] = [tag.title for tag in instance.tag.all()]
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        representation['rating'] = round(instance.rates.aggregate(Avg('rate'))['rate__avg'] or 0, 1)
        return representation

    


