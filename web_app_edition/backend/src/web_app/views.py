from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from . import serializers as srs
from . import models as mds
from rest_framework_jwt.views import ObtainJSONWebToken


class LeaderboardViews():

    class NMM_Leaderboard(APIView):
        permission_classes = (AllowAny,)

        def post(self, request, format='json'):
            emmelo = mds.NMM_ELO_Rating.objects.order_by('-score')

            return Response({"success":False}, status=status.HTTP_200_OK)



class UserLogin(ObtainJSONWebToken):

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code in [400,401]:
            return Response({"success":False}, status=status.HTTP_200_OK)
        return response

class UserCreate(APIView):

    permission_classes = (AllowAny,)
          
    def get(self, request): #checks for validity of email and username
        data={}
        for key in request.GET.keys():
            data.update({key:request.GET[key]})

        if len(data)==1:
            serializer = srs.CheckUserSerializer(data=data)
            if serializer.is_valid():
                return Response({"success":False}, status=status.HTTP_200_OK)
        return Response({"success":True}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):#creates the user
        password1=request.data.pop('password1',None)

        errors={}
        if request.data["password"]!=password1:
            errors.update({'passwords':'Passwords do not match'}) 
        
        serializer = srs.UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
                    
            if not errors:
                user = serializer.save()

                if user:
                    response={'success':True}
                    response.update({"data":{"token":serializer.data['token']}})
                    response['data']['userId']=serializer.data['id']
                    response['data']['username']=serializer.data['username']

                    return Response(response, status=status.HTTP_201_CREATED)

        for key in serializer.errors.keys():
            errors.update({key:serializer.errors[key][0]})

        response={'success':False}
        response.update({"data":{"message":errors}})

        return Response(response, status=status.HTTP_200_OK)
