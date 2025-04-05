from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import Usuario



class UsuarioCreationForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        print('Eso es lo que hay')


class UsuarioChangeForm(UserChangeForm):

    class Meta:
        model = Usuario
        fields = '__all__'