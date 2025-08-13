# Importa as views de login/logout do Django
from django.contrib.auth.views import LoginView, LogoutView
# Funções para renderizar páginas e redirecionar
from django.shortcuts import render, redirect
# Para criar rotas/URLs
from django.urls import path
# Decorador para exigir login do usuário
from django.contrib.auth.decorators import login_required
# Importa os modelos usados nas views
from .models import Grade, Student, Class, Matter, Professor
# Para respostas HTTP (ex: PDF)
from django.http import HttpResponse
# Biblioteca para gerar PDFs
from reportlab.pdfgen import canvas

# Página inicial do sistema
def home(request):
    return render(request, 'home.html')

# Painel do aluno, mostra notas, faltas, advertências e suspensões
@login_required
def dashboard(request):
    try:
        # Busca o aluno pelo nome do usuário logado
        aluno = Student.objects.get(full_name=request.user.get_full_name())
    except Student.DoesNotExist:
        aluno = None
    # Busca as notas, faltas, advertências e suspensões do aluno
    grades = Grade.objects.filter(student=aluno) if aluno else []
    faltas = aluno.faltas.all()[:5] if aluno else []
    advertencias = aluno.advertencias.all()[:5] if aluno else []
    suspensoes = aluno.suspensoes.all()[:5] if aluno else []
    turma = grades[0].classs if grades else None
    serie = turma.get_class_choices_display() if turma else "-"
    # Renderiza o painel do aluno
    return render(request, 'dashboard.html', {
        'user': request.user,
        'aluno': aluno,
        'grades': grades[:5],
        'faltas': faltas,
        'advertencias': advertencias,
        'suspensoes': suspensoes,
        'turma': turma,
        'serie': serie,
    })

# Mostra médias por disciplina e alerta se média < 6
@login_required
def desempenho(request):
    # Busca todas as notas e matérias
    grades = Grade.objects.select_related('student', 'classs', 'matter')
    materias = Matter.objects.all()
    labels = [m.get_matter_choices_display() for m in materias]
    medias = []
    alertas = []
    for m in materias:
        # Calcula a média das notas finais por matéria
        notas = grades.filter(matter=m).values_list('grade_final', flat=True)
        if notas:
            media = round(sum(notas)/len(notas), 2)
            medias.append(media)
            # Adiciona alerta se média menor que 6
            if media < 6:
                alertas.append(f"{m.get_matter_choices_display()} (média: {media})")
        else:
            medias.append(0)
    alertas_html = '<br>'.join(alertas) if alertas else ''
    # Renderiza o desempenho do aluno
    return render(request, 'desempenho.html', {
        'labels': labels,
        'medias': medias,
        'alertas': alertas_html,
    })

# Mostra histórico completo do aluno (notas, faltas, advertências, suspensões)
@login_required
def historico(request):
    try:
        # Busca o aluno pelo nome do usuário logado
        aluno = Student.objects.get(full_name=request.user.get_full_name())
    except Student.DoesNotExist:
        aluno = None
    grades = Grade.objects.filter(student=aluno) if aluno else []
    faltas = aluno.faltas.all() if aluno else []
    advertencias = aluno.advertencias.all() if aluno else []
    suspensoes = aluno.suspensoes.all() if aluno else []
    faltas_excesso = len(faltas) > 5
    # Calcula média de presença
    if grades:
        media_presenca = round(sum([g.grade_presence for g in grades]) / len(grades), 2)
    else:
        media_presenca = 0
    # Renderiza o histórico do aluno
    return render(request, 'historico.html', {
        'grades': grades,
        'faltas': faltas,
        'faltas_excesso': faltas_excesso,
        'media_presenca': media_presenca,
        'advertencias': advertencias,
        'suspensoes': suspensoes,
    })

