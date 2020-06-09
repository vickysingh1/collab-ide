import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

room_list=dict()
person_list=dict()
class Consumer(WebsocketConsumer):
    
    def connect(self):
        
        self.person_name=self.scope['url_route']['kwargs']['person_name']
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name='chat_%s' % self.room_name
        # if len(room_list)==0:
        #     room_list[self.room_name]="writedata"+"0"+".txt"
        #     file2=open('writedata0.txt','w+')
        #     file2.close()
        
           
        if(self.room_name not in room_list):
            a="writedata"+str(len(room_list))+".txt"
            room_list[self.room_name]=a
            person_list[self.room_name]=[self.person_name]
            file2=open(room_list[self.room_name],'w+')
            file2.close()
        person_list[self.room_name].append(self.person_name)
        file_name=room_list[self.room_name]
        print(file_name)
        file1=open(room_list[self.room_name],'r+')
        fh=file1.read()
        print(fh)
        print(room_list)
        print(person_list)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type":"chat_message",
                "message":self.person_name+" Joined Chat",
                "listofconnected":person_list[self.room_name],
                "output":"",
                "language":"",
                "message1":self.person_name+" Joined Chat",
                "precodes":fh
            }
        )
        self.accept()

    def disconnect(self, code):
        person_list[self.room_name].remove(self.person_name)
        print(person_list)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type":"chat_message",
                "message":self.person_name+" Left Chat",
                "listofconnected":person_list[self.room_name],
                "output":"",
                "language":"",
                "message1":self.person_name+" Left Chat",
                "precodes":""
            }
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    def receive(self, text_data=None, bytes_data=None):
        text_data_json=json.loads(text_data)
        message=text_data_json['message']
        file_subname=room_list[self.room_name]
        file3=open(file_subname,'w+')
        file3.write(message)
        file3.close()  
        output=text_data_json['output']
        language=text_data_json['language']
        message1=text_data_json['message1']
        precodes=text_data_json['precodes']
        

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'listofconnected':None,
                'output':output,
                'language':language,
                "message1":self.person_name+": "+message1,
                "precodes":""
                
            }
        )

    def chat_message(self,event):
        message=event['message']
        output=event['output']
        language=event['language']
        message1=event['message1']
        precodes=event['precodes']
        connected=event['listofconnected']
        if connected==None:
            self.send(text_data=json.dumps({
            'message':message,
            'output':output,
            'language':language,
            'message1':message1,
            'precodes':precodes,
            'connected':None
            }))
        else:
            connected=list(set(connected))
            self.send(text_data=json.dumps({
            'message':message,
            'output':output,
            'language':language,
            'message1':message1,
            'precodes':precodes,
            'connected':connected
            }))
    

       
