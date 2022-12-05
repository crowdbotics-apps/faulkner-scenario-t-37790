from datetime import datetime, timezone, timedelta

from django.test import TestCase
from django.urls import reverse

from home.models import App, Plan, Subscription
from users.models import User


class AppTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(name='testuser')
        cls.app = App.objects.create(
            name='Hamburger Flipper - test',
            description='Web app for determining when to flip burgers. - test',
            app_type='Web',
            framework='Django',
            domain_name='burgerflip.com- test',
            screenshot='hostedimage.service.com/burger- test',
            user=cls.user,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            )

    def test_app_content(self):
        self.assertEqual(self.app.name, 'Hamburger Flipper - test')
        self.assertEqual(self.app.description, 'Web app for determining when to flip burgers. - test')
        self.assertEqual(self.app.app_type, 'Web')
        self.assertEqual(self.app.framework, 'Django')
        self.assertEqual(self.app.domain_name, 'burgerflip.com- test')
        self.assertEqual(self.app.screenshot, 'hostedimage.service.com/burger- test')
        self.assertEqual(self.app.user, self.user)

    def test_url_exists_at_correct_location(self):
        response = self.client.get('/api/v1/apps/')
        self.assertEqual(response.status_code, 200)

    def test_app_list(self):
        response = self.client.get('/api/v1/apps/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hamburger Flipper')
        self.assertContains(response, 'Drone Light Show')
        self.assertContains(response, 'Military Analytics')
        self.assertContains(response, 'Hamburger Flipper - test')

    def test_app_create(self):
        data = {
            "name": "test app",
            "description": "app for testing, created by POST",
            "app_type": "Web",
            "framework": "Django",
            "domain_name": "string",
            "screenshot": "string",
            "user": self.user.id,
            "created_at": "2022-12-05T06:08:02.325Z",
            "updated_at": "2022-12-05T06:08:02.325Z"
        }
        response = self.client.post('/api/v1/apps/', data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/apps/')
        self.assertContains(response, 'test app')

    def test_app_get(self):
        response = self.client.get('/api/v1/apps/1/')
        self.assertContains(response, 'Hamburger Flipper')

    def test_app_put(self):
        data = {
            "name": "Hamburger Flipper - test",
            "description": "Web app for determining when to flip burgers. - test",
            "app_type": "Web",
            "framework": "Django",
            "domain_name": "mydomain.com",
            "screenshot": "string",
            "user": self.user.id,
            "created_at": "2022-12-05T06:08:02.325Z",
            "updated_at": "2022-12-05T06:08:02.325Z"
        }
        response = self.client.put('/api/v1/apps/4/', data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/v1/apps/')
        self.assertContains(response, 'mydomain.com')

    def test_app_patch(self):
        data = {
            "domain_name": "mydomainpatched.com"
        }
        response = self.client.patch('/api/v1/apps/4/', data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/v1/apps/')
        self.assertContains(response, 'mydomainpatched.com')

    def test_app_delete(self):
        response = self.client.delete('/api/v1/apps/4/')
        self.assertEqual(response.status_code, 204)

        # make sure that the app was deleted
        response = self.client.get('/api/v1/apps/')
        try:
            self.assertContains(response, 'mydomainpatched.com')
            raise Exception('App DELETE failed.')
        except AssertionError:
            pass


class PlanTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.plan = Plan.objects.get(name='Free')

    def test_plan_content(self):
        self.assertEqual(self.plan.name, 'Free')
        self.assertEqual(self.plan.description, 'Free Plan with $0 cost.')
        self.assertEqual(self.plan.price, 0.0)

    def test_url_exists_at_correct_location(self):
        response = self.client.get('/api/v1/plans/')
        self.assertEqual(response.status_code, 200)

    def test_plan_list(self):
        response = self.client.get('/api/v1/plans/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Free')
        self.assertContains(response, 'Standard')
        self.assertContains(response, 'Pro')

    def test_plan_get(self):
        response = self.client.get('/api/v1/plans/1/')
        self.assertContains(response, 'Free')


class SubscriptionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(name='testuser')
        cls.burger_app = App.objects.get(name='Hamburger Flipper')
        cls.subscription = cls.burger_app.app_subscription

    def test_subscription_content(self):
        self.assertEqual(self.subscription.user, self.user)
        self.assertEqual(self.subscription.plan.name, 'Free')
        self.assertEqual(self.subscription.subscription_app, self.burger_app)
        self.assertEqual(self.subscription.active, True)

    def test_url_exists_at_correct_location(self):
        response = self.client.get('/api/v1/subscriptions/')
        self.assertEqual(response.status_code, 200)

    def test_subscription_list(self):
        response = self.client.get('/api/v1/subscriptions/')
        self.assertEqual(response.status_code, 200)

    def test_subscription_create(self):
        # create test app for test subscription
        data = {
            "name": "test app",
            "description": "app for testing, created by POST",
            "app_type": "Web",
            "framework": "Django",
            "domain_name": "string",
            "screenshot": "string",
            "user": self.user.id,
            "created_at": "2022-12-05T06:08:02.325Z",
            "updated_at": "2022-12-05T06:08:02.325Z"
        }
        response = self.client.post('/api/v1/apps/', data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/apps/')
        self.assertContains(response, 'test app')
        test_app_response = self.client.get('/api/v1/apps/4/')

        # test creating/assigning subscription
        subscription_data = {
            "user": self.user.id,
            "plan": Plan.objects.get(name='Free').id,
            "subscription_app": test_app_response.data['id'],
            "created_at": "2022-12-05T06:08:02.325Z",
            "updated_at": "2022-12-05T06:08:02.325Z"
        }
        subscription_response = self.client.post('/api/v1/subscriptions/', subscription_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_subscription_get(self):
        response = self.client.get('/api/v1/subscriptions/1/')
        burger_app = App.objects.get(id=response.json()['subscription_app'])
        self.assertEqual(burger_app.name, 'Hamburger Flipper')

    def test_subscription_put(self):
        app_response = self.client.get('/api/v1/apps/1/')
        data = {
            "user": self.user.id,
            "plan": Plan.objects.get(name='Standard').id,
            "subscription_app": app_response.json()['id'],
            "created_at": "2022-12-05T06:08:02.325Z",
            "updated_at": "2022-12-05T06:08:02.325Z"
        }
        response = self.client.put('/api/v1/subscriptions/1/', data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_subscription_patch(self):
        data = {
            "plan": Plan.objects.get(name='Pro').id,
        }
        response = self.client.patch('/api/v1/subscriptions/1/', data, content_type='application/json')
        self.assertEqual(response.status_code, 200)



