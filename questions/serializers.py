from typing import SupportsRound
from rest_framework import serializers
from . import models
from users.serializers import UserSerializer,ProfileSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer

class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    number_of_likes = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()
    class Meta:
        model = models.Answer
        exclude = (
            'updated_at',
            'question',
        )        
    def get_number_of_likes(self,instance):
        return instance.a_likes.count()    

    def get_user_liked(self,instance):
        request = self.context['request'].user
        return models.ALike.objects.filter(
            answer=instance,
            liker = request
        ).exists()

class QuestionLikeSerializer(serializers.ModelSerializer):
    liker = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = models.QLike
        exclude = (
            'question',
            'id',
        )



class QuestionSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    number_of_answers = serializers.SerializerMethodField()
    answers = AnswerSerializer(many=True,read_only=True)
    q_likes = QuestionLikeSerializer(many=True,read_only=True)
    number_of_likes = serializers.SerializerMethodField()
    user_answered = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()
    
    
    
    class Meta:
        model = models.Question
        exclude = (
            'updated_at',
        )
        depth = 1


    # def validate(self,data):
    #     if not models.Category.objects.get(id=data['category']):
    #         return serializers.ValidationError('category can not created ')
    #     return data    
    
    def get_number_of_answers(self,instance):
        return instance.answers.count()
        ''' return models.Answer.objects.filter(question=instance).count() '''

    def get_number_of_likes(self,instance):
        return instance.q_likes.count() 
        '''return models.QLike.objects.filter(question=instance).count'''
    def get_user_answered(self,instance):
        request = self.context['request'].user
        return models.Answer.objects.filter(
            question=instance,
            author = request
        ).exists()

    def get_user_liked(self,instance):
        request = self.context['request'].user
        return models.QLike.objects.filter(
            question=instance,
            liker = request
        ).exists()

       
class QuestionPostSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    number_of_answers = serializers.SerializerMethodField()
    answers = AnswerSerializer(many=True,read_only=True)
    q_likes = QuestionLikeSerializer(many=True,read_only=True)
    number_of_likes = serializers.SerializerMethodField()
    user_answered = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()
    
    
    
    class Meta:
        model = models.Question
        exclude = (
            'updated_at',
        )
        extra_kwargs = {'category':{'write_only':True}}


    # def validate(self,data):
    #     if not models.Category.objects.get(id=data['category']):
    #         return serializers.ValidationError('category can not created ')
    #     return data    
    
    def get_number_of_answers(self,instance):
        return instance.answers.count()
        ''' return models.Answer.objects.filter(question=instance).count() '''

    def get_number_of_likes(self,instance):
        return instance.q_likes.count() 
        '''return models.QLike.objects.filter(question=instance).count'''
    def get_user_answered(self,instance):
        request = self.context['request'].user
        return models.Answer.objects.filter(
            question=instance,
            author = request
        ).exists()

    def get_user_liked(self,instance):
        request = self.context['request'].user
        return models.QLike.objects.filter(
            question=instance,
            liker = request
        ).exists()
        
        

        

class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    questions = QuestionSerializer(many=True,read_only=True)
    class Meta:
        model = models.Category
        fields = '__all__'

    def create(self,validate_data):
        if models.Category.objects.filter(name=validate_data['name']).exists():
            raise serializers.ValidationError("This category name already exists")    
        return models.Category.objects.create(**validate_data) 

                




class AnswerLikeSerializer(serializers.ModelSerializer):
    liker = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = models.ALike
        exclude = (
            'answer',
            'id',
        )        


