from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mriic', '0005_cleanup_item_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='BorrowRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requester_name', models.CharField(max_length=100)),
                ('requester_email', models.EmailField(max_length=254)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('purpose', models.TextField(blank=True, max_length=500)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('returned', 'Returned'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrow_requests', to='mriic.item')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
