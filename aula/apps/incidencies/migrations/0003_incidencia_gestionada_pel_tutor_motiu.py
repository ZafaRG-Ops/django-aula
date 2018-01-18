# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-17 16:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidencies', '0002_incidencia_gestionada_pel_tutor'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidencia',
            name='gestionada_pel_tutor_motiu',
            field=models.CharField(choices=[('1AHora', 'Retard de 1a hora'), ('ForaAula', "Incid\xe8ncia fora d'aula"), ('Guardia', 'Incid\xe8ncia en hora de Gu\xe0rdia'), ('N/A', 'Incid\xe8ncia gestionada pel tutor')], default=b'', max_length=20),
        ),
    ]