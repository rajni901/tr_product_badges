from odoo import _, api, fields, models


class BulkBadgeWizard(models.TransientModel):
    _name = 'bulk.badge.wizard'
    _description = 'Bulk Assign Badge to Products'

    ribbon_id = fields.Many2one('product.ribbon', string='Badge', required=True)
    product_ids = fields.Many2many('product.template', string='Products')
    action = fields.Selection([
        ('assign', 'Assign Badge'),
        ('remove', 'Remove Badge'),
    ], string='Action', default='assign', required=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            res['product_ids'] = [(6, 0, active_ids)]
        return res

    def action_apply(self):
        self.ensure_one()
        count = 0
        for product in self.product_ids:
            if self.action == 'assign':
                product.website_ribbon_id = self.ribbon_id
            else:
                product.website_ribbon_id = False
            count += 1
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Done'),
                'message': _(f'Badge {"assigned to" if self.action == "assign" else "removed from"} {count} products.'),
                'type': 'success',
                'sticky': False,
            },
        }
