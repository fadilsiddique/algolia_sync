import frappe
import json
import requests



@frappe.whitelist()
def address(email):
    address = frappe.db.get_all("Address",filters={"owner":email,"disabled":0},fields=["name","address_title","disabled",\
    "address_line1","address_line2","city","state","country","pincode","phone"])

    doc=frappe.get_doc("Address",address[0]['name'])

    for i in doc.links:
        link_name=i.link_name

        return address, link_name
        # return address
    return address, link_name

@frappe.whitelist()
def ItemFilter(item_code):
    Items = frappe.db.get_all("Item",filters = {"item_code":item_code},fields=["website_image_1"])
    return Items


@frappe.whitelist()
def order():
    user = frappe.session.user
    sales_item = []
    order_item = []
    so = frappe.db.get_all("Sales Order",filters = {"contact_email":user},fields=["order_status","name","transaction_date","delivery_date","grand_total",\
    "total_taxes_and_charges","status"])
    for i in so:
        sales_order = frappe.get_doc("Sales Order",i["name"])
        for item in sales_order.items:
            imageItem = frappe.get_doc('Item',item.item_code)
            order_item.append({"Item_name":item.item_name,"item_code":item.item_code,"qty":item.qty,"price":item.amount,"Image":imageItem.website_image_1,"order_status":i["order_status"],\
            "transaction_date":i["transaction_date"],"status":i["status"],\
            "delivery_date":i["delivery_date"],"id":i["name"]})     

        sales_item.append({"sales_invoice_name":i["name"],"Grand Total":i["grand_total"],"Tax":i["total_taxes_and_charges"],"Response":order_item})
        order_item = []

    return sales_item

@frappe.whitelist()
def orderhistory():
    user = frappe.session.user
    sales_item = []
    item_list = []
    so = frappe.db.get_all("Sales Order",filters={"contact_email":user},fields=["name"])
    for i in so:
        sales_order = frappe.get_doc("Sales Order",i["name"])
        for item in sales_order.items:
            imageItem = frappe.get_doc('Item',item.item_code)
            item_list.append({"item_name":item.item_name,"price":item.amount,"item_code":item.item_code,"Quantity":item.qty,"Image":imageItem.website_image_1})
        sales_item.append({"sales_invoice_name":i["name"],"item_list":item_list})
        item_list = []
    return sales_item