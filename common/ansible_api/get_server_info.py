from assets.models import Assets


def HostGenerate(hosts: list):
    result = []

    for host in hosts:
        if "." in host:
            a = Assets.objects.filter(ip=host).first()
        else:
            a = Assets.objects.filter(id=host).first()
        if a:
            result.append({
                "host": a.ip,
                "username": a.sshuser,
                "password": a.sshpwd,
                "port": a.sshport,
            })
    return result
