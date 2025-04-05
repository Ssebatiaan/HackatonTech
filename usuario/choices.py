from djchoices import DjangoChoices, ChoiceItem



class TIPO_USUARIO(DjangoChoices):
    USUARIO = ChoiceItem('USUARIO')
    COORDINADOR = ChoiceItem('COORDINADOR')
    ADMINISTRADOR_SISTEMA = ChoiceItem('ADMINISTRADOR_SISTEMA')