from odoo import models, fields, api

class RopalmiPurchase(models.Model):
   _name = "ropalmi.purchase"
   _description = "Compra de ropa"

   name = fields.Char("Referencia", required=True, readonly=True, default="New")
   date = fields.Date("Fecha", default=fields.Date.today)
   supplier = fields.Many2one("res.partner", string="Proveedor", required=True)
   purchase_lines = fields.One2many("ropalmi.purchase.line", "purchase_id", string="Líneas de compra")
   total = fields.Float("Total", compute="_compute_total")
   state = fields.Selection([
       ("draft", "Borrador"),
       ("confirmed", "Confirmada"),
       ("received", "Recibida"),
       ("cancelled", "Cancelada")
   ], string="Estado", default="draft")

   @api.model
   def create(self, vals):
       if vals.get("name", "New") == "New":
           vals["name"] = self.env["ir.sequence"].next_by_code("ropalmi.purchase") or "New"
       return super(RopalmiPurchase, self).create(vals)

   @api.depends("purchase_lines.subtotal")
   def _compute_total(self):
       for purchase in self:
           purchase.total = sum(line.subtotal for line in purchase.purchase_lines)

class RopalmiPurchaseLine(models.Model):
   _name = "ropalmi.purchase.line"
   _description = "Línea de compra"

   purchase_id = fields.Many2one("ropalmi.purchase", string="Compra")
   product_id = fields.Many2one("ropalmi.product", string="Producto", required=True)
   quantity = fields.Integer("Cantidad", default=1)
   price = fields.Float("Precio")
   subtotal = fields.Float("Subtotal", compute="_compute_subtotal")

   @api.depends("quantity", "price")
   def _compute_subtotal(self):
       for line in self:
           line.subtotal = line.quantity * line.price
