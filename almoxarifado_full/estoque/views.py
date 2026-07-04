from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash
)

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse

from django.contrib.auth.models import User

from .models import Item
from .forms import ItemForm, RegistroForm


# LOGIN

def home(request):

    erro = None

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('menu')

        else:

            erro = (
                "Usuário ou senha incorretos, "
                "tente novamente"
            )

    return render(
        request,
        'home.html',
        {
            'erro': erro
        }
    )


# REGISTRO

def registro(request):

    form = RegistroForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        return redirect('home')

    return render(
        request,
        'registro.html',
        {
            'form': form
        }
    )


# LOGOUT

def sair(request):

    logout(request)

    return redirect('home')


# MENU

@login_required
def menu(request):

    return render(
        request,
        'menu.html'
    )


# VISUALIZAR

@login_required
def visualizar(request):

    busca = request.GET.get('q')

    itens = Item.objects.all()

    if busca:

        itens = itens.filter(
            nome__icontains=busca
        )

    return render(
        request,
        'visualizar.html',
        {
            'itens': itens
        }
    )


# EDITAR

@login_required
def editar(request):

    itens = Item.objects.all()

    return render(
        request,
        'editar.html',
        {
            'itens': itens
        }
    )


# ADICIONAR

@login_required
def adicionar(request):

    form = ItemForm(
        request.POST or None
    )

    if form.is_valid():

        obj = form.save(commit=False)

        obj.usuario = request.user

        obj.save()

        return redirect('editar')

    return render(
        request,
        'form.html',
        {
            'form': form
        }
    )


# ATUALIZAR

@login_required
def atualizar(request, id):

    item = get_object_or_404(
        Item,
        id=id
    )

    form = ItemForm(
        request.POST or None,
        instance=item
    )

    if form.is_valid():

        form.save()

        return redirect('editar')

    return render(
        request,
        'form.html',
        {
            'form': form
        }
    )


# DELETAR ITEM

@login_required
def deletar(request, id):

    item = get_object_or_404(
        Item,
        id=id
    )

    item.delete()

    return redirect('editar')


# RELATÓRIOS

@login_required
def relatorios(request):

    itens = Item.objects.all()

    q = request.GET.get('q')
    min_qtd = request.GET.get('min_qtd')
    max_qtd = request.GET.get('max_qtd')
    min_valor = request.GET.get('min_valor')

    if q:

        itens = itens.filter(
            nome__icontains=q
        )

    if min_qtd:

        itens = itens.filter(
            quantidade__gte=min_qtd
        )

    if max_qtd:

        itens = itens.filter(
            quantidade__lte=max_qtd
        )

    if min_valor:

        itens = itens.filter(
            valor_unitario__gte=min_valor
        )

    total_itens = itens.aggregate(
        total=Sum('quantidade')
    )['total'] or 0

    valor_total = sum(
        i.valor_total for i in itens
    )

    return render(
        request,
        'relatorios.html',
        {
            'itens': itens,
            'total_itens': total_itens,
            'valor_total': valor_total
        }
    )


# PERFIL

@login_required
def perfil(request):

    erro = None
    sucesso = None
    acao = None

    usuario = request.user

    if request.method == 'POST':

        acao = request.POST.get('acao')

        # ====================================
        # ALTERAR NOME
        # ====================================

        if acao == 'nome':

            novo_nome = request.POST.get(
                'username'
            )

            senha = request.POST.get(
                'senha_atual'
            )

            if not usuario.check_password(senha):

                erro = 'Senha incorreta.'

                return render(
                    request,
                    'perfil.html',
                    {
                        'erro': erro,
                        'acao': 'nome'
                    }
                )

            usuario_existente = User.objects.filter(
                username=novo_nome
            ).exclude(
                id=usuario.id
            ).exists()

            if usuario_existente:

                erro = (
                    'Nome de usuário já utilizado.'
                )

                return render(
                    request,
                    'perfil.html',
                    {
                        'erro': erro,
                        'acao': 'nome'
                    }
                )

            usuario.username = novo_nome

            usuario.save()

            sucesso = (
                'Nome de usuário atualizado.'
            )

            acao = None

        # ====================================
        # ALTERAR SENHA
        # ====================================

        elif acao == 'senha':

            senha_atual = request.POST.get(
                'senha_atual'
            )

            nova_senha = request.POST.get(
                'nova_senha'
            )

            confirmar_senha = request.POST.get(
                'confirmar_senha'
            )

            if not usuario.check_password(
                senha_atual
            ):

                erro = 'Senha incorreta.'

                return render(
                    request,
                    'perfil.html',
                    {
                        'erro': erro,
                        'acao': 'senha'
                    }
                )

            if (
                not nova_senha or
                not confirmar_senha
            ):

                erro = (
                    'Preencha todos os campos.'
                )

                return render(
                    request,
                    'perfil.html',
                    {
                        'erro': erro,
                        'acao': 'senha'
                    }
                )

            if nova_senha != confirmar_senha:

                erro = (
                    'As novas senhas não coincidem.'
                )

                return render(
                    request,
                    'perfil.html',
                    {
                        'erro': erro,
                        'acao': 'senha'
                    }
                )

            usuario.set_password(
                nova_senha
            )

            usuario.save()

            update_session_auth_hash(
                request,
                usuario
            )

            sucesso = (
                'Senha atualizada com sucesso.'
            )

            acao = None

    return render(
        request,
        'perfil.html',
        {
            'erro': erro,
            'sucesso': sucesso,
            'acao': acao
        }
    )


# EXCLUIR PERFIL

@login_required
def excluir_perfil(request):

    erro = None

    if request.method == 'POST':

        senha = request.POST.get('senha')

        usuario = authenticate(
            request,
            username=request.user.username,
            password=senha
        )

        if usuario is None:

            erro = 'Senha incorreta.'

            return render(
                request,
                'perfil.html',
                {
                    'erro': erro,
                    'acao': 'excluir'
                }
            )

        request.user.delete()

        logout(request)

        return redirect('/')

    return redirect('/perfil/')