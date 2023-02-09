from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.contrib.auth import authenticate


from .serializers import BookSerializer, BookCompletedSerializer
from bookprog.models import Book


# AUTHENTICATION
# --------------------------------------------------

# Initial POST request to sign up. User wont have valid token => exempt them from csrf check
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(username=data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            
            return JsonResponse({
                'token': str(token)
            }, status=201)
        except IntegrityError:
            return JsonResponse({
                'error': 'username already taken'
            }, status=400)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(
            request,
            username=data['username'],
            password=data['password']
        )

        if user is None:
            return JsonResponse(
                {'error': 'Unable to log in. Check username and password'},
                status=400
            )
        else:
            try:
                token = Token.objects.get(user=user)
            except: # user token is not in db
                token = Token.objects.create(user=user)
            return JsonResponse(
                {'token': str(token)},
                status=201
            )


# --------------------------------------------------

# open to the PUBLIC
# returns all books in existence
class BookList(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.all().order_by('-created')


# Only authenticated USER
# View all the books the user created
class UserBookList(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(user = self.request.user).order_by('-created')
        

# Create a new book
class UserBookCreate(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Book.objects.filter(user=user).order_by('-created')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserBookEdit(generics.RetrieveUpdateAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user).order_by('-created')

class UserBookCompleted(generics.UpdateAPIView):
    serializer_class = BookCompletedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user).order_by('-created')
    
    def perform_update(self, serializer):
        serializer.instance.complete = not(serializer.instance.complete)
        serializer.save()
    
