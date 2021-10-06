from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article, Lesson, NewUser, Tutorial, Chapter, Book
from .serializers import (ArticleSerializer, 
                          RegisterSerializer, 
                          LoginSerializer, 
                          TutorialSerializer, 
                          LessonSerializer, 
                          BookSerializer, 
                          ChapterSerializer)
from rest_framework import generics
from rest_framework import permissions
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import update_last_login
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import authentication
from itertools import chain
# Create your views here.

def index(request):
    return render(request, 'build/index.html')


# Register user and generate the token
@method_decorator(csrf_exempt, name='post')
class RegisterView(generics.CreateAPIView):
    queryset = NewUser.objects.all()
    permission_classes = []
    serializer_class = RegisterSerializer

class LoginAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        update_last_login(None, user)
        token, created = Token.objects.get_or_create(user=user)
        print(user)
        return Response({"status": status.HTTP_200_OK, "token": token.key, "message": "User Logged In"})

class Search(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        query = request.GET.get('query')
        queryset1 = Article.objects.all()
        article_final_data = []
        
               
        if request.user.is_authenticated == False and query is not None:
            print(request.user)
            article_data1 = queryset1.filter(title__icontains = query)
            article_data2 = queryset1.filter(description__icontains = query).exclude(title__icontains = query)
            article_final_data = chain(article_data1, article_data2)
            print(article_final_data)
        
        serializer_data = ArticleSerializer(article_final_data, many = True)

        return Response({"Article": serializer_data.data})

class ArticleView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request, format = None):
        
        queryset1 = Article.objects.all()
        queryset2 = Lesson.objects.all()
        queryset3 = Tutorial.objects.all()
        queryset4 = Chapter.objects.all()
        queryset5 = Book.objects.all()
        
        
        print(request.user)
        if request.user.is_authenticated == False:
            print(request.user.is_authenticated)
            article_data = queryset1.exclude(is_public = False)
            lesson_data = queryset2.exclude(is_public = False)
            tutorial_data = queryset3.exclude(is_public = False)
            chapter_data = queryset4.exclude(is_public = False)
            book_data = queryset5.exclude(is_public = False)


            serializer_article = ArticleSerializer(article_data, many = True)
            serializer_lesson = LessonSerializer(lesson_data, many = True)
            serializer_tutorial = TutorialSerializer(tutorial_data, many = True)
            serializer_chapter = ChapterSerializer(chapter_data, many = True)
            serializer_book = BookSerializer(book_data, many = True)


            return Response({"Article": serializer_article.data, 
                            "Lesson": serializer_lesson.data, 
                            "Tutorial": serializer_tutorial.data,
                            "Chapter": serializer_chapter.data,
                            "Book": serializer_book.data})

        else: 
            serializer_article = ArticleSerializer(queryset1, many = True)
            serializer_lesson = LessonSerializer(queryset2, many = True)
            serializer_tutorial = TutorialSerializer(queryset3, many = True)
            serializer_chapter = ChapterSerializer(queryset4, many = True)
            serializer_book = BookSerializer(queryset5, many = True)
            
            return Response({"Article": serializer_article.data, 
                            "Lesson": serializer_lesson.data,
                            "Tutorial": serializer_tutorial.data, 
                            "Chapter": serializer_chapter.data,
                            "Book": serializer_book.data})


        # serializer_article = ArticleSerializer(article_data, many = True)
        # serializer_lesson = LessonSerializer(lesson_data, many = True)
        # serializer_tutorial = TutorialSerializer(tutorial_data, many = True)
        # serializer_chapter = ChapterSerializer(chapter_data, many = True)
        # serializer_book = BookSerializer(book_data, many = True)

        # serializer_article = ArticleSerializer(queryset1, many = True)
        # serializer_lesson = LessonSerializer(queryset2, many = True)
        # serializer_tutorial = TutorialSerializer(queryset3, many = True)
        # serializer_chapter = ChapterSerializer(queryset4, many = True)
        # serializer_book = BookSerializer(queryset5, many = True)
        
        # return Response({"Article": serializer_article.data,  
        #                 "Lesson": serializer_lesson.data,
        #                 "Tutorial": serializer_tutorial.data,
        #                 "Chapter": serializer_chapter.data, 
        #                 "Book": serializer_book.data})
        
        #     article_serializer = self.serializer_class(article_data, many = True)
        #     return Response(article_serializer.data)
        
        # serializer_article = self.serializer_class()
        
        # article_data = self.queryset.exclude(is_public = False)
        # article_serializer = self.serializer_class(article_data, many = True)
        # return Response(article_serializer.data)

# class RegisterView(APIView):
#     permissions = []
#     def post(self, request):

#         serializer = RegisterSerializer(data = request.data)

#         if not serializer.is_valid():
#             return Response({'status': 403, 'error': serializer.error, 'message': "Some Error Occured"})
#         serializer.save()

#         user = NewUser.objects.get(email = serializer.data['email'])
#         token_obj, _ = Token.objects.get_or_create(user=user)

#         return Response({'status': 200, 'User': serializer.data, 'token': str(token_obj)})


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def login_user(request):
#     data = {}
#     reqBody = json.loads(request.body)
#     email1 = reqBody['Email_Address']
#     print(email1)
#     password = reqBody['password']
#     try:
#         Account = NewUser.objects.get(Email_Address=email1)
#     except BaseException as e:
#         raise ValidationError({"400": f'{str(e)}'})
#     token = Token.objects.get_or_create(user=Account)[0].key
#     print(token)
#     if not check_password(password, Account.password):
#         raise ValidationError({"message": "Incorrect Login credentials"})

#     if Account:
#         if Account.is_active:
#             print(request.user)
#             login(request, Account)
#             data["message"] = "user logged in"
#             data["email_address"] = Account.email

#             Res = {"data": data, "token": token}

#             return Response(Res)

#         else:
#             raise ValidationError({"400": f'Account not active'})

#     else:
#         raise ValidationError({"400": f'Account doesnt exist'})

                

