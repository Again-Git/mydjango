from django.shortcuts import render
from django.views import View
from .models import projects,interface
from .serializers import ProjectSerializers,InterfaceSerializers
from django.http import JsonResponse
import json

class myinterface2(View):
    def put(self,request,pk):
        inter = interface.objects.get(id=pk)
        res = {}
        try:
            inter_param = json.loads(request.body,encoding="utf-8")
        except Exception as e:
            res["msg"]="参数错误"
            res["code"]=1
            return JsonResponse(res,status=400)
        try:
            inter_s = InterfaceSerializers(data= inter_param)
        except Exception as e:
            res["msg"]="参数错误"
            res["code"]=1
            return JsonResponse(res,status=400)

        flag = inter_s.is_valid()
        if not flag:
            res.update(inter_s.errors)
            res["msg"] = "参数错误"
            res["code"] = 1
            return JsonResponse(res, status=400)

        inter_dict = inter_s.validated_data
        inter.name = inter_dict["name"] or inter.name
        inter.url = inter_dict["url"] or inter.url
        inter.save()
        inter_dict["msg"]="修改成功"
        inter_dict["code"]=0
        return JsonResponse(inter_dict,status=200)


    def get(self,request,pk):
        inter = interface.objects.get(id=pk)
        inter_serializer = InterfaceSerializers(instance=inter)
        inter_dict = inter_serializer.data
        inter_dict.update({"msg":"查询成功","code":0})
        return JsonResponse(inter_dict,status=200)

    def delete(self,request,pk):
        inter = interface.objects.get(id = pk)
        inter.delete()
        res ={"msg":"删除成功","code":0}
        return JsonResponse(res,status=200)


class myinterface(View):
    def get(self,request):
        inter = interface.objects.all()
        inter_serializer = InterfaceSerializers(instance=inter,many=True)
        inter_dict = inter_serializer.data

        res = {}
        res["msg"]="查询成功"
        res["code"]=0
        res["data"]=inter_dict
        return JsonResponse(res,status=200,safe=False)


    def post(self,request):
        res = {}
        try:
            inter_json = json.loads(request.body,encoding="utf-8")
        except Exception as e:
            res["msg"]="参数有误"
            res["code"]=1
            return JsonResponse(res,status=400)

        inter_serializer =InterfaceSerializers(data= inter_json)
        try:
            inter_serializer.is_valid()
        except Exception as e:
            res.update(inter_serializer.errors)
            res["msg"]="参数有误"
            res["code"]=1
            return JsonResponse(res,status=400)

        create_dict = inter_serializer.validated_data
        projectid = create_dict["projectid"]
        projects_obj =projects.objects.get(id=projectid)
        create_dict["projects"]= projects_obj
        create_dict.pop("projectid")
        obj = interface.objects.create(**create_dict)
        obj_dict = InterfaceSerializers(instance=obj)
        resdata = obj_dict.data
        resdata["msg"]="添加成功"
        resdata["code"]=0
        return JsonResponse(resdata,status=201)


class projectsView2(View):
    def get(self,request,pk):
        obj = projects.objects.get(id = pk)
        pro_dict = ProjectSerializers(instance=obj)
        dict1 = pro_dict.data
        dict1.update({"msg":"查询成功"})
        dict1.update({"code":0})
        return JsonResponse(dict1,status=200)

    def put(self, request,pk):
        res = {}
        try:
            #  反序列化要格式化的参数
            param = json.loads(request.body)
        except Exception as e:
            res["msg"] = "参数有误"
            res["code"] = 1
            return JsonResponse(res, status=400)
        try:
            #  将要修改的参数反序列化成字典类型
            pro_param = ProjectSerializers(data=param)
        except Exception as e :
            res["msg"]="传入的参数错误"
            res["code"]=1
            return JsonResponse(res,status=400)

        pro_param.is_valid()
        project = projects.objects.get(id= pk)
        project.name = pro_param.validated_data["name"] or project.name
        project.leader = pro_param.validated_data["leader"] or project.leader
        project.tester = pro_param.validated_data["tester"] or  project.tester
        project.desc = pro_param.validated_data["desc"] or project.desc
        project.save()
        res["msg"]="修改成功"
        res["code"]=0
        res.update(pro_param.validated_data)
        return JsonResponse(res,status=201)

    def delete(self,request,pk):
        obj = projects.objects.get(id=pk)
        obj.delete()
        res={"msg":"删除成功","code":0}
        return  JsonResponse(res,status=200)
# Create your views here.
class projectsView(View):

    def get(self,request):
        #  查询所有的项目信息
        pro_queryset  = projects.objects.all()
        #  将项目信息查询集对象序列化成嵌套字典的列表
        pro_list = ProjectSerializers(instance=pro_queryset,many=True)
        return JsonResponse(pro_list.data,safe=False,status=200)

    def post(self,request):
        # post 提交  格式：raw
        #  将前端传递的json格式的参数，转化为python中的json类型
        res ={}
        try:
            param = json.loads(request.body,encoding="utf-8")
        except Exception as e:
            res["msg"]="参数错误1"
            res["code"]=0
            return JsonResponse(res,status=400)
        obj  ={}
        try:
            # 反序列化，将json格式转化为dict字典格式
            obj = ProjectSerializers(data=param)
            # 进行校验，并抛出异常
            obj.is_valid(raise_exception=True)
        except Exception as e:
            #  obj.errors 是校验不通过的错误信息
            #  将错误信息添加到字典中,方便返回
            res.update(obj.errors)
            return JsonResponse(res, status=400)

        #  将校验通过的数据保存到数据库
        result = projects.objects.create(**obj.validated_data)
        #  将校验通过的数据添加到字典中方便返回
        res.update(obj.validated_data)
        res["msg"]="添加成功"
        res["code"]=1
        return JsonResponse(res,status=201)
