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
            item_list.append({"item_name":item.item_name,"price":item.amount,"item_code":item.item_code,\
            "Quantity":item.qty,"Image":imageItem.website_image_1})
            
        sales_item.append({"sales_invoice_name":i["name"],"item_list":item_list})
        item_list = []
    return sales_item

@frappe.whitelist()
def latest_items():
    attribute_list = []
    price_list = []
    web_item = frappe.db.get_all('Website Item',
                                                filters={'has_variants':0},
                                                fields={
                                                    'item_code'
                                                    },
                                                order_by="creation desc",
                                                limit_start=0, 
                                                limit_page_length= 8
                                )
    for web in web_item:
        items = frappe.db.get_list('Item',

                filters={
                    'item_code':web["item_code"] ,
                    'has_variants':0
                    },
            
                fields=["item_code",'item_name','creation','website_image_1','website_image_2','website_image_3','website_image_4','best_seller'])
        

        price = frappe.get_doc('Item Price',web.item_code)
        attribute_list.append({"Item Details" :items,"Price":price.price_list_rate})

    # items_list.append({"Items":attribute_list})
    return attribute_list

@frappe.whitelist()
def Featured():
    Items = frappe.db.get_all("Item",filters = {"featured_item_":1},fields=["item_name" , "item_code", 'creation',
                                                                            'website_image_1','website_image_2',
                                                                            'website_image_3','website_image_4','best_seller'])
        
    return Items


@frappe.whitelist()
def Categories():
    attributes = frappe.db.get_list('Item Attribute',filters={"name":"Category"},fields=["*"])
    for i in attributes:
        cat = frappe.get_doc('Item Attribute',i["name"])
        return cat.item_attribute_values
  

@frappe.whitelist()
def customer_fetch(email):
    customer_list = frappe.db.get_all('Customer',filters={"email":email},fields=["name"])
    return customer_list


