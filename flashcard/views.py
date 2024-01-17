from django.shortcuts import render, redirect
from .models import Categoria, Flashcard
from django.contrib.messages import constants
from django.contrib import messages


def novo_flashcard(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/logar')

    if request.method == 'GET':
        categoria = Categoria.objects.all()
        dificuldade = Flashcard.DIFICULDADE_CHOICES
        flashcards = Flashcard.objects.all()

        categoria_filtrar = request.GET.get('categoria')
        dificuldade_filtrar = request.GET.get('dificuldade')

        if categoria_filtrar:
            flashcards = flashcards.filter(
                categoria__id=categoria_filtrar
                )

        if dificuldade_filtrar:
            flashcards = flashcards.filter(
                dificuldade=dificuldade_filtrar
            )

        return render(
            request,
            'novo_flashcard.html',
            {
                'categoria': categoria,
                'dificuldade': dificuldade,
                'flashcards': flashcards
             }
        )

    elif request.method == 'POST':
        pergunta = request.POST.get('pergunta')
        resposta = request.POST.get('resposta')
        categoria = request.POST.get('categoria')
        dificuldade = request.POST.get('dificuldade')

        if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
            messages.add_message(
                request,
                constants.ERROR,
                'Preencha os campos de pergunta e resposta',
                )
            return redirect('/flashcard/novo_flashcard')

        flashcard = Flashcard(
            user=request.user,
            pergunta=pergunta,
            resposta=resposta,
            categoria_id=categoria,
            dificuldade=dificuldade,
            )

        flashcard.save()

        messages.add_message(
            request,
            constants.SUCCESS,
            'Flashcard criado com sucesso'
        )
        return redirect('/flashcard/novo_flashcard')


def deletar_flashcard(request, id):
    flashcard = Flashcard.objects.get(id=id)

    if request.user.id != flashcard.user.id:
        messages.add_message(
            request,
            constants.ERROR,
            'Voce nao pode deletar esse flashcard!'
        )
        return redirect('/flashcard/novo_flashcard')

    flashcard.delete()
    messages.add_message(
        request,
        constants.SUCCESS,
        'Flashcard deletado com sucesso!'
    )

    return redirect('/flashcard/novo_flashcard')