from django.contrib.admin import AdminSite


class TTAdminSite(AdminSite):
    index_title = '首页'
    site_title = 'TT管理后台'
    site_header = 'TT-CMDB系统'


tt_admin_site = TTAdminSite(name='tt_admin')
