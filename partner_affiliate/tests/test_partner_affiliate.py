# Copyright 2024 Sygel Technology - Alberto Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import TransactionCase


class TestPartnerAffiliate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Disable chatter tracking to speed up tests and avoid side effects.
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.partner_model = cls.env["res.partner"]

    def setUp(self):
        super().setUp()
        self.company = self.partner_model.create(
            {"name": "Parent Company", "is_company": True}
        )
        self.contact = self.partner_model.create(
            {
                "name": "Employee",
                "is_company": False,
                "parent_id": self.company.id,
            }
        )
        self.archived_contact = self.partner_model.create(
            {
                "name": "Former Employee",
                "is_company": False,
                "parent_id": self.company.id,
                "active": False,
            }
        )
        self.affiliate = self.partner_model.create(
            {
                "name": "Affiliate Company",
                "is_company": True,
                "parent_id": self.company.id,
            }
        )
        self.archived_affiliate = self.partner_model.create(
            {
                "name": "Old Affiliate",
                "is_company": True,
                "parent_id": self.company.id,
                "active": False,
            }
        )

    def test_child_ids_only_show_contacts(self):
        self.assertEqual(set(self.company.child_ids.ids), {self.contact.id})

    def test_affiliate_ids_only_show_companies(self):
        self.assertEqual(set(self.company.affiliate_ids.ids), {self.affiliate.id})
        field_context = self.partner_model._fields["affiliate_ids"].context
        self.assertFalse(field_context.get("active_test", True))
