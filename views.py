from django.http import HttpResponse
from django.core.management import call_command

def trigger_migrate(request):
    call_command('migrate')
    return HttpResponse("Migrações executadas com sucesso!")
