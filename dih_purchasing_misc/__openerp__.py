{
    'name': 'Purchasing misc modifications',
    'description': '''
    Add "Analytic Account" field on RFQs to auto-fill analytic account on each line

    Add "Analytic Account" search field 

    Add "Analytic Account" column to list view of RFQs

    Add "Product Category" line on each Quotation line to filter Products

    Add fields to model and to form view for RFQs : 

    	-M2m tags for internal product category

    	-M2m tags for product category

    	-Different fields/selects by Antoine for conditions, hide text box with terms and conditions

    	-Expected PO Date

    	-Internal PO Number - incremented automatically, created by joining analytic account,year,increment

    Update string for RFQ line : change Scheduled Delivery Date to Expected Delivery Date

    Add new product.cat.leaf model to place in RFQs, describing the class of products (once internal product category is passed)

    For analytic accounts, added field for seqnames on the POs

    ''',
    'author': 'Kevin Khao',
    'depends': ['purchase', 'account'],
	'sequence': 17,
    'application': False,
    'data': [
        'views/dih_purchase_order_view.xml',
        'dih_purchase_order_sequence.xml',
        'views/dih_analytic_account_view.xml',
    ]
}
