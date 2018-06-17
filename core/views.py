import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .helper import Crawling


# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

@csrf_exempt
def crawler(request):
    post_data = json.loads(request.body).get('data')
    craw_url = post_data.get('url') or ''
    craw_depth = int(post_data.get('depth') or 1)
    try:
        instance = Crawling(url = craw_url, depth= craw_depth)
        instance.bifrost()
        value = instance.scrapped_data
            
        return HttpResponse(json.dumps(value),
                        status=200, content_type="application/json")
    except Exception as e:
        print (e)
        return HttpResponse(json.dumps({'msg': 'please check the url which is been passed, make sure url format should be http://fullcontact.com'}),
                        status=202, content_type="application/json")
