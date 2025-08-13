from django.db import models
from django.core.validators import FileExtensionValidator
from secretariaescolar.validators import cpf_validator, cep_validator, phone_validator, validate_nota
from django.contrib.auth.models import User


class Class(models.Model):
    CLASS_CHOICES = (
        ("1A", "1º Ano A"),
        ("1B", "1º Ano B"),
        ("1C", "1º Ano C"),
        ("2A", "2º Ano A"),
        ("2B", "2º Ano B"),
        ("2C", "2º Ano C"),
        ("3A", "3º Ano A"),
        ("3B", "3º Ano B"),
        ("3C", "3º Ano C"),
    )

    ITINERARY_CHOICES = (
        ("DS", "Desenvolvimento de Sistemas"),
        ("CN", "Ciências da Natureza"),
        ("JG", "Desenvolvimento de Jogos"),
    )
    class_choices = models.CharField(max_length=50, choices=CLASS_CHOICES, blank=False, null=True, verbose_name="Turma")
    itinerary_choices = models.CharField(max_length=50, choices=ITINERARY_CHOICES, blank=False, null=True, verbose_name="Itinerário")
    def __str__(self):
        # Retorna a representação em texto da turma e do itinerário
        return f"{self.get_class_choices_display()} - {self.get_itinerary_choices_display()}"

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"

class Matter(models.Model):
    MATTER_CHOICES = (
        ("CH", "Ciências Humanas"),
        ("L", "Linguagens"),
        ("M", "Matemática"),
        ("CN", "Ciências da Natureza"),
    )
    matter_choices = models.CharField(max_length=50, choices=MATTER_CHOICES, blank=False, null=True, verbose_name="Área da disciplina")
    def __str__(self):
        # Retorna a representação em texto da matéria
        return f"{self.get_matter_choices_display()}"

    class Meta:
        verbose_name = "Área/Disciplina"
        verbose_name_plural = "Áreas/Disciplinas"

class Student(models.Model):
    full_name = models.CharField(
        max_length=200, verbose_name="Nome completo do aluno", null=True
    )

    registration_number = models.CharField(
        max_length=6, unique=True, verbose_name="Matrícula do aluno"
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Telefone do aluno (XX) 9XXXX-XXXX",
        validators=[phone_validator],
    )
    email = models.EmailField(max_length=100, verbose_name="E-mail do aluno")
    cpf = models.CharField(
        max_length=11,
        verbose_name="CPF do aluno",
        unique=True,
        validators=[cpf_validator],
    )
    birthday = models.DateField(max_length=10, verbose_name="Data de nascimento do aluno")
    adress = models.CharField(max_length=100, validators=[cep_validator], verbose_name="Endereço do aluno")
    class_choice = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name="Turma do aluno",
        related_name="student_class",
        blank=False,
        null=True,
    )


    def __str__(self):
        # Retorna o nome completo do aluno
        return self.full_name

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"


class Guardian(models.Model):
    full_name = models.CharField(
        max_length=200, verbose_name="Nome completo do responsável", null=True
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="Aluno do responsável",
        related_name="guardian_student",
        blank=False,
        null=True,
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Telefone do responsável (XX) 9XXXX-XXXX",
        validators=[phone_validator],
    )
    email = models.EmailField(max_length=100, verbose_name="E-mail do responsável")
    cpf = models.CharField(
        max_length=11,
        verbose_name="CPF do responsável",
        unique=True,
        validators=[cpf_validator],
    )
    birthday = models.DateField(max_length=10, verbose_name="Data de nascimento do responsável")
    adress = models.CharField(max_length=100, validators=[cep_validator], verbose_name="Endereço do responsável")

    def __str__(self):
        # Retorna o nome completo do responsável
        return self.full_name

    class Meta:
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"


