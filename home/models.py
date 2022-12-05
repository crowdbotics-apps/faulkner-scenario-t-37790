from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator


class App(models.Model):
    """
    An app the user has created in our platform. Includes metadata about the app such
    as name and description.

    id
    name='hamburger_flipper'
    description='Algo for determining when to flip burgers.'
    app_type=['Web', 'Mobile']
    framework=['Django', 'React Native']
    domain_name='example.com'
    screenshot='screenshot.uri'
    app_subscription=<Subscription>
    user=<User>
    created_at=<datetime>
    updated_at=<datetime>
    """
    APP_TYPE_CHOICES = [
        ('Web', 'Web'),
        ('Mobile', 'Mobile'),
    ]
    FRAMEWORK_CHOICES = [
        ('Django', 'Django'),
        ('React Native', 'React Native'),
    ]
    readonly_fields=('created_at', )

    name = models.CharField(max_length=50, db_index=True, unique=True, validators=[MinLengthValidator(1)])
    description = models.CharField(max_length=255, blank=True)
    app_type = models.CharField(max_length=255, db_index=True, choices=APP_TYPE_CHOICES)
    framework=models.CharField(max_length=255, db_index=True, choices=FRAMEWORK_CHOICES)
    domain_name = models.CharField(max_length=50, db_index=True, unique=True, blank=True)
    screenshot = models.CharField(max_length=255, blank=True)
    app_subscription = models.ForeignKey('home.Subscription', unique=True, db_index=True, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # PROTECT?
    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)

    def __str__(self):
        return f"App: {self.name} - {self.description} \n\tUser: {self.user} \n\t{self.app_subscription}"


class Plan(models.Model):
    """
    Plans to which a user can subscribe their app. Plans are billed on a monthly basis.

    id
    name='Free'
    description='Free Plan with $0 cost.'
    price=0.0
    created_at=<datetime>
    updated_at=<datetime>
    """
    readonly_fields=('created_at', )

    name = models.CharField(max_length=20, db_index=True, unique=True, validators=[MinLengthValidator(1)])
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=21, decimal_places=8)
    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)

    def __str__(self):
        return f"Plan: {self.name} - {self.description}"


class Subscription(models.Model):
    """
    Subscription tracks what plan is associated with an app. For record keeping
    subscriptions are never deleted, their active attribute is set to False.

    id
    user=<User>
    plan=<Plan>
    subscription_app=<App>
    active=False
    created_at=<datetime>
    updated_at=<datetime>
    """
    readonly_fields=('created_at', 'subscription_app')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True, blank=True, on_delete=models.CASCADE)
    plan = models.ForeignKey('home.Plan', db_index=True, on_delete=models.PROTECT) # CASCADE?
    subscription_app = models.ForeignKey('home.App', db_index=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)

    def __str__(self):
        return f"Subscription: App: {self.subscription_app.name} {self.plan}"



