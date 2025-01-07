from odoo import models, fields, api

class RopalmiSale(models.Model):
    _name = "ropalmi.sale"
    _description = "Venta de ropa"

    name = fields.Char("Referencia", required=True, readonly=True, default="New")
    date = fields.Date("Fecha", default=fields.Date.today)
    customer = fields.Many2one("res.partner", string="Cliente", required=True)
    sale_lines = fields.One2many("ropalmi.sale.line", "sale_id", string="Líneas de venta")
    total = fields.Float("Total", compute="_compute_total")
    state = fields.Selection([
        ("draft", "Borrador"),
        ("confirmed", "Confirmada"),
        ("done", "Realizada"),
        ("cancelled", "Cancelada")
    ], string="Estado", default="draft")

    def action_confirm(self):
        for rec in self:
            rec.state = "confirmed"

    def action_done(self):
        for rec in self:
            rec.state = "done"

    def action_cancel(self):
        for rec in self:
            rec.state = "cancelled"

    @api.model
    def create(self, vals):
        if vals.get("name", "New") == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("ropalmi.sale") or "New"
        return super(RopalmiSale, self).create(vals)

    @api.depends("sale_lines.subtotal")
    def _compute_total(self):
        for sale in self:
            sale.total = sum(line.subtotal for line in sale.sale_lines)

class RopalmiSaleLine(models.Model):
    _name = "ropalmi.sale.line"
    _description = "Línea de venta"

    sale_id = fields.Many2one("ropalmi.sale", string="Venta")
    product_id = fields.Many2one("ropalmi.product", string="Producto", required=True)
    quantity = fields.Integer("Cantidad", default=1)
    price = fields.Float("Precio", related="product_id.price")
    subtotal = fields.Float("Subtotal", compute="_compute_subtotal")

    @api.depends("quantity", "price")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price
