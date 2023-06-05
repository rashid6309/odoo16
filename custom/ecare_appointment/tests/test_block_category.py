from odoo.tests import common, tagged
from logging import getLogger

_logger = getLogger(__name__)

from datetime import datetime, timedelta


class BlockCategoryTest(common.TransactionCase):

    def setUp(self):
        super(BlockCategoryTest, self).setUp()

    def test_block_slot_creation(self):
        _model = "ec.block.slot"
        model_obj = self.env[_model]

        # Give category_id which you want to test
        category_id = self.env['ec.slot.sub.category'].search(domain=[],
                                                              limit=1,
                                                              order="id asc")

        obj = model_obj.create({
            'category_id': category_id.id,
            'start_date': datetime.today() - timedelta(days=15),
            'end_date': datetime.today() + timedelta(days=15),
            'active_time': '10:00',
            'to_time': '12:00',
            'active': True
        })

        self.assertEqual(obj.active, 1)

        _logger.info("Test: BlockCategoryTest.test_block_slot_creation passed ...")

    def test_block_slot_unique_validation(self):
        self.test_block_slot_creation()
        self.test_block_slot_creation()

    def test_block_slot_functionality(self):
        category_ids = self.env['ec.slot.sub.category'].search(domain=[('active', '=', True)])

        block_slot_obj = self.env['ec.block.slot']
        if not block_slot_obj:
            _logger.info("No block slot available")
            return True

        today_date = datetime.today().date()
        block_slot_obj.prepare_block_slot_data(category_ids.ids, today_date)

        block_category_ids = block_slot_obj.search(domain=[('active', '=', True),
                                                  block_slot_obj         ('end_date', '>=', today_date)])

        result = block_slot_obj.check_slot_block(block_category_ids[0].category_id.id, "11:00", "11:30")
        self.assertEqual(result, True)

        result = block_slot_obj.check_slot_block(block_category_ids[0].category_id.id, "10:30", "11:00")
        self.assertEqual(result, True)
