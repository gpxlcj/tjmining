from django.shortcuts import render, render_to_response

def page_not_found(request):
    response = render_to_response('error/p_404.html', locals())
    return response