
from algoliasearch.search_client import SearchClient #type:ignore
import frappe 
import json
import itertools

client = SearchClient.create('1YNAN4KMZC', 'd71f17dac615797748f874a5efaef664')
index = client.init_index('dev_item')

def send_algolia(doc,event):
    items = frappe.get_doc('Item', doc.name)
    for i in items.attributes:
        atribute = i.attribute
        value = i.attribute_value
    records = {"item":items.item_name,"item_code":items.item_code,"item_group":items.item_group,"imageURL":items.website_image,"attribute":atribute,"value":value }
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
    attribute_list=[]
    value_list=[]
    algolia_list=[]
    for i in item_doc.attributes:
        attribute_list.append(i.attribute)
        value_list.append(i.attribute_value)

    # name = s.join(attribute_list)
    # value = '\n'.join(value_list)
    # frappe.throw(attribute_list[1])
    # for i in range(len(attribute_list)):
    #     name = attribute_list[i]
    #     frappe.throw(name)
    # for i in range(len(value_list)):
    #     value=value_list[i]
    # frappe.throw(value)
    # frappe.throw(attribute_list)
    # frappe.throw(value_list)
        # attri = frappe.db.get_all("Item Variant Attribute",fields=["attribute","attribute_value","parent"],filters={"parent":["in",'attributes']})
        # if i.attribute_value:
        #     for j in i.attribute:
        #         var_list.append(j)
        #         frappe.throw(var_list)


    # frappe.throw(attri)
    # attri = json.dump(item_doc.attributes)
    # for i in item_doc.attributes:
       
        # for j in i:
        #     frappe.throw(j.attribute)
            # atribute = j.attribute
            # value = j.attribute_value
    
    # frappe.throw(frappe.as_json(item_doc.attributes))
        # for j in attri:
        #     frappe.throw(j.attribute_name)
        #
    # for i in item_doc.attributes: 
    #     atribute = i.attribute
    #     value = i.attribute_value
         
    #     frappe.throw(atribute, +str(i))


    # for j in item_doc.attributes:
    #     color =j.attribute
    #     val = j.attribute_value
            # frappe.throw(j)
    # while (item_doc.attributes):
        # color = i.attribute
        # name = i.attribute_value
    # frappe.throw(frappe.as_json(item_doc.attributes))
    
    algolia_id = item_doc.algolia_id
    item_name = item_doc.item_name
    item_code = item_doc.item_code
    item_group = item_doc.item_group
    image1 = item_doc.website_image
    image2 = item_doc.website_image_2
    image3 = item_doc.website_image_3
    update_object = index.partial_update_object({"objectID":algolia_id,"item":item_name,"item_code":item_code,"item_group":item_group,"imageURL":[image1,image2,image3],attribute_list[0]:value_list[0],attribute_list[1]:value_list[1]},{'createIfNotExists':False})
    
def show_website(doc,event):
    item_doc = frappe.get_doc('Item',doc.name)
    algolia_id = item_doc.algolia_id
    image2 = item_doc.website_image_2
    image3 = item_doc.website_image_3
    attribute_list=[]
    value_list=[]
    algolia_list=[]
    for i in item_doc.attributes:
        attribute_list.append(i.attribute)
        value_list.append(i.attribute_value)
    # name = '\n'.join(attribute_list)
    # value = '\n'.join(value_list)
    # algolia_list = attribute_list + value_list
    
    records = {"objectID":algolia_id,"item":item_doc.item_name,"item_code":item_doc.item_code,"item_group":item_doc.item_group,"imageURL":[item_doc.website_image,image2,image3],attribute_list[0]:value_list[0],attribute_list[1]:value_list[1]}
    if item_doc.show_in_website == 1 or item_doc.show_variant_in_website == 1:
        send = index.save_object(records)
    else:
        del_object = index.delete_object(algolia_id)

