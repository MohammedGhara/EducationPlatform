from django.db import migrations
from django.contrib.auth.models import Group

def create_groups(apps, schema_editor):
    Group.objects.create(name='student')
    Group.objects.create(name='lecturer')
    Group.objects.create(name='parent')

class Migration(migrations.Migration):
    dependencies = [
        # Add any dependencies here
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
