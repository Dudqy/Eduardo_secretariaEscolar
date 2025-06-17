from django.test import TestCase
from django.core.exceptions import ValidationError
from .validators import cpf_validator, cep_validator, phone_validator, validate_nota

class ValidatorTests(TestCase):
    def test_cpf_validator_valido(self):
        # CPF válido (exemplo fictício)
        try:
            cpf_validator('39053344705')
        except ValidationError:
            self.fail('cpf_validator levantou ValidationError para um CPF válido.')

    def test_cpf_validator_invalido(self):
        with self.assertRaises(ValidationError):
            cpf_validator('12345678900')

    def test_cep_validator_valido(self):
        try:
            cep_validator('12345678')
        except ValidationError:
            self.fail('cep_validator levantou ValidationError para um CEP válido.')

    def test_cep_validator_invalido(self):
        with self.assertRaises(ValidationError):
            cep_validator('1234')

    def test_phone_validator_valido(self):
        try:
            phone_validator('(12) 91234-5678')
        except ValidationError:
            self.fail('phone_validator levantou ValidationError para um telefone válido.')

    def test_phone_validator_invalido(self):
        with self.assertRaises(ValidationError):
            phone_validator('12345678')

    def test_validate_nota_valida(self):
        try:
            validate_nota(8)
        except ValidationError:
            self.fail('validate_nota levantou ValidationError para uma nota válida.')

    def test_validate_nota_invalida(self):
        with self.assertRaises(ValidationError):
            validate_nota(12)
