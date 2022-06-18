from django.http import HttpResponse
from django.shortcuts import render
from api.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Books
from .serializers import BookSerializer
from django.db import connection


# Create your views here.
def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    else:
        # signup
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            db_email = User.objects.get(email=email)
            error = {"err2":"Email already exists"}
            return render(request, 'home.html',error)
        except:
            user = User(email=email, password=password)
            user.save()
            return render(request, 'home.html')
        


def index(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    loggedIn = 'None'
    try:
        db_email = User.objects.get(email=email)
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM api_user WHERE email=%s''',[email])
        user = cursor.fetchall()
        if(user[0][1] == email and user[0][2] == password):
            request.session['loggedIn'] = email
            return render(request, 'index.html',{"session":loggedIn})
        else:
            error = {"err1":"Wrong Credentials"}
            return render(request, 'home.html', error)
    except:
        error = {"err1":"Wrong Credentials"}
        return render(request, 'home.html', error)
    


def student_view(request):
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM api_books''')
    books = cursor.fetchall()
    booksD = {
        "data": books,
        "session": 'loggedIn'
    }
    return render(request, 'studentView.html', booksD)

@api_view(['GET'])
def fetchAllRecords(request):
    books = Books.objects.all()
    jsonSerializer = BookSerializer(books, many=True)
    
    return Response(jsonSerializer.data)

@api_view(['POST'])
def createBook(request):
    jsonSerializer = BookSerializer(data=request.data)
    
    if jsonSerializer.is_valid():
        jsonSerializer.save()
    
    return Response("added successfully")


@api_view(['POST'])
def updateBook(request, id):
    book = Books.objects.get(id=id)
    jsonSerializer = BookSerializer(instance = book, data=request.data)
    
    if jsonSerializer.is_valid():
        jsonSerializer.save()
    
    return Response("updated successfully")


@api_view(['DELETE'])
def deleteBook(request, id):
    book = Books.objects.get(id=id)
    book.delete()
    
    return Response("deleted successfully")


def logout(request):
    try:
      del request.session['loggedIn']
    except:
      pass
    return render(request, 'home.html')