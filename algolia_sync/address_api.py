import frappe
import json
import requests



@frappe.whitelist(allow_guest=True)
def address(email):
    address = frappe.db.get_all("Address",filters={"owner":email},fields=["address_title","address_line1","address_line2","city","state","country","pincode","phone"])
    return address