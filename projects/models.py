from django.db import models

# Create your models here.
class projects(models.Model):
    name = models.CharField(max_length=200,verbose_name="项目名称",help_text="项目名称")
    leader = models.CharField(max_length=50,verbose_name="项目负责人",help_text="项目负责人")
    tester = models.CharField(max_length=50,verbose_name="测试人员",help_text="测试人员")
    desc = models.CharField(max_length=500,verbose_name="备注",help_text="备注",null=True)

    class Meta:
        db_table = "tb_projects"
        verbose_name ="项目表"
        verbose_name_plural = verbose_name

class interface(models.Model):
    name = models.CharField(max_length=50,verbose_name="接口名称",help_text="接口名称")
    url = models.CharField(max_length=200,verbose_name="接口地址",help_text="接口地址")
    projects = models.ForeignKey(to= projects,on_delete=models.CASCADE,verbose_name="所属项目",help_text="所属项目")

    class Meta:
        db_table = "tb_interface"
        verbose_name ="接口表"
        verbose_name_plural = verbose_name