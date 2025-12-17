from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import SolicitudAusencia 

class Command(BaseCommand):
    help = 'Crea usuarios iniciales (Admin y Empleados) si no existen'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@empresa.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('USUARIO ADMIN CREADO (User: admin / Pass: admin123)'))
        else:
            self.stdout.write('El usuario admin ya existe.')

        empleados = [
            {'user': 'empleado1', 'pass': 'test1234', 'code': 'EMP-001'},
            {'user': 'empleado2', 'pass': 'test1234', 'code': 'EMP-002'},
        ]

        for emp in empleados:
            if not User.objects.filter(username=emp['user']).exists():
                User.objects.create_user(emp['user'], f"{emp['user']}@empresa.com", emp['pass'])
                self.stdout.write(self.style.SUCCESS(f"EMPLEADO CREADO: {emp['user']}"))
            else:
                self.stdout.write(f"El empleado {emp['user']} ya existe.")