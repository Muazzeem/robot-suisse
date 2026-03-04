
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.pagination import PageNumberPagination

from .serializers import OutputSerializer
from .models import Chat    

@api_view(['POST'])
def post_output(request):

    def group_name_from_uid(uid):
        safe_uid = str(uid).replace(':', '_').replace('.', '_').replace('/', '_')
        return f"chat_{safe_uid}"

    if isinstance(request.data, list):
        serializer = OutputSerializer(data=request.data, many=True)
    else:
        serializer = OutputSerializer(data=request.data)

    if serializer.is_valid():
        print(serializer.data)
        channel_layer = get_channel_layer()
        uid = request.data['uid']
        group_name = group_name_from_uid(uid)
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "broadcast.message",
                "data": serializer.data
            }
        )
        Chat.objects.create(**serializer.data)      
        return Response({
            "message": "Data received successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size' 
    max_page_size = 100


@api_view(['GET'])
def get_chat(request):
    uid = request.query_params.get('uid')
    
    if not uid:
        return Response({
            'error': 'uid parameter is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    chats = Chat.objects.filter(uid=uid).order_by('created_at')
    paginator = ChatPagination()
    paginated_chats = paginator.paginate_queryset(chats, request)
    
    chats_data = [
        {
            'question': chat.question,
            'output': chat.output,
            'created_at': chat.created_at.isoformat()
        }
        for chat in paginated_chats
    ]
    
    return paginator.get_paginated_response(chats_data)