# Generated by Django 2.2.11 on 2020-04-04 13:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RunRoleScript',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r_name', models.CharField(blank=True, max_length=128, unique=True, verbose_name='脚本名')),
                ('r_content', models.TextField(blank=True, null=True, verbose_name='脚本内容/.yml')),
                ('change_time', models.DateTimeField(auto_now_add=True, verbose_name='最后修改')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建用户')),
            ],
            options={
                'verbose_name': 'AnsibleRole执行脚本表',
                'db_table': 'run_role_script',
            },
        ),
        migrations.CreateModel(
            name='RunRoleLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=100, verbose_name='剧本名称')),
                ('role_result', models.TextField(verbose_name='执行结果')),
                ('role_datetime', models.DateTimeField(auto_now_add=True, verbose_name='执行时间')),
                ('role_user', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='操作用户')),
            ],
            options={
                'verbose_name': 'Role执行记录表',
                'verbose_name_plural': 'Role执行记录表',
                'db_table': 'ansible_role_log',
            },
        ),
        migrations.CreateModel(
            name='AnsibleRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=100, unique=True, verbose_name='role名称')),
                ('role_file', models.FileField(upload_to='roles/')),
                ('role_time', models.DateTimeField(auto_now_add=True, verbose_name='添加日期')),
                ('role_desc', models.TextField(blank=True, null=True, verbose_name='role描述')),
                ('role_user', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='添加人员')),
            ],
            options={
                'verbose_name': 'AnsibleRole表',
                'verbose_name_plural': 'AnsibleRole表',
                'db_table': 'ansible_role',
            },
        ),
        migrations.CreateModel(
            name='AnsiblePlaybookLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playbook_name', models.CharField(max_length=100, verbose_name='剧本名称')),
                ('playbook_result', models.TextField(verbose_name='执行结果')),
                ('playbook_datetime', models.DateTimeField(auto_now_add=True, verbose_name='执行时间')),
                ('playbook_user', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='操作用户')),
            ],
            options={
                'verbose_name': 'Playbook执行记录表',
                'verbose_name_plural': 'Playbook执行记录表',
                'db_table': 'ansible_playbook_log',
            },
        ),
        migrations.CreateModel(
            name='AnsiblePlaybook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playbook_name', models.CharField(max_length=100, unique=True, verbose_name='剧本名称')),
                ('playbook_file', models.FileField(blank=True, null=True, upload_to='playbooks/')),
                ('playbook_content', models.TextField(null=True, verbose_name='剧本内容')),
                ('playbook_time', models.DateTimeField(auto_now_add=True, verbose_name='添加日期')),
                ('playbook_desc', models.TextField(blank=True, null=True, verbose_name='剧本描述')),
                ('playbook_user', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='添加人员')),
            ],
            options={
                'verbose_name': 'Ansible剧本表',
                'verbose_name_plural': 'Ansible剧本表',
                'db_table': 'ansible_playbook',
            },
        ),
        migrations.CreateModel(
            name='AnsibleModuleLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ans_module', models.CharField(max_length=100, verbose_name='模块名称')),
                ('ans_args', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='模块参数')),
                ('ans_server', models.TextField(verbose_name='服务器')),
                ('ans_result', models.TextField(verbose_name='执行结果')),
                ('ans_datetime', models.DateTimeField(auto_now_add=True, verbose_name='执行时间')),
                ('ans_user', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='操作用户')),
            ],
            options={
                'verbose_name': 'Ansible模块执行记录表',
                'verbose_name_plural': 'Ansible模块执行记录表',
                'db_table': 'ans_module_log',
            },
        ),
    ]