# Gera o histórico do aluno em PDF
@login_required
def historico_pdf(request):
    try:
        aluno = Student.objects.get(full_name=request.user.get_full_name())
    except Student.DoesNotExist:
        aluno = None
    grades = Grade.objects.filter(student=aluno) if aluno else []
    faltas = aluno.faltas.all() if aluno else []
    advertencias = aluno.advertencias.all() if aluno else []
    suspensoes = aluno.suspensoes.all() if aluno else []
    # Cria resposta PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="historico_{request.user.username}.pdf"'
    p = canvas.Canvas(response)
    # Escreve dados no PDF
    p.drawString(100, 800, f"Histórico Acadêmico de {request.user.get_full_name()}")
    y = 770
    p.drawString(100, y, "Turma | Disciplina | Presença | Atividade | Avaliativa | Final")
    y -= 20
    for g in grades:
        p.drawString(100, y, f"{g.classs} | {g.matter} | {g.grade_presence} | {g.grade_activity} | {g.grade_evaluative} | {g.grade_final}")
        y -= 20
        if y < 100:
            p.showPage()
            y = 800
    y -= 20
    p.drawString(100, y, "Faltas:")
    y -= 20
    for f in faltas:
        p.drawString(100, y, f"{f.data} - {f.motivo or 'Sem motivo'}")
        y -= 20
        if y < 100:
            p.showPage()
            y = 800
    y -= 20
    p.drawString(100, y, "Advertências:")
    y -= 20
    for adv in advertencias:
        p.drawString(100, y, f"{adv.data} - {adv.motivo}")
        y -= 20
        if y < 100:
            p.showPage()
            y = 800
    y -= 20
    p.drawString(100, y, "Suspensões:")
    y -= 20
    for s in suspensoes:
        p.drawString(100, y, f"{s.data} - {s.motivo} - {s.dias} dias")
        y -= 20
        if y < 100:
            p.showPage()
            y = 800
    p.save()
    return response

# View personalizada de login
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Define o template de login
    def get_success_url(self):
        user = self.request.user
        from .models import Student, Professor
        # Redireciona para o painel correto após login
        if Student.objects.filter(full_name=user.get_full_name()).exists():
            return '/dashboard/'
        elif Professor.objects.filter(user=user).exists():
            return '/dashboard-professor/'
        elif user.is_staff or user.is_superuser:
            return '/admin/'
        return '/'

# Painel do professor, mostra turmas, disciplinas, aulas dadas e dias trabalhados
@login_required
def dashboard_professor(request):
    try:
        professor = Professor.objects.get(user=request.user)
    except Professor.DoesNotExist:
        professor = None
    turmas = list(set([p.class_choice for p in Professor.objects.filter(user=request.user)])) if professor else []
    disciplinas = list(set([p.matter_choice for p in Professor.objects.filter(user=request.user)])) if professor else []
    grades = Grade.objects.filter(classs__in=turmas, matter__in=disciplinas) if professor else []
    from .models import Evento
    aulas_dadas = Evento.objects.filter(professor=professor, tipo__in=["atividade"]).count() if professor else 0
    dias_trabalhados = Evento.objects.filter(professor=professor).dates('data', 'day').count() if professor else 0
    # Renderiza o painel do professor
    return render(request, 'dashboard_professor.html', {
        'professor': professor,
        'turmas': turmas,
        'disciplinas': disciplinas,
        'grades': grades,
        'aulas_dadas': aulas_dadas,
        'dias_trabalhados': dias_trabalhados,
    })

# Lista de rotas/URLs do sistema
urlpatterns = [
    path('', home, name='home'),  # Página inicial
    path('dashboard/', dashboard, name='dashboard'),  # Painel do aluno
    path('dashboard-professor/', dashboard_professor, name='dashboard_professor'),  # Painel do professor
    path('desempenho/', desempenho, name='desempenho'),  # Página de desempenho
    path('historico/', historico, name='historico'),  # Página de histórico
    path('historico/pdf/', historico_pdf, name='historico_pdf'),  # PDF do histórico
    path('login/', CustomLoginView.as_view(), name='login'),  # Login
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Logout
]
