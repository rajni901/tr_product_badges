from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    tr_badge_notes = fields.Char(
        string='Badge Note',
        help='Internal note about why this badge was applied.',
    )
