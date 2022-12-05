from datetime import datetime, timezone, timedelta

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

from home.models import App, Plan, Subscription
from users.models import User

def seed_apps(apps, schema_editor):
    """
    Seed test apps and subscriptions.
    """
    super_user = User.objects.create(name='testuser')
    free_plan = Plan.objects.get(name='Free')
    standard_plan = Plan.objects.get(name='Standard')
    pro_plan = Plan.objects.get(name='Pro')

    burger_flip_app = App.objects.create(
        name='Hamburger Flipper',
        description='Web app for determining when to flip burgers.',
        app_type='Web',
        framework='Django',
        domain_name='burgerflip.com',
        screenshot='hostedimage.service.com/burger',
        user=super_user,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        )
    burger_flip_subscription = Subscription.objects.create(
        user=super_user,
        plan=free_plan,
        subscription_app=burger_flip_app,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        )
    burger_flip_subscription.save()
    burger_flip_app.app_subscription = burger_flip_subscription
    burger_flip_app.save()

    drone_light_show_app = App.objects.create(
        name='Drone Light Show',
        description='Mobile app for controlling drone light show.',
        app_type='Mobile',
        framework='React Native',
        domain_name='dronelights.com',
        screenshot='dronelights.com/images/drone',
        user=super_user,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        )
    drone_light_subscription = Subscription.objects.create(
        user=super_user,
        plan=standard_plan,
        subscription_app=drone_light_show_app,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        )
    drone_light_subscription.save()
    drone_light_show_app.app_subscription = drone_light_subscription
    drone_light_show_app.save()

    military_analytics_app = App.objects.create(
        name='Military Analytics',
        description='Web app for military analytics.',
        app_type='Web',
        framework='Django',
        domain_name='militaryanalytics.com',
        screenshot='militaryanalytics.com/images/data_graphs',
        user=super_user,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        )
    military_analytics_subscription = Subscription.objects.create(
        user=super_user,
        plan=pro_plan,
        subscription_app=military_analytics_app,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        )
    military_analytics_subscription.save()
    military_analytics_app.app_subscription = military_analytics_subscription
    military_analytics_app.save()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20221205_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='app_subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Subscription', unique=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='app',
            name='domain_name',
            field=models.CharField(blank=True, db_index=True, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='screenshot',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(seed_apps,
            reverse_code=migrations.RunPython.noop),
    ]
