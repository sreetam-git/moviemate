from rest_framework import serializers
from watchlist.models import WatchList, StreamPlatform, Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ['active', 'updated_at', 'watchlist']

class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    # len_title = serializers.SerializerMethodField()
    # full_storyline = serializers.SerializerMethodField()
    
    class Meta:
        model = WatchList
        # fields = "__all__"
        # fields = ['id', 'name', 'description']
        exclude = ['active']
        
    # def get_len_title(self, obj):
    #     return len(obj.title)
    
    # def get_full_storyline(self, obj):
    #     return obj.title + ' -> ' + obj.storyline
        
    def validate_name(self, title):
        if len(title) < 2:
            raise serializers.ValidationError("Title must be at least 2 characters")
        else:
            return title
        
    def validate_description(self, storyline):
        if len(storyline) < 10:
            raise serializers.ValidationError("Storyline must be at least 10 characters")
        else:
            return storyline
        
    def validate(self, data):
        if data['title'] == data['storyline']:
            raise serializers.ValidationError("Title and storyline cannot be the same")
        return data
    
class StreamPlatformSerializer(serializers.ModelSerializer):
    
    watchlist = WatchListSerializer(many=True, read_only=True) 
    
    class Meta:
        model = StreamPlatform
        fields = "__all__"

# def name_length(name):
#     if len(name) < 2:
#         raise serializers.ValidationError("Name must be at least 2 characters")

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, request):
#         movie = Movie.objects.create(**request)
#         return movie
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
    # 