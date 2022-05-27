import frappe
import json
import requests



@frappe.whitelist()
def address(email):
    address = frappe.db.get_all("Address",filters={"owner":email,"disabled":0},fields=["name","address_title","disabled","address_line1","address_line2","city","state","country","pincode","phone"])
    return address
        # return address

@frappe.whitelist()
def ItemFilter(item_code):
    Items = frappe.db.get_all("Item",filters = {"item_code":item_code},fields=["image"])
    return Items


# @frappe.whitelist()
# def emailSend():
#     doc=frappe.get_doc('Sales Invoice','SINV-22-00003')
#     # return doc.contact_email
#     email_args={
#         "recipients":doc.contact_email,
#         "message":"Please see your invoice",
#         "subject":"Sales Invoice",
#         "attachments":[frappe.attach_print(doc.doctype,doc.name,file_name=doc.name)],
#         "reference_doctype":doc.doctype,
#         "reference_name":doc.name
#     }
#     frappe.sendmail(**email_args,delayed=False)