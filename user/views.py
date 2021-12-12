import json
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .services import create_random_string,updateRefferals
from .serializers import *
from .models import *
from rest_framework import generics


class Test(APIView):
    def get(self,request):
        updateRefferals()
        return Response(status=200)
class UserUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        #print(json.loads(request.data['userData']))

        # password = None
        # try:
        #     password = json.loads(request.data['password'])
        # except:
        #     pass

        if json.loads(request.data['userData'])['user_type'] == 'ur':
            user.is_company = True
            user.save(update_fields=['is_company'])
        else:
            user.is_company = False
            user.save(update_fields=['is_company'])

        serializer = UserSerializer(user, data=json.loads(request.data['userData']))
        # if password:
        #     user.set_password(password)
        #     user.save()
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:
            #print(serializer.errors)
            return Response(status=400)


class GetUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserRecoverPassword(APIView):
    def post(self,request):
        user = None
        try:
            user = User.objects.get(email=request.data['email'])
        except:
            user = None
        if user:
            password = create_random_string(digits=True, num=8)
            user.set_password(password)
            user.save()
            return Response({'result': True, 'email': user.email}, status=200)
        else:
            return Response({'result': False}, status=200)


class GetReferals(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):


        first_line_users = UserRefferalFirstLine.objects.get(user=request.user)

        second_line_users = UserRefferalSecondLine.objects.get(user=request.user)

        third_line_users = UserRefferalThirdLine.objects.get(user=request.user)
        serializer_1 = UserShortSerializer(first_line_users.users.all(), many=True)
        serializer_2 = UserShortSerializer(second_line_users.users.all(), many=True)
        serializer_3 = UserShortSerializer(third_line_users.users.all(), many=True)
        return Response({
            'first_line_users':serializer_1.data,
            'second_line_users':serializer_2.data,
            'third_line_users':serializer_3.data,
                         }, status=200)