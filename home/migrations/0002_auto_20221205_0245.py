from datetime import datetime, timezone, timedelta

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion

from home.models import Plan

def seed_plans(apps, schema_editor):
    """
    Seed all plans.
    """
    free_plan = Plan.objects.create(name='Free',
        description='Free Plan with $0 cost.',
        price=0.0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    free_plan.save()

    standard_plan = Plan.objects.create(name='Standard',
        description='Standard Plan with $10 cost.',
        price=10.0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    standard_plan.save()

    pro_plan = Plan.objects.create(name='Pro',
        description='Pro Plan with $25 cost.',
        price=25.0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    pro_plan.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_load_initial_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(1)])),
                ('description', models.CharField(max_length=255)),
                ('app_type', models.CharField(choices=[('Web', 'Web'), ('Mobile', 'Mobile')], db_index=True, max_length=255)),
                ('framework', models.CharField(choices=[('Django', 'Django'), ('React Native', 'React Native')], db_index=True, max_length=255)),
                ('domain_name', models.CharField(db_index=True, max_length=50, unique=True)),
                ('screenshot', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(blank=True)),
                ('updated_at', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, unique=True, validators=[django.core.validators.MinLengthValidator(1)])),
                ('description', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=8, max_digits=21)),
                ('created_at', models.DateTimeField(blank=True)),
                ('updated_at', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(db_index=True, default=True)),
                ('created_at', models.DateTimeField(blank=True)),
                ('updated_at', models.DateTimeField(blank=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.Plan')),
                ('subscription_app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.App')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='app',
            name='app_subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.Subscription'),
        ),
        migrations.AddField(
            model_name='app',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(seed_plans,
            reverse_code=migrations.RunPython.noop),
    ]
