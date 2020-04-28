from user.models import Menu


class MenuLookupDict:
    def __init__(self, user, menu_name):
        self.user, self.menu_name = user, menu_name

    def __repr__(self):
        return str(self.menu_name)

    def __getitem__(self, perm_name):
        print("这里1")
        return self.user.has_menu(self.menu_name)

    def __iter__(self):
        raise TypeError("MenuLookupDict is not iterable.")

    def __bool__(self):
        """ 返回 True 或 False """
        return self.user.has_menu(self.menu_name)


class MenuWrapper:
    def __init__(self, user):
        self.user = user

    def __getitem__(self, menu_label):
        if self.user.is_superuser:
            return True
        roles = self.user.roles.prefetch_related("menu").filter(status=True)
        menus = Menu.objects.none()
        for role in roles:
            menus |= role.menu.only("title").filter(status=True)
        for menu in menus:
            if menu_label == menu.name:
                return True
        return False

    def __iter__(self):
        # I am large, I contain multitudes.
        raise TypeError("Menu is not iterable.")

    def __contains__(self, menu_name):
        print(12, menu_name)
        """
        Lookup by "someapp" or "someapp.someperm" in perms.
        """
        print(menu_name)
        if '.' not in menu_name:
            # The name refers to module.
            return bool(self[menu_name])
        menu_name, perm_name = menu_name.split('.', 1)
        return self[menu_name]


def role_context(request):
    if not request.user.is_anonymous:
        roles = request.user.roles.all()
        menus = Menu.objects.none()
        for role in roles:
            menus |= role.menu.filter(status=True)
        context = {
            "menu": MenuWrapper(request.user),
            "menus": menus
        }
        return context
    return {}
