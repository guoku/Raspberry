# coding=utf-8
from django.http import HttpResponse
from pymogile import Client, MogileFSError

def image(request, image_key):
    
    datastore = Client( 
        domain = 'staging',
        trackers = ['10.0.1.23:7001']
    )
    
    _data = datastore.get_file_data('test_guoku4pk_avatar')

    return HttpResponse(_data, mimetype="image/jpeg")
        
        


