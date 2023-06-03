import json
from channels.generic.websocket import AsyncWebsocketConsumer

from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync, sync_to_async
from .models import *
from channels.db import database_sync_to_async
# data = machine_data.objects.filter(machine_id="ABD2").values().last()
# print('data',data)
# data=machine_info.objects.all()
# print('data',data)

data = Department.objects.filter(name='Java developer').values().first()
print('data',data)




class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print('channel layer.........', self.channel_layer)   #get default channel layer from a project RedisChannelLayer(hosts=[{'address': 'redis://65.2.3.42:6379'}])
        print('channel name.........', self.channel_name)  #get default channel name  specific.348716a6ca6449589732ffef26e730e8!8c8a1f9863ed43e7aa7beb5a1c2c1eb7
        print('scope',self.scope['url_route']['kwargs']['groupname'])
        #add a channel(channel_name) to a new or existing group(programmer)
        self.group_name = self.scope['url_route']['kwargs']['groupname']

        async_to_sync(self.channel_layer.group_add)(
            # 'programmers',self.channel_name
            self.group_name, self.channel_name

        )
        # model_data = Department.objects.get(id=1)

        self.send({
            "type": "websocket.accept",
            # "text": str(model_data)  # Convert the data to a string or serialize it as needed
        })


    def websocket_receive(self,event):
        print('receive',event)
        print('receive text',event['text'])
        print('receive text type',type(event['text']))
        # self.data=json.loads(event['text'])
        # print('msg',self.data['message'])

        # model_data=Department.objects.get(id=1)
        async_to_sync(self.channel_layer.group_send)(self.group_name,{
            'type':'chat.message',
            'message':event['text']
        })
    def chat_message(self,event):
        print('Event......',event)
        print('Event message......',event['message'])
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })
    def websocket_disconnect(self,event):
        print('disconnect',event)
        print('channel layer.........', self.channel_layer)  # get default channel layer from a project RedisChannelLayer(hosts=[{'address': 'redis://65.2.3.42:6379'}])
        print('channel name.........',self.channel_name)  # get default channel name  specific.348716a6ca6449589732ffef26e730e8!8c8a1f9863ed43e7aa7beb5a1c2c1eb7
        self.group_name = self.scope['url_route']['kwargs']['groupname']

        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        raise StopConsumer()







class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print('channel layer.........', self.channel_layer)   #get default channel layer from a project RedisChannelLayer(hosts=[{'address': 'redis://65.2.3.42:6379'}])
        print('channel name.........', self.channel_name)  #get default channel name  specific.348716a6ca6449589732ffef26e730e8!8c8a1f9863ed43e7aa7beb5a1c2c1eb7


        #add a channel(channel_name) to a new or existing group(programmer)
        await self.channel_layer.group_add(
            'programmers',self.channel_name
        )

        await self.send({
            "type": "websocket.accept"
        })
        print('connect',event)


    async def websocket_receive(self,event):
        print('receive',event)
        print('receive text',event['text'])
        print('receive text type',type(event['text']))
        # data=machine_info.objects.all()
        # print('data',data)
        # self.model_data = await database_sync_to_async(self.get_id)

        print('Message received from client:', event)

        await self.channel_layer.group_send('programmers', {
            'type': 'chat.message',
            'message': event['text']
        })

    async def chat_message(self, event):
        print('Event......', event)
        print('Event message......', event['message'])
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })





    #     data = await self.get_data_from_database()
    #     print('data',data)
    #     data_str = json.dumps(data)
    #     print('data_str',type(data_str))
    #
    #     await self.send({
    #         'type': 'websocket.send',
    #         'text': data_str
    #     })
    #
    # @database_sync_to_async
    # def get_data_from_database(self):
    #     # data = 'kavya'
    #     # data = Department.objects.filter(name='Java developer').values()
    #     # print('get_data',data)
    #     return data


        # def get_id(self):
        #     return Department.objects.all()[0].id
    # async def chat_message(self,event):
    #     print('Event......',event)
    #     print('Event message......',event['message'])
    #     await self.send({
    #         'type':'websocket.send',
    #         'text':event['message']
    #     })
    async def websocket_disconnect(self,event):
        print('disconnect',event)
        print('channel layer.........', self.channel_layer)  # get default channel layer from a project RedisChannelLayer(hosts=[{'address': 'redis://65.2.3.42:6379'}])
        print('channel name.........',self.channel_name)  # get default channel name  specific.348716a6ca6449589732ffef26e730e8!8c8a1f9863ed43e7aa7beb5a1c2c1eb7
        await self.channel_layer.group_discard(
            'programmers',
            self.channel_name
        )
        raise StopConsumer()





