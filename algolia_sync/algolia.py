from algoliasearch.search_client import SearchClient 
import frappe 
import json

client = SearchClient.create('NAH884LD6O','155ad86e58cb50ae7eefab00df3bc15d')
# index = client.init_index('zoomcartlive')
index = client.init_index('zoomcartDev')

# client = SearchClient.create('8AF7KWVKMG','ea7e8bb31e90edadcd63df48fc239f20')
# index = client.init_index('dev_item')



def send_algolia_item(doc,event):
    web = frappe.get_doc('Website Item',doc.name)
    items = frappe.get_doc('Item',web.item_code)

    attribute_list=[]
    value_list=[]
    price = frappe.get_doc('Item Price',items.name)
    rate= price.price_list_rate
    for i in items.attributes:
        attribute_list.append(i.attribute)
        value_list.append(i.attribute_value)
    featured = items.featured_item_
    image1 = items.website_image_1
    image2 = items.website_image_2
    image3 = items.website_image_3
    image4 = items.website_image_4
    url = items.website_url
    
    if web.published == 1:
        if items.has_variants == 0:
            records = {"item":items.item_name,"item_code":items.item_code,"Publish":items.published_in_website,"item_group":items.item_group,"Description":items.description,"Item_price":rate,"Image URL":[image1,image2,image3,image4],\
            attribute_list[0]:value_list[0],attribute_list[1]:value_list[1],attribute_list[2]:value_list[2], attribute_list[3]:value_list[3] ,"_tags":items.best_seller , "Featured":featured,"item_url":url}
            send = index.save_object(records,  {'autoGenerateObjectIDIfNotExist': True})
        
            for ids in send:
                obj_id = ids["objectIDs"]

                for algo_id in obj_id:
                    update = frappe.db.set_value('Website Item',doc.name,'algolia_id', algo_id )



def delete_object(doc,event):
    web_doc = frappe.get_doc('Website Item',doc.name)
    item_doc = frappe.get_doc('Item',web_doc.item_code)
    if item_doc.has_variants == 0:
        algolia_id = web_doc.algolia_id
        del_object = index.delete_object(algolia_id)



def update_object(doc,event):
    item_doc = frappe.get_doc('Item',doc.name)
    price = frappe.get_doc('Item Price',item_doc.name)
    rate= price.price_list_rate
    attribute_list=[]
    value_list=[]
    for i in item_doc.attributes:
        attribute_list.append(i.attribute)
        value_list.append(i.attribute_value) 
    
    item_name = item_doc.item_name
    item_code = item_doc.item_code
    item_group = item_doc.item_group
    featured = item_doc.featured_item_
    image1 = item_doc.website_image_1
    image2 = item_doc.website_image_2
    image3 = item_doc.website_image_3
    image4 = item_doc.website_image_4
    published = item_doc.published_in_website
    description = item_doc.description
    Bestseller = item_doc.best_seller
    url = item_doc.website_url


    if item_doc.has_variants == 0:
        web = frappe.db.get_all('Website Item',filters={"item_name":item_doc.item_name},fields={"published","algolia_id"})
        for pub in web:
            if pub["published"] == 1:
                update_object = index.partial_update_object({"objectID":pub["algolia_id"],"item":item_name,"item_code":item_code,"Published":published,"item_group":item_group,"Description":description,"item_price":rate,\
                "Image URL":[image1,image2,image3,image4],attribute_list[0]:value_list[0],attribute_list[1]:value_list[1],attribute_list[2]:value_list[2],attribute_list[3]:value_list[3],"_tags":Bestseller , "Featured":featured,"item_url":url},{'createIfNotExists':False})
    

  
def website_item(doc,event):
    web = frappe.get_doc('Website Item',doc.name)
    item_doc = frappe.get_doc('Item',web.item_code)
    
    algolia_id = web.algolia_id
    price = frappe.get_doc('Item Price',item_doc.name)
    rate = price.price_list_rate
    image1 = item_doc.website_image_1
    image2 = item_doc.website_image_2
    image3 = item_doc.website_image_3
    image4 = item_doc.website_image_4
    featured = item_doc.featured_item_
    Bestseller = item_doc.best_seller
    published = item_doc.published_in_website
    url = item_doc.website_url

    attribute_list=[]
    value_list=[]
    for i in item_doc.attributes:
        attribute_list.append(i.attribute)
        value_list.append(i.attribute_value)

    if item_doc.has_variants == 0:
        records = {"objectID":algolia_id,"item":item_doc.item_name,"item_code":item_doc.item_code,"Published":published,"item_group":item_doc.item_group,"Description":item_doc.description,"item_price":rate,\
        "Image URL":[image1,image2,image3,image4],attribute_list[0]:value_list[0],attribute_list[1]:value_list[1],attribute_list[2]:value_list[2],attribute_list[3]:value_list[3],"_tags":Bestseller,"Featured":featured,"item_url":url}
   
   
        if web.published == 0:
            del_object = index.delete_object(algolia_id)
        
        else:
            send = index.save_object(records)

    
def priceChange(doc,event):
       
    price = frappe.get_doc('Item Price',doc.name)
    item_doc = frappe.get_doc('Item',price.name)
    price = frappe.get_doc('Item Price',item_doc.name)
    rate = price.price_list_rate
    item_name = item_doc.item_name
    item_code = item_doc.item_code
    item_group = item_doc.item_group
    description = item_doc.description
    image1 = item_doc.website_image_1
    image2 = item_doc.website_image_2
    image3 = item_doc.website_image_3
    image4 = item_doc.website_image_4
    featured = item_doc.featured_item_
    Bestseller = item_doc.best_seller
    published = item_doc.published_in_website
    url = item_doc.website_url
    attribute_list=[]
    value_list=[]
    for i in item_doc.attributes:
        attribute_list.append(i.attribute)
        value_list.append(i.attribute_value)
    
    if item_doc.has_variants == 0:
        web = frappe.db.get_all('Website Item',filters={"item_name":item_doc.item_name},fields={"published","algolia_id"})
        for pub in web:
            if pub["published"] == 1:
                update_object = index.partial_update_object({"objectID":pub["algolia_id"],"item":item_name,"item_code":item_code,"Published":published,"item_group":item_group,"Description":description,"item_price":rate,\
                "Image URL":[image1,image2,image3,image4],attribute_list[0]:value_list[0],attribute_list[1]:value_list[1],attribute_list[2]:value_list[2],attribute_list[3]:value_list[3],"_tags":Bestseller , "Featured":featured,"item_url":url},{'createIfNotExists':False})




                