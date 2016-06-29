import unittest

from BitnFly.api import BitnFly


class UserSettings(object):

    roles = [
        'admin', 'moderator',
        'staff', 'anonymous'
    ]

    options = [
        'can_read', 'can_delete',
        'can_edit', 'can_publish'  # high bits
    ]


class TestBitsFly(unittest.TestCase):

    def setUp(self):

        self.admin = BitnFly(
            UserSettings.roles + UserSettings.options
        )

        self.mod = BitnFly(
            UserSettings.roles + UserSettings.options
        )

    def test_is_set(self):

        self.assertTrue(self.admin._is_set('can_read'))
        self.assertTrue(self.admin._is_set('anonymous'))

        self.assertTrue(self.mod._is_set('can_read'))
        self.assertFalse(self.mod.flip('anonymous')._is_set('anonymous'))

    def test_get(self):

        self.assertTrue(self.admin.get())
        self.assertTrue(self.admin.get() >= 0)
        self.assertEqual(255, self.admin.get())
        self.assertFalse(self.admin.get(9))
        self.assertFalse(self.admin.get(9))
        self.assertFalse(self.admin.get(3))
        self.assertEqual(0, self.admin.get(256))
        self.assertTrue(self.admin.get('admin'))
        self.assertTrue(self.admin.get(1))
        self.assertTrue(self.admin.get(2))
        self.assertTrue(self.admin.get(4))
        self.assertTrue(self.admin.get(8))
        self.assertTrue(self.admin.get(16))
        self.assertTrue(self.admin.get(32))
        self.assertTrue(self.admin.get(64))
        self.assertTrue(self.admin.get(128))
        self.assertFalse(self.admin.flip('anonymous').get('anonymous'))
        self.assertTrue(self.mod.get())
        self.assertTrue(self.mod.get() >= 0)

        with self.assertRaises(TypeError):
            self.admin.get(['1'])

    def test_init(self):

        flag, mask = self.admin._init()
        self.assertEqual(flag, 255)
        self.assertEqual(mask, 255)

        flag, mask = self.mod._init()

        self.assertEqual(flag, 255)
        self.assertEqual(mask, 255)

        # TODO: more tests

    def test_flip_nums_admin(self):

        # flip nums

        self.admin.flip(1)
        self.assertFalse(self.admin._is_set('admin'))
        self.admin.flip(2)
        self.assertFalse(self.admin._is_set('moderator'))

        self.admin.flip(1)
        self.assertTrue(self.admin._is_set('admin'))
        self.admin.flip(2)
        self.assertTrue(self.admin._is_set('moderator'))

        self.admin.flip([1, 2])
        self.assertFalse(self.admin._is_set('admin'))
        self.assertFalse(self.admin._is_set('moderator'))

        self.admin.flip([1, 2])
        self.assertTrue(self.admin._is_set('admin'))
        self.assertTrue(self.admin._is_set('moderator'))

    def test_flip_names_admin(self):

        # flip names
        self.admin.flip('admin')
        self.assertFalse(self.admin._is_set('admin'))

        self.admin.flip('admin')
        self.assertTrue(self.admin._is_set('admin'))

        self.admin.flip(['admin', 'moderator'])
        self.assertFalse(self.admin._is_set('admin'))
        self.assertFalse(self.admin._is_set('moderator'))

    def test_flip_nums_mod(self):

        # flip nums
        # moderator sections

        self.mod.flip(2)
        self.assertFalse(self.mod._is_set('moderator'))
        self.mod.flip(4)
        self.assertFalse(self.mod._is_set('staff'))

        self.mod.flip(2)
        self.assertTrue(self.mod._is_set('moderator'))
        self.mod.flip(4)
        self.assertTrue(self.mod._is_set('staff'))

        self.mod.flip([2, 4])
        self.assertFalse(self.mod._is_set('staff'))
        self.assertFalse(self.mod._is_set('moderator'))

        self.mod.flip([2, 4])
        self.assertTrue(self.mod._is_set('staff'))
        self.assertTrue(self.mod._is_set('moderator'))

    def test_flip_nums_mod_attr(self):

        self.admin.reset()

        self.admin.flip(self.admin.CAN_READ)
        self.assertFalse(self.admin._is_set('can_read'))
        self.admin.flip(self.admin.CAN_READ)

        self.admin.flip([self.admin.CAN_READ, self.admin.CAN_EDIT])
        self.assertFalse(self.admin._is_set('can_read'))
        self.assertFalse(self.admin._is_set('can_edit'))

    def test_flip_names_mod(self):

        # flip names
        self.mod.flip('moderator')
        self.assertFalse(self.mod._is_set('moderator'))

        self.mod.flip('moderator')
        self.assertTrue(self.mod._is_set('moderator'))
        self.mod.flip(['staff', 'moderator'])
        self.assertFalse(self.mod._is_set('staff'))
        self.assertFalse(self.mod._is_set('moderator'))

    def test_usersettings_options(self):

        admin = self.admin
        self.assertEqual(admin.get(), 255)

        admin.flip('can_read').get()
        self.assertFalse(admin._is_set('can_read'))
        self.assertEqual(0, admin.off().get())

    def test_off(self):

        admin = self.admin
        self.assertEqual(255, admin.get())

        admin.off()
        self.assertEqual(0, admin.get())

        admin.on()
        self.assertEqual(255, admin.get())

    def test_on(self):

        admin = self.admin
        self.assertEqual(admin.on().get(), 255)

    def test_reset(self):

        admin = self.admin
        admin.off()
        admin.reset()
        self.assertEqual(255, admin.get())

    def test_bitwise_and(self):

        admin = self.admin

        b = BitnFly(['lamp', 'contact', 'door', 'camera'], output=bin)
        c = BitnFly(['read', 'delete', 'write', 'execute'], output=bin)

        self.assertTrue(admin & 1)
        self.assertTrue(admin & 'admin')

        self.assertTrue((admin & 'admin') and (admin & 'moderator'))
        admin ^= 'anonymous'
        self.assertFalse((admin & 'admin') and (admin & 'anonymous'))

    def test_bitwise_xor(self):

        admin = self.admin
        self.assertTrue(admin & 1)

        admin ^= 'admin'
        self.assertFalse(admin & 'admin')

        admin ^= 'admin'
        self.assertTrue(admin & 'admin')

        admin ^= 1
        self.assertFalse(admin & 1)

        admin ^= 1
        self.assertTrue(admin & 1)

        admin ^= 2
        self.assertFalse(admin & 2)

    def test_or(self):

        self.admin.reset()
        self.admin.off()

        self.admin |= 1
        self.assertTrue(self.admin & 1)

        self.admin |= [2, 4, 8]

        self.assertTrue(self.admin & 2)
        self.assertTrue(self.admin & 4)
        self.assertTrue(self.admin & 8)

        self.admin |= 'can_read'
        self.assertTrue(self.admin & 16)

        self.admin |= ['can_edit', 'can_publish', 'can_delete']
        self.assertEqual(255, self.admin.get())

    def test_repr(self):

        admin = self.admin
        admin.reset()
        self.assertEqual(
            'BitnFly({}, mask={})'.format(
                [flag.lower() for flag in admin.flags().keys()],
                admin.mask(),
            ),
            repr(admin)
        )

    def test_str(self):
        self.admin.reset()
        self.assertEqual(str(self.admin), '255')

    def test_getattr(self):
        with self.assertRaises(AttributeError):
            print(self.admin.nothere)