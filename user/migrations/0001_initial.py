# Generated by Django 2.1.7 on 2020-03-28 00:51

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('create_time', models.DateTimeField(auto_created=True, null=True, verbose_name='创建时间')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='用户ID')),
                ('password', models.CharField(blank=True, max_length=128, null=True, verbose_name='password')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('realname', models.CharField(max_length=32, verbose_name='真实姓名')),
                ('is_active', models.BooleanField(default=True, null=True, verbose_name='是否激活')),
                ('avatar', models.CharField(default='/static/users-img/admin.png', max_length=255, null=True, verbose_name='用户头像')),
                ('info', models.CharField(max_length=100, null=True, verbose_name='介绍')),
                ('token', models.CharField(blank=True, max_length=128, verbose_name='钉钉唯一标识符')),
                ('userid', models.CharField(blank=True, max_length=128, null=True, verbose_name='钉钉用户id')),
                ('change_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='更新时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=64)),
                ('status', models.BooleanField(blank=True, default=True)),
                ('icon', models.CharField(blank=True, max_length=64, null=True, verbose_name='图标')),
                ('name', models.CharField(blank=True, max_length=32, null=True, verbose_name='别名')),
                ('path', models.CharField(blank=True, max_length=128, null=True, verbose_name='路径')),
                ('url', models.CharField(blank=True, max_length=128, null=True, verbose_name='url')),
            ],
            options={
                'verbose_name': '菜单',
                'verbose_name_plural': '菜单',
                'db_table': 'menu',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=64)),
                ('status', models.BooleanField(blank=True, default=True)),
                ('menu', models.ManyToManyField(blank=True, db_constraint=False, related_name='role', to='user.Menu')),
            ],
            options={
                'verbose_name': '角色',
                'verbose_name_plural': '角色',
                'db_table': 'role',
            },
        ),
        migrations.CreateModel(
            name='UrlPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=64)),
                ('url', models.CharField(blank=True, help_text='url与method 联合唯一', max_length=128, null=True)),
                ('status', models.BooleanField(blank=True, default=True)),
                ('is_absolute', models.BooleanField(blank=True, default=True, verbose_name='绝对匹配(默认:模糊匹配)')),
                ('method', models.CharField(blank=True, choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE'), ('ALL', 'ALL')], default='GET', max_length=32)),
            ],
            options={
                'verbose_name': 'url权限表',
                'verbose_name_plural': 'url权限表',
                'db_table': 'permission',
            },
        ),
        migrations.AlterUniqueTogether(
            name='urlpermission',
            unique_together={('url', 'method')},
        ),
        migrations.AddField(
            model_name='role',
            name='permission',
            field=models.ManyToManyField(blank=True, db_constraint=False, related_name='role', to='user.UrlPermission'),
        ),
        migrations.AddField(
            model_name='role',
            name='users',
            field=models.ManyToManyField(blank=True, db_constraint=False, related_name='roles', to=settings.AUTH_USER_MODEL),
        ),
    ]
