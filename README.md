# mübaşir

![mübaşir](http://katipler.net/wp-content/uploads/2010/01/mubasir-150x150.jpg)

A slack extension for creating queues.

> muammer çay söyle iki tane ordan.

## Development

- Install Docker.
- Run `./tools/run_development.sh`
- Ask for `secrets.py`.
- Ask for `hipo_django_core` package.
- Inside the container, `python manage.py migrate` (If you need database modifications)
- Inside the container, `python manage.py createsuperuser` (If you need a super user)
- Inside the container, `python manage.py runserver 0:8000`
