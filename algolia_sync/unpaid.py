# import frappe
# import json

# def unpaid_amt(doc,event):
#     unpaid_doc = frappe.get_doc('Sales Invoice',doc.name)

#     if unpaid_doc.customer=='Swiggy':
#         unpaid_doc.status='Unpaid'

#     unpaid_doc.save(ignore_permissions=True,
#     ignore_version=True)

