from pathlib import Path

p = Path("/opt/cvat/cvat/urls.py")
s = p.read_text()

route = 'urlpatterns.append(path("api/test/", include("cvat.apps.test.urls")))'

if route not in s:
    s = s.replace(
        'if apps.is_installed("health_check"):',
        route + '\n\nif apps.is_installed("health_check"):'
    )
    p.write_text(s)
