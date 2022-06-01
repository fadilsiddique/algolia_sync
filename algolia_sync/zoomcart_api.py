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
    Items = frappe.db.get_all("Item",filters = {"item_code":item_code},fields=["website_image_1"])
    return Items


@frappe.whitelist()
def order():
    user = frappe.session.user
    order_item = []
    so = frappe.db.get_all("Sales Order",filters = {"contact_email":user},fields=["order_status","name","transaction_date","delivery_date"])
    for i in so:
        sales_order = frappe.get_doc("Sales Order",i["name"])
        for item in sales_order.items:
            order_item.append({"Item_name":item.item_name,"item_code":item.item_code,"qty":item.qty,"order_status":i["order_status"],"transaction_date":i["transaction_date"],\
            "delivery_date":i["delivery_date"],"id":i["name"]})            
    return order_item

@frappe.whitelist()
def orderhistory():
    user = frappe.session.user
    sales_item = []
    item_list = []
    so = frappe.db.get_all("Sales Order",filters={"contact_email":user},fields=["name"])
    for i in so:
        sales_order = frappe.get_doc("Sales Order",i["name"])
        for item in sales_order.items:
            item_list.append({"item_name":item.item_name,"item_code":item.item_code,"Quantity":item.qty})
        sales_item.append({"sales_invoice_name":i["name"],"item_list":item_list})
        item_list = []
    return sales_item