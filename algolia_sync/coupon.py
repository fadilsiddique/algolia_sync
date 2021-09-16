# import frappe


# from frappe import throw, _


# @frappe.whitelist(allow_guest=True)

# def apply_coupon_code(coupon_apply):

#     if not coupon_apply:
#         frappe.throw(_("Please enter a coupon code"))

#     coupon_list = frappe.get_all('Coupon Code', filters={'coupon_code': coupon_apply})
#     if not coupon_list:
#         frappe.throw(_("Please enter a valid coupon code"))

#     coupon_name = coupon_list[0].name
#     from erpnext.accounts.doctype.pricing_rule.utils import validate_coupon_code
#     from erpnext.shopping_cart.cart import get_cart_quotation

#     validate_coupon_code(coupon_name)
#     quotation=get_cart_quotation()
#     quotation.coupon_code = coupon_name
#     quotation.flags.ignore_permissions = True
#     quotation.save()

#     return quotation


    



    

