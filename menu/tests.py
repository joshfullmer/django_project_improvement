from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from menu.models import Menu, Item, Ingredient


class MenuTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="josh", email="josh@josh.com", password="top_secret")
        self.ingredient1 = Ingredient.objects.create(name="Ketchup",)
        self.ingredient2 = Ingredient.objects.create(name="Mustard",)
        self.ingredient3 = Ingredient.objects.create(name="BBQ",)
        self.item1 = Item.objects.create(
            name="hotdog",
            description="A hotdog.",
            chef=self.user,
            standard=True)
        self.item1.ingredients.set([self.ingredient1, self.ingredient2])
        self.item2 = Item.objects.create(
            name='chicken',
            description='Chicken.',
            chef=self.user,
            standard=True)
        self.item2.ingredients.set([self.ingredient2, self.ingredient3])
        self.menu = Menu.objects.create(season="Now")
        self.menu.items.set([self.item1])

    def test_menu_list(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_menu_detail(self):
        resp = self.client.get('/menu/{}/'.format(self.menu.pk))
        self.assertEqual(resp.status_code, 200)

    def test_menu_create(self):
        menu_count = Menu.objects.count()
        data = {'season': 'TEST',
                'items': [self.item1.id, self.item2.id],
                'expiration_date': '12/12/2018'}
        resp = self.client.post(
            reverse('menu:menu_new'),
            data,
            format='json',
            follow=True)
        menu = Menu.objects.order_by('-id')[0]
        print(resp.status_code)
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')
        self.assertRedirects(resp, '/menu/{}/'.format(menu.id))
        self.assertEqual(Menu.objects.count(), menu_count+1)

    def test_menu_edit(self):
        data = {'season': 'Then',
                'items': [self.item1.id, self.item2.id],
                'expiration_date': '01/01/2019'}
        resp = self.client.post(
            reverse('menu:menu_edit', args=[self.menu.id]),
            data,
            format='json',
            follow=True)
        print(resp.content)
        menu = Menu.objects.order_by('-id')[0]
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')
        self.assertRedirects(resp, '/menu/{}/'.format(self.menu.id))
        self.assertEqual(menu.season, 'Then')

    def test_menu_edit_to_new(self):
        menu_count = Menu.objects.count()
        data = {'season': 'Then',
                'items': [self.item1.id, self.item2.id],
                'expiration_date': '01/01/2019'}
        resp = self.client.post(
            reverse('menu:menu_edit', args=[0]),
            data,
            format='json',
            follow=True)
        menu = Menu.objects.order_by('-id')[0]
        self.assertRedirects(resp, '/menu/{}/'.format(menu.id))
        self.assertEqual(Menu.objects.count(), menu_count+1)

    def test_menu_edit_get(self):
        resp = self.client.get(reverse('menu:menu_edit', args=[self.menu.id]))
        self.assertEqual(resp.status_code, 200)


class ItemTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="josh", email="josh@josh.com", password="top_secret")
        self.ingredient1 = Ingredient.objects.create(name="Ketchup",)
        self.ingredient2 = Ingredient.objects.create(name="Mustard",)
        self.ingredient3 = Ingredient.objects.create(name="BBQ",)
        self.item1 = Item.objects.create(
            name="hotdog",
            description="A hotdog.",
            chef=self.user,
            standard=True)
        self.item1.ingredients.set([self.ingredient1, self.ingredient2])
        self.menu = Menu.objects.create(season="Now")
        self.menu.items.set([self.item1])

    def test_item_detail(self):
        resp = self.client.get('/menu/item/{}/'.format(self.item1.pk))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/item_detail.html')

    def test_item_edit(self):
        data = {'name': 'hamburger',
                'description': '4444\rA hamburger.',
                'chef': self.user.id,
                'standard': False,
                'ingredients': [self.ingredient1.id, self.ingredient3.id]}
        resp = self.client.post(
            reverse('menu:item_edit', args=[self.item1.id]),
            data,
            format='json',
            follow=True)
        item = Item.objects.get(pk=self.item1.id)
        self.assertTemplateUsed(resp, 'menu/item_detail.html')
        self.assertRedirects(resp, '/menu/item/{}/'.format(item.id))
        self.assertEqual(item.name, 'hamburger')

    def test_item_edit_to_new(self):
        item_count = Item.objects.count()
        data = {'name': 'hamburger',
                'description': '4444\rA hamburger.',
                'chef': self.user.id,
                'standard': False,
                'ingredients': [self.ingredient1.id, self.ingredient3.id]}
        resp = self.client.post(
            reverse('menu:item_edit', args=[0]),
            data,
            format='json',
            follow=True)
        item = Item.objects.order_by('-id')[0]
        self.assertRedirects(resp, '/menu/item/{}/'.format(item.id))
        self.assertEqual(Item.objects.count(), item_count+1)

    def test_item_edit_get(self):
        resp = self.client.get(reverse('menu:item_edit', args=[self.item1.id]))
        self.assertEqual(resp.status_code, 200)