class Professor(models.Model):
    """
    Modelo que representa o professor da escola.
    O campo 'user' vincula o professor ao usuário do Django para autenticação.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Usuário", related_name="professor", null=True, blank=True
    )  # Permite nulo para migração, mas validação impede salvar sem usuário
    full_name = models.CharField(
        max_length=200, verbose_name="Nome completo do professor", null=True
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Telefone do professor (XX) 9XXXX-XXXX",
        validators=[phone_validator],
    )
    email = models.EmailField(max_length=100, verbose_name="E-mail do professor")
    cpf = models.CharField(
        max_length=11,
        verbose_name="CPF do professor",
        unique=True,
        validators=[cpf_validator],
    )
    birthday = models.DateField(max_length=10, verbose_name="Data de nascimento do professor")
    adress = models.CharField(max_length=100, validators=[cep_validator], verbose_name="Endereço do professor")
    class_choice = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name="Turma do professor",
        related_name="professor_class",
        blank=False,
        null=True,
    )
    matter_choice = models.ForeignKey(
        Matter,
        on_delete=models.CASCADE,
        verbose_name="Disciplina do professor",
        related_name="professor_matter",
        blank=False,
        null=True,
    )

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.user:
            raise ValidationError({'user': 'O campo Usuário é obrigatório para o Professor.'})

    def __str__(self):
        # Retorna o nome completo do professor
        return self.full_name

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"


class Contract(models.Model):
    guardian = models.ForeignKey(
        Guardian,
        on_delete=models.CASCADE,
        verbose_name="Responsável",
        related_name="contract_guardian",
        blank=False,
        null=True,
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="Aluno",
        related_name="contract_student",
        blank=False,
        null=True,
    )

    uploaded_pdf = models.FileField(
        upload_to="contracts/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        verbose_name="Contrato em PDF"
    )

    def generate_contract_pdf(self):
        # Gera um PDF do contrato com os dados do responsável e do aluno (em português)
        from django.http import HttpResponse
        from reportlab.pdfgen import canvas
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="contrato_{self.id}_{self.guardian.full_name}-{self.student.full_name}.pdf"'
        )
        p = canvas.Canvas(response)
        p.drawString(100, 800, f"Contrato Nº: {self.id}")
        p.drawString(100, 780, f"Nome do Responsável: {self.guardian.full_name}")
        p.drawString(100, 760, f"Telefone do Responsável: {self.guardian.phone_number}")
        p.drawString(100, 740, f"E-mail do Responsável: {self.guardian.email}")
        p.drawString(100, 720, f"CPF do Responsável: {self.guardian.cpf}")
        p.drawString(100, 700, f"Data de Nascimento do Responsável: {self.guardian.birthday}")
        p.drawString(100, 680, f"Endereço do Responsável: {self.guardian.adress}")
        p.drawString(100, 640, f"Nome do Aluno: {self.student.full_name}")
        p.drawString(100, 620, f"Telefone do Aluno: {self.student.phone_number}")
        p.drawString(100, 600, f"E-mail do Aluno: {self.student.email}")
        p.drawString(100, 580, f"CPF do Aluno: {self.student.cpf}")
        p.drawString(100, 560, f"Data de Nascimento do Aluno: {self.student.birthday}")
        p.drawString(100, 540, f"Endereço do Aluno: {self.student.adress}")
        p.drawString(
            100, 500, f"Assinatura: _______________________________________________X"
        )
        p.showPage()
        p.save()
        return response

    def __str__(self):
        # Retorna uma descrição do contrato
        return f"Contrato de {self.student.full_name} e {self.guardian.full_name}"

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"


class Grade(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="Aluno",
        related_name="grade_student",
        blank=False,
        null=True,
    )

    classs = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name="Turma",
        related_name="grade_class",
        blank=False,
        null=True,
    )
    matter = models.ForeignKey(
        Matter,
        on_delete=models.CASCADE,
        verbose_name="Disciplina",
        related_name="grade_matter",
        blank=False,
        null=True,
    )
    grade_presence = models.FloatField(
         verbose_name="Nota de Presença",
         default=0,
         validators=[validate_nota],
    )
    grade_activity = models.FloatField(
         verbose_name="Nota de Atividade",
         default=0,
         validators=[validate_nota],
    )
    grade_evaluative = models.FloatField(
         verbose_name="Nota Avaliativa",
         default=0,
         validators=[validate_nota],
    )
    grade_final = models.FloatField(
         verbose_name="Nota Final",
         default=0,
         validators=[validate_nota],
         editable=False
    )
    class Meta:
        unique_together = (
            "student",
            "classs",
            "matter",
        )
    def save(self, *args, **kwargs):
        # Calcula a média final automaticamente ao salvar
        self.grade_final = (
            self.grade_presence + self.grade_activity + self.grade_evaluative
        ) / 3
        super().save(*args, **kwargs)
    def __str__(self):
        # Retorna uma descrição das notas do aluno
        return f"Notas de {self.student.full_name} em {self.classs} - {self.matter}"

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"

class Falta(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Aluno", related_name="faltas")
    data = models.DateField(verbose_name="Data da falta")
    motivo = models.CharField(max_length=200, verbose_name="Motivo", blank=True, null=True)
    class Meta:
        verbose_name = "Falta"
        verbose_name_plural = "Faltas"
    def __str__(self):
        return f"{self.student.full_name} - {self.data}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Notificação automática se o aluno ultrapassar 5 faltas
        if self.student.faltas.count() > 5:
            try:
                guardian = self.student.guardian_student.first()
                if guardian and guardian.email:
                    from django.core.mail import send_mail
                    send_mail(
                        subject=f"Alerta de faltas para {self.student.full_name}",
                        message=f"O aluno {self.student.full_name} já possui {self.student.faltas.count()} faltas. Favor verificar a situação acadêmica.",
                        from_email=None,
                        recipient_list=[guardian.email],
                        fail_silently=True,
                    )
            except Exception:
                pass

class Advertencia(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Aluno", related_name="advertencias")
    data = models.DateField(verbose_name="Data da advertência")
    motivo = models.CharField(max_length=200, verbose_name="Motivo")
    class Meta:
        verbose_name = "Advertência"
        verbose_name_plural = "Advertências"
    def __str__(self):
        return f"{self.student.full_name} - {self.data}"

class Suspensao(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Aluno", related_name="suspensoes")
    data = models.DateField(verbose_name="Data da suspensão")
    motivo = models.CharField(max_length=200, verbose_name="Motivo")
    dias = models.PositiveIntegerField(verbose_name="Dias de suspensão")
    class Meta:
        verbose_name = "Suspensão"
        verbose_name_plural = "Suspensões"
    def __str__(self):
        return f"{self.student.full_name} - {self.data} ({self.dias} dias)"

class Evento(models.Model):
    TIPOS_EVENTO = [
        ("prova", "Prova"),
        ("feriado", "Feriado"),
        ("reuniao", "Reunião"),
        ("entrega", "Entrega de Trabalho"),
        ("atividade", "Atividade"),
        ("outro", "Outro")
    ]
    titulo = models.CharField(max_length=100, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição", blank=True, null=True)
    data = models.DateTimeField(verbose_name="Data e hora")
    tipo = models.CharField(max_length=20, choices=TIPOS_EVENTO, verbose_name="Tipo de evento")
    turma = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Turma", related_name="eventos")
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Professor", related_name="eventos_prof")
    publico_alvo = models.CharField(max_length=20, choices=[('aluno','Aluno'),('professor','Professor'),('todos','Todos')], default='todos', verbose_name="Público alvo")
    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
    def __str__(self):
        return f"{self.titulo} - {self.data:%d/%m/%Y %H:%M}"
#teste tropa
