from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http import *
# pyrefly: ignore [missing-import]
from .models import Students
import json


def get_app_routes():
    try:
        from django.urls import get_resolver, URLPattern, URLResolver
        resolver = get_resolver()
        routes = []

        def walk(patterns, prefix=""):
            for p in patterns:
                if isinstance(p, URLPattern):
                    pattern_str = prefix + str(p.pattern)
                    route_path = "/" + pattern_str.lstrip("^").lstrip("/")
                    if not route_path.startswith("/admin"):
                        name = p.name or "—"
                        view_fn = p.callback
                        view_name = getattr(view_fn, "__name__", str(view_fn))
                        methods = ["GET"]
                        if view_name == "home":
                            methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
                        elif view_name == "redirect_example":
                            methods = ["GET", "POST"]
                        is_api = view_name in ["jsonresponse", "student", "students", "querystudent"]

                        routes.append({
                            "path": route_path,
                            "name": name,
                            "view": view_name,
                            "has_params": "<" in route_path,
                            "methods": methods,
                            "is_api": is_api,
                        })
                elif isinstance(p, URLResolver):
                    pattern_str = prefix + str(p.pattern)
                    if not pattern_str.lstrip("/").startswith("admin"):
                        walk(p.url_patterns, prefix=pattern_str)

        walk(resolver.url_patterns)
        seen = set()
        unique = []
        for r in routes:
            key = (r["path"], r["name"])
            if key not in seen:
                seen.add(key)
                unique.append(r)
        return unique
    except Exception:
        return [
            {"path": "/", "name": "home", "view": "home", "has_params": False, "methods": ["GET", "POST", "PUT", "PATCH", "DELETE"], "is_api": False},
            {"path": "/put/<int:id>/", "name": "update", "view": "home", "has_params": True, "methods": ["PUT"], "is_api": False},
            {"path": "/about/", "name": "about", "view": "about", "has_params": False, "methods": ["GET"], "is_api": False},
            {"path": "/contact/", "name": "contact", "view": "contact", "has_params": False, "methods": ["GET"], "is_api": False},
            {"path": "/jsonrequest/", "name": "jsonapi", "view": "jsonresponse", "has_params": False, "methods": ["GET"], "is_api": True},
            {"path": "/students/", "name": "students", "view": "students", "has_params": False, "methods": ["GET"], "is_api": True},
            {"path": "/student/<int:id>/", "name": "student", "view": "student", "has_params": True, "methods": ["GET"], "is_api": True},
            {"path": "/redirect/", "name": "—", "view": "redirect_example", "has_params": False, "methods": ["GET", "POST"], "is_api": False},
            {"path": "/query/", "name": "—", "view": "querystudent", "has_params": False, "methods": ["GET"], "is_api": True},
        ]


# Create your views here.
def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        branch = request.POST.get('branch')
        if name and age and branch:
            Students.objects.create(name=name, age=int(age) if str(age).isdigit() else 0, branch=branch)
        return redirect('home')
    elif request.method == 'PUT':
        data=json.loads(request.body)
        id=data.get('id')
        student=Students.objects.get(id=id)
        student.name = data.get('name')
        student.age = data.get('age')
        student.branch = data.get('branch')
        student.save()
        return HttpResponse("Student Updated Sucessfully")
    elif request.method == 'PATCH':
        data=json.loads(request.body)
        id=data.get('id')
        student=Students.objects.get(id=id)
        student.name = data.get('name')
        student.save()
        return HttpResponse("Student Updated Sucessfully")
    elif request.method=='DELETE':
        data=json.loads(request.body)
        id=data.get('id')
        student=Students.objects.get(id=id)
        student.delete()
        return HttpResponse("Student Deleted Sucessfully")
    else:
        obj=Students.objects.all()
        routes = get_app_routes()
        return render(request,'home.html',{'obj':obj, 'routes': routes})
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def jsonresponse(request):
    data={
        "name":"json request",
        "message":"Hello Json"
    }
    return JsonResponse(data)
#lets send data in json 
def student(request,id):
    student = Students.objects.get(id=id)
    data = {
        'id': student.id,
        'name': student.name,
        'age': student.age,
        'branch': student.branch
    }
    return JsonResponse(data)
def students(request):
    students=Students.objects.all()
    data=list(students.values('id','name','age','branch'))
    return JsonResponse(data, safe=False)
        
def redirect_example(request):
    if request.method=="POST":
        name=request.POST.get("name")
        if name=="Honey":
            return redirect('student',id=1)
        elif name=="Sandeep":
            return redirect('student',id=2)
        else:
            return redirect('contact')
    else:
        return render(request,'redirect_ex.html')
def querystudent(request):
    name=request.GET.get('name','Vellu broooooo') #everything treated as str 
    data=list(Students.objects.filter(name=name).values())
    return JsonResponse(data,safe=False)