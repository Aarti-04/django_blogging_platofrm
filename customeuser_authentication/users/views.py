from django.shortcuts import render
from rest_framework.views import APIView,Response,status
from .managers import CustomUserManager
from django.contrib.auth import authenticate,login
from .models import CustomUser,CustomToken
from .serializers import CustomTokenObtainPairSerializers,UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated

def get_auth_token(authenticatedUser):
    token_serializer = CustomTokenObtainPairSerializers()
    token = token_serializer.get_token(authenticatedUser)
    refresh = RefreshToken.for_user(authenticatedUser)
    token["refresh"]=str(refresh)
    # token["userid"]=int( authenticatedUser.id)
    return token
class UserApiView(APIView):
    def get(self,request):
        users=CustomUser.objects.all()
        users=UserSerializer(users,many=True)
        return Response({"response":users.data})
    def post(self,request):
        user=request.data
        if "email" not in user or "password" not in user:
            raise ValueError("Username and Password is required")
                # return Response({"errors":""},status=status.HTTP_400_BAD_REQUEST) 
        password=user["password"]
        user= CustomUser(**user)
        user.set_password(password)
        user.save()
        return Response({"response":"User Registered successfully"},status=status.HTTP_201_CREATED)     
class UserLoginApiView(APIView):
    def post(self,request):
        user =request.data
        authenticatedUser=authenticate(**user)
        if authenticatedUser is None:
            return Response({"Error":"Authentication failed"},status=status.HTTP_401_UNAUTHORIZED)
        # return Response({"response":"authenticated"})
        token=get_auth_token(authenticatedUser)
        # print(token["userid"])
        tokenToSave=CustomToken.objects.create(access_token= str(token.access_token),refresh_token=token["refresh"])
        tokenToSave.save()
        return Response({
            "access_token": str(token.access_token),
            "refresh_token": token["refresh"],
            "response":"login successfully"
        },status=status.HTTP_200_OK)
class UserLogoutView(APIView):
    # permission_classes=[IsAuthenticated]
    def post(self, request):
        print(request.headers) 
        token=request.headers["Authorization"].split()[1]
        print(token)
        # token_key = request.auth.key
        # print(token_key)
        # print(token_key)
        # token = CustomToken.c_token.check_token(token)
        # print(token)
        print(CustomToken.c_token.delete_token(token))
            # print("token deleted")
        # t=CustomToken.c_token.get_all()
        # print(t)

        # print(token)
        # token.delete()
        return Response({'detail': 'Successfully logged out.'})
