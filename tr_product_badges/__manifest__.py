{
    'name': 'Product Badges & Ribbons Pro',
    'version': '19.0.1.0.0',
    'category': 'Website/eCommerce',
    'summary': 'Advanced product badges: New, Sale, Hot, Bestseller, Low Stock with auto-assign rules',
    'description': """
Product Badges & Ribbons Pro — by Technical Rajni
==================================================
Extend Odoo's built-in ribbons with powerful auto-assign rules.

Features:
- Pre-built badge templates: NEW, SALE, HOT, BESTSELLER, LOW STOCK, FEATURED
- Auto-assign badges based on rules:
  - Sales count (Bestseller)
  - Stock quantity (Low Stock)
  - Creation date (New)
  - Discount (Sale)
  - Manual (Featured, Hot)
- Bulk assign badges to multiple products
- One-click apply all auto rules
- Scheduled auto-update cron job
    """,
    'author': 'Technical Rajni',
    'website': 'https://www.technicalrajni.com',
    'license': 'OPL-1',
    'depends': ['website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/badge_templates.xml',
        'data/scheduled_actions.xml',
        'views/product_ribbon_views.xml',
        'views/product_views.xml',
        'wizard/bulk_badge_wizard_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 12.00,
    'currency': 'USD',
}
