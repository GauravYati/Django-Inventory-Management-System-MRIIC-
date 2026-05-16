# Generated after project cleanup.

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('mriic', '0004_item_item_desc'),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_qty',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='tags',
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text='A comma-separated list of tags.',
                through='taggit.TaggedItem',
                to='taggit.Tag',
                verbose_name='Tags',
            ),
        ),
    ]
