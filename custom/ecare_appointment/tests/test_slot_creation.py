from odoo.tests import common, tagged
from logging import getLogger


_logger = getLogger(__name__)


class SlotConfigurationTest(common.TransactionCase):

    def setUp(self):
        super(SlotConfigurationTest, self).setUp()

    def test_session_inactive_categories(self):
        """
        As the case can arise when the category selected at the client side can be inactive or not found in the Server
        :return: Pass/Fail
        """
        _model = "ec.slot.category"
        slot_category_id = self.env[_model]

        parent_category_ids, active_parent_category_id, fetch_category, category_id =\
            slot_category_id.get_relevant_categories(parent_category_id=10000, active_category_id=100000)
        if not parent_category_ids:
            self.fail("Failed: Parent Categories not found.")

        if not active_parent_category_id:
            self.fail("Failed: Active Parent Category not found")

        if not fetch_category:
            self.fail("Failed: Fetch Category not found")

        if not category_id:
            self.fail("Failed: Category not found")

        self.assertEqual(parent_category_ids[0].id, active_parent_category_id)
        self.assertEqual(fetch_category[0].id, category_id.id)

        _logger.info("Test: SlotConfigurationTest.test_get_active_categories passed ...")
