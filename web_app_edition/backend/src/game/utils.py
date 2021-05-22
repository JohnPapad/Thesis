from web_app.serializers import GetIDUserSerializer
# used in seetings for authentication
def my_jwt_response_handler(token, user=None, request=None):
    info=GetIDUserSerializer(user, context={'request': request})
    return {
        "success" : True,
        "data":{
            'token' : token,
            "userId" :info.data['id'],
            "username" :info.data['username']
        }
    }