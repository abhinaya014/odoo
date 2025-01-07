from odoo import models, fields

class RopalmiProduct(models.Model):
    _name = "ropalmi.product"
    _description = "Producto de ropa"

    name = fields.Char("Nombre", required=True)
    reference = fields.Char("Referencia")
    category = fields.Selection([
        ("shirts", "Camisetas"),
        ("pants", "Pantalones"),
        ("dresses", "Vestidos"),
        ("accessories", "Accesorios")
    ], string="Categoría")
    size = fields.Selection([
        ("XS", "XS"),
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL")
    ], string="Talla")
    color = fields.Char("Color")
    price = fields.Float("Precio")
    stock = fields.Integer("Stock")
    image = fields.Binary("Imagen")
