from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta
from django.http.response import Http404

# Create your views here.

#def index(request):
#    return redirect('/agenda/')
def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, " Usuario ou senha inválido")

    return redirect('/')

@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario,
                                   data_evento__gt=data_atual)
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)


@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)


@login_required(login_url='/login/')
def submit_evento(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')

        # Analisando a data e hora para garantir que esteja no formato correto
        data_evento = parse_datetime(data_evento)

        if data_evento is None:
            return render(request, 'evento.html', {'error': 'Invalid date format'})

        if id_evento:
            Evento.objects.filter(id=id_evento).update(
                titulo=titulo,
                data_evento=data_evento,
                descricao=descricao,
                usuario=usuario
            )
        else:
            if titulo and data_evento and descricao:
                Evento.objects.create(
                    titulo=titulo,
                    data_evento=data_evento,
                    descricao=descricao,
                    usuario=usuario
                )
            else:
                return HttpResponse("Faltam informações no formulário.")

        return redirect('/agenda/')  # Redirecione para a página correta após o salvamento

    return redirect('/')


@login_required(login_url='/login/')
def delete_evento(request, id):
    evento = get_object_or_404(Evento, id=id, usuario=request.user)
    evento.delete()
    return redirect('/agenda/')

