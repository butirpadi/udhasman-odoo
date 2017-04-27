# -*- coding: utf-8 -*-
{
    'name': "udhasman",

    'summary': """
        Aplikasi Penjualan & Pembelian
        Karyawan
        Reporting
        UD Hasil Mancing""",

    'description': """
        Aplikasi UD Hasil Mancing
    """,

    'author': "Butirpadi",
    'website': "http://github.com/butirpadi",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'views/hs_toggle_leftbar.xml',
        'views/hs_provinsi_view.xml',
        'views/hs_kabupaten_view.xml',
        'views/hs_kecamatan_view.xml',
        'views/hs_lokasi_galian_view.xml',
        'views/hs_alat_berat_view.xml',
        'views/hs_armada_view.xml',
        'views/hs_product_unit_view.xml',
        'views/hs_karyawan_view.xml',
        'views/hs_product_template_view.xml',
        'views/hs_res_partner_supplier_view.xml',
        'views/hs_res_partner_customer_view.xml',
        'views/hs_pekerjaan_view.xml',
        'views/hs_purchase_view.xml',
        'views/hs_account_invoice_supplier_view.xml',
        'views/hs_account_payment_view.xml',
        'views/hs_sale_view.xml',
        'views/hs_stock_picking_view.xml',
        'views/hs_sale_make_invoice_advance_views.xml',
        'views/hs_account_invoice_view.xml',
        'views/menu.xml',
        # 'views/demo_appkonfig.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True
}