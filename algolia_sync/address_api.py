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