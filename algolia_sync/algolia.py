from algoliasearch.search_client import SearchClient 
import frappe 
import json

client = SearchClient.create('8AF7KWVKMG','ea7e8bb31e90edadcd63df48fc239f20')
index = client.init_index('dev_item')

def send_algolia(doc,event):
    items = frappe.get_doc('Item', doc.name)
    attribute_list=[]
    value_list=[]
    price = frappe.get_doc('Item Price',items.name)
    rate= price.price_list_rate
    for i in items.attributes:
        attribute_list.append(i.attribute)
        value_list.append(i.attribute_value)
    image2 = items.website_image_2
    image3 = items.website_image_3
    image4 = items.website_image_4
    date = items.creation

    if items.has_variants == 0:
        records = {"item":items.item_name,"item_code":items.item_code,"item_group":items.item_group,"Description":items.description,"Item_price":rate,"Image URL":[items.image,image2,image3,image4],"Date":date,attribute_list[0]:value_list[0],attribute_list[1]:value_list[1],attribute_list[2]:value_list[2],"_tags":items.best_seller}
        send = index.save_object(records,  {'autoGenerateObjectIDIfNotExist': True})
    
        for ids in send:

            obj_id = ids["objectIDs"]
            update = frappe.db.set_value('Item',doc.name,'algolia_id', obj_id)
        

def delete_object(doc,event):
    item_doc = frappe.get_doc('Item',doc.name)
    algolia_id = item_doc.algolia_id
    del_object = index.delete_object(algolia_id)

def update_object(doc,event):
    item_doc = frappe.get_doc('Item',doc.name)
    price = frappe.get_doc('Item Price',item_doc.name)
    rate= price.price_list_rate
    date = item_doc.creation
    attribute_list=[]
    value_list=[]
    for i in item_doc.attributes:
        attribute_list.append(i.attribute)
        value_list.append(i.attribute_value) 
    
    algolia_id = item_doc.algolia_id
    item_name = item_doc.item_name
    item_code = item_doc.item_code
    item_group = item_doc.item_group
    image2 = item_doc.website_image_2
    image3 = item_doc.website_image_3
    image4 = item_doc.website_image_4
    description = item_doc.description
    Bestseller = item_doc.best_seller

    if item_doc.has_variants == 0:
        update_object = index.partial_update_object({"objectID":algolia_id,"item":item_name,"item_code":item_code,"item_group":item_group,"Description":description,"item_price":rate,"Image URL":[item_doc.image,image2,image3,image4],"Date":date,attribute_list[0]:value_list[0],attribute_list[1]:value_list[1],attribute_list[2]:value_list[2],"_tags":Bestseller},{'createIfNotExists':False})
    
def show_website(doc,event):
    item_doc = frappe.get_doc('Item',doc.name)
    price = frappe.get_doc('Item Price',item_doc.name)
    rate= price.price_list_rate
    algolia_id = item_doc.algolia_id
    image2 = item_doc.website_image_2
    image3 = item_doc.website_image_3
    image4 = item_doc.website_image_4
    date = item_doc.creation
    Bestseller = item_doc.best_seller
    attribute_list=[]
    value_list=[]
    for i in item_doc.attributes:
        attribute_list.append(i.attribute)
        value_list.append(i.attribute_value)
    if item_doc.has_variants == 0:
        records = {"objectID":algolia_id,"item":item_doc.item_name,"item_code":item_doc.item_code,"item_group":item_doc.item_group,"Description":item_doc.description,"item_price":rate,"Image URL":[item_doc.image,image2,image3,image4],"Date":date,attribute_list[0]:value_list[0],attribute_list[1]:value_list[1],attribute_list[2]:value_list[2],"_tags":Bestseller}
        send = index.save_object(records)
  

def website_item(doc,event):
    web = frappe.get_doc('Website Item',doc.name)
    item_doc = frappe.get_doc('Item',web.item_code)
    
    algolia_id = item_doc.algolia_id
    price = frappe.get_doc('Item Price',item_doc.name)
    rate = price.price_list_rate
    image2 = item_doc.website_image_2
    image3 = item_doc.website_image_3
    image4 = item_doc.website_image_4
    date = item_doc.creation
    Bestseller = item_doc.best_seller
    attribute_list=[]
    value_list=[]
    for i in item_doc.attributes:
        attribute_list.append(i.attribute)
        value_list.append(i.attribute_value)

    if item_doc.has_variants == 0:
        records = {"objectID":algolia_id,"item":item_doc.item_name,"item_code":item_doc.item_code,"item_group":item_doc.item_group,"Description":item_doc.description,"item_price":rate,"Image URL":[item_doc.image,image2,image3,image4],"Date":date,attribute_list[0]:value_list[0],attribute_list[1]:value_list[1],attribute_list[2]:value_list[2],"_tags":Bestseller}
   
   
        if web.published == 0:
            del_object = index.delete_object(algolia_id)
        
        else:
            send = index.save_object(records)


