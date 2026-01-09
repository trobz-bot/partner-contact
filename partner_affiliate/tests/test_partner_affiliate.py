# Copyright 2024 Sygel Technology - Alberto Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import TransactionCase


class TestPartnerAffiliate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"].with_context(tracking_disable=True)

    def _create_partner_hierarchy(self):
        company = self.partner_model.create(
            {"name": "Parent Company", "is_company": True}
        )
        contact = self.partner_model.create(
            {"name": "Employee", "is_company": False, "parent_id": company.id}
        )
        archived_contact = self.partner_model.create(
            {
                "name": "Former Employee",
                "is_company": False,
                "parent_id": company.id,
                "active": False,
            }
        )
        affiliate = self.partner_model.create(
            {"name": "Affiliate Company", "is_company": True, "parent_id": company.id}
        )
        archived_affiliate = self.partner_model.create(
            {
                "name": "Old Affiliate",
                "is_company": True,
                "parent_id": company.id,
                "active": False,
            }
        )
        return company, contact, archived_contact, affiliate, archived_affiliate

    def test_child_ids_only_show_contacts(self):
        company, contact, *_ = self._create_partner_hierarchy()
        self.assertEqual(set(company.child_ids.ids), {contact.id})

    def test_affiliate_ids_only_show_companies(self):
        company, _, _, affiliate, _ = self._create_partner_hierarchy()
        self.assertEqual(set(company.affiliate_ids.ids), {affiliate.id})
        field_context = self.partner_model._fields["affiliate_ids"].context
        self.assertFalse(field_context.get("active_test", True))
