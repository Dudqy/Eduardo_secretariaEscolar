from django.core.exceptions import ValidationError
import re
from validate_docbr import CPF


def cpf_validator(value):
    """
    Valida se o CPF informado é válido.
    Aceita apenas números, sem pontos ou traços.
    """
    cpf = CPF()
    if not cpf.validate(value):
        raise ValidationError(
            ("O CPF '%(value)s' não é válido. Digite apenas números, sem pontos ou traços."),
            params={"value": value},
        )


def cep_validator(value):
    """
    Valida se o CEP informado possui 8 dígitos numéricos.
    """
    if not len(value) == 8:
        raise ValidationError(
            ("O CEP '%(value)s' deve conter 8 dígitos numéricos."),
            params={"value": value},
        )
    pattern = re.compile(r"(\d){5}(\d){3}")
    if not re.match(pattern, value):
        raise ValidationError(
            ("O CEP '%(value)s' deve conter apenas números."),
            params={"value": value},
        )


def phone_validator(value):
    """
    Valida se o telefone está no formato (XX) 9XXXX-XXXX.
    """
    pattern = r"^\(\d{2}\) 9\d{4}-\d{4}$"
    if not re.match(pattern, value):
        raise ValidationError(
            ("O telefone '%(value)s' deve estar no formato (XX) 9XXXX-XXXX."),
            params={"value": value},
        )


def validate_nota(value):
    """
    Valida se a nota está entre 0 e 10.
    """
    if not (0 <= value <= 10):
        raise ValidationError(
            f"Nota inválida: {value}. A nota deve estar entre 0 e 10."
        )
