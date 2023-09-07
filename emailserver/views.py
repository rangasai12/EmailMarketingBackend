from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Subscriber
from .serializers import SubscriberSerializer


# Create your views here.
def home(request):
    return HttpResponse("Welcome to the Email Server")


@api_view(['POST'])
def add_subscriber(request):
    if request.method == 'POST':
        serializer = SubscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def unsubscribe(request):
    if request.method == 'POST':
        email = request.data.get('email', None)
        if email:
            try:
                subscriber = Subscriber.objects.get(email=email)
                subscriber.is_active = False  # Mark subscriber as inactive
                subscriber.save()
                return Response({'message': 'Subscriber unsubscribed successfully.'})
            except Subscriber.DoesNotExist:
                return Response({'message': 'Subscriber not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
