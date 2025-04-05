# Generated by Django 3.2.18 on 2025-04-05 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Desc', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Instuciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CodInstucion', models.IntegerField(max_length=200)),
                ('descripcion', models.TextField(max_length=800)),
                ('ciudad', models.CharField(max_length=200)),
                ('Departamento', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Municipios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Desc', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Desc', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=200)),
                ('Apellido', models.CharField(max_length=200)),
                ('TipoId', models.CharField(choices=[('TI', 'Tarjeta de Identidad'), ('CC', 'Cedula de Ciudadania'), ('P', 'Pasaporte')], max_length=20)),
                ('NroId', models.IntegerField(max_length=200)),
                ('Telefono', models.IntegerField(max_length=200)),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='RecursosInstucion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NomRecurso', models.CharField(max_length=200)),
                ('Cantidad', models.IntegerField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Desc', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Barrio', models.CharField(max_length=200)),
                ('Direccion', models.TextField(max_length=800)),
                ('Departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.departamento')),
                ('Municipio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.municipios')),
                ('Pais', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.pais')),
            ],
        ),
    ]
