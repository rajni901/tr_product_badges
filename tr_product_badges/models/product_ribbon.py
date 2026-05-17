from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductRibbon(models.Model):
    _inherit = 'product.ribbon'

    assign = fields.Selection(
        selection_add=[
            ('bestseller', 'Bestseller (by sales count)'),
            ('low_stock', 'Low Stock'),
            ('featured', 'Featured (manual)'),
        ],
        ondelete={
            'bestseller': 'set manual',
            'low_stock': 'set manual',
            'featured': 'set manual',
        },
    )
    bestseller_min_qty = fields.Integer(
        string='Min. Sales Qty for Bestseller',
        default=10,
        help='Products sold more than this quantity will get the Bestseller badge.',
    )
    low_stock_qty = fields.Integer(
        string='Low Stock Threshold',
        default=5,
        help='Products with stock below this quantity will get the Low Stock badge.',
    )

    @api.constrains('assign')
    def _check_assign(self):
        for ribbon in self:
            if ribbon.assign not in ('manual', 'featured'):
                existing = self.search([
                    ('id', '!=', ribbon.id),
                    ('assign', '=', ribbon.assign),
                ], limit=1)
                if existing:
                    raise ValidationError(_(
                        'Only one ribbon with assign "%s" is allowed.',
                        dict(self._fields['assign'].selection).get(ribbon.assign)
                    ))

    def action_apply_auto_rules(self):
        """Apply all auto-assign rules to products."""
        self.ensure_one()
        count = self._apply_rule()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Badge Applied'),
                'message': _(f'Applied "{self.name}" badge to {count} products.'),
                'type': 'success',
            },
        }

    def _apply_rule(self):
        ProductTemplate = self.env['product.template']
        count = 0

        if self.assign == 'bestseller':
            products = ProductTemplate.search([('website_published', '=', True)])
            for product in products:
                sold = sum(product.product_variant_ids.mapped('sales_count'))
                if sold >= self.bestseller_min_qty:
                    product.website_ribbon_id = self
                    count += 1

        elif self.assign == 'low_stock':
            products = ProductTemplate.search([
                ('website_published', '=', True),
                ('type', 'in', ['product', 'consu']),
            ])
            for product in products:
                if 0 < product.qty_available <= self.low_stock_qty:
                    product.website_ribbon_id = self
                    count += 1

        return count

    @api.model
    def _cron_apply_all_auto_rules(self):
        """Scheduled action to apply all auto-assign rules."""
        ribbons = self.search([('assign', 'in', ['bestseller', 'low_stock'])])
        for ribbon in ribbons:
            ribbon._apply_rule()
