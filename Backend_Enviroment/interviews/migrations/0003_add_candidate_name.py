# Generated manually to add candidate_name field
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0002_answer_feedback_answer_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateinterview',
            name='candidate_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
