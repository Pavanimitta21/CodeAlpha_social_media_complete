
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Post, Comment, Like

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def api_register(request):
    if request.method != 'POST':
        return JsonResponse({'error':'POST only'}, status=405)
    data = json.loads(request.body.decode('utf-8'))
    username = data.get('username','').strip()
    password = data.get('password','').strip()
    if not username or not password:
        return JsonResponse({'error':'username and password required'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error':'username taken'}, status=400)
    user = User.objects.create_user(username=username, password=password)
    return JsonResponse({'message':'user created'})

@csrf_exempt
def api_login(request):
    if request.method != 'POST':
        return JsonResponse({'error':'POST only'}, status=405)
    data = json.loads(request.body.decode('utf-8'))
    username = data.get('username','').strip()
    password = data.get('password','').strip()
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'error':'invalid credentials'}, status=400)
    login(request, user)
    return JsonResponse({'message':'login successful'})

def api_logout(request):
    logout(request)
    return JsonResponse({'message':'logged out'})

@csrf_exempt
def api_create_post(request):
    if request.method != 'POST':
        return JsonResponse({'error':'POST only'}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({'error':'authentication required'}, status=401)
    data = json.loads(request.body.decode('utf-8'))
    content = data.get('content','').strip()
    if not content:
        return JsonResponse({'error':'content required'}, status=400)
    p = Post.objects.create(user=request.user, content=content)
    return JsonResponse({'id':p.id, 'content':p.content, 'user':p.user.username, 'created_at':p.created_at.isoformat()})

def api_feed(request):
    posts = Post.objects.all().order_by('-created_at').select_related('user')
    out = []
    for p in posts:
        out.append({
            'id': p.id,
            'content': p.content,
            'user': p.user.username,
            'created_at': p.created_at.isoformat(),
            'likes': p.likes.count(),
            'commentsCount': p.comments.count()
        })
    return JsonResponse(out, safe=False)

@csrf_exempt
def api_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'GET':
        cs = post.comments.order_by('created_at').select_related('user')
        out = [{'id':c.id, 'content':c.content, 'user':c.user.username, 'created_at':c.created_at.isoformat()} for c in cs]
        return JsonResponse(out, safe=False)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error':'authentication required'}, status=401)
        data = json.loads(request.body.decode('utf-8'))
        content = data.get('content','').strip()
        if not content:
            return JsonResponse({'error':'content required'}, status=400)
        c = Comment.objects.create(post=post, user=request.user, content=content)
        return JsonResponse({'id':c.id, 'content':c.content, 'user':c.user.username, 'created_at':c.created_at.isoformat()})

@csrf_exempt
def api_like(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error':'authentication required'}, status=401)
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        like = Like.objects.filter(post=post, user=request.user).first()
        if like:
            like.delete()
            return JsonResponse({'liked': False, 'likes': post.likes.count()})
        else:
            Like.objects.create(post=post, user=request.user)
            return JsonResponse({'liked': True, 'likes': post.likes.count()})
    return JsonResponse({'error':'POST only'}, status=405)
