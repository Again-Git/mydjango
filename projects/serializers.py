from rest_framework import serializers, validators


class ProjectSerializers(serializers.Serializer):
    id = serializers.IntegerField(label="id",help_text="项目id",read_only=True)
    name = serializers.CharField(max_length=50,min_length=1,label="项目名称",help_text="项目名称")
    leader = serializers.CharField(max_length=50,label="项目负责人",help_text="项目负责人")
    tester = serializers.CharField(max_length=30,label="测试人员",help_text="测试人员")
    desc = serializers.CharField(allow_blank=True)


class InterfaceSerializers(serializers.Serializer):
    id = serializers.IntegerField(label="接口id",help_text="接口id",read_only=True)
    name = serializers.CharField(max_length=50,label="接口名称",help_text="接口名称")
    url = serializers.CharField(max_length=50,required=True,label="接口地址",help_text="接口地址")
    projectid = serializers.IntegerField(required=False,label="所属项目",help_text="所属项目")
