from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .serializers import user_likesSerializer
from .models import user_likes

from rest_framework import status
import json
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.models import User

import sys
sys.path.append('C:/Users/prashant jha/projects/RecomendationSystem')
from scraper import tfidf

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def likearticle(request):
  d1=json.dumps(request.data)
  payload = json.loads(d1)
  user = request.user
  like = user_likes.objects.create(
    user= user,
    like_index= payload["like_index"]
  )
  serializer =user_likesSerializer(like)
  return JsonResponse({'likes': serializer.data}, safe=False, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def viewarticle(request):
  user=request.user
  try:
    r_index=user_likes.objects.filter(user=user).last().like_index
    recomend_articles=tfidf.tfidf_based_model(r_index-2, 10)
    return HttpResponse(str(recomend_articles))
  except:
    recomend_articles=tfidf.tfidf_based_model(100-2, 10)
    return HttpResponse(str(recomend_articles))
    return HttpResponse(str(request.user))

@api_view(["DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated]) 
def deleteuser(request):
  d1=json.dumps(request.data)
  payload = json.loads(d1)
  user = payload["user"]
  try:
    #import pdb; pdb.set_trace()
    user1 = User.objects.get(username=user)
    #return HttpResponse(str(user1))
    s=user1.delete()
    return HttpResponse(str(s))
    return Response(status=status.HTTP_204_NO_CONTENT)
  except ObjectDoesNotExist as e:
    return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
  except Exception as e:
    return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  pass
