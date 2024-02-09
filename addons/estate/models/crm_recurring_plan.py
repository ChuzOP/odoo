from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.today() + timedelta(days=90), copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
        help="The orientation of the garden",
    )
    status = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="new",
    )

    active = fields.Boolean("Active", default=True)

    buyer_id = fields.Many2one("res.partner", string="Buyer")
    seller_id = fields.Many2one("res.partner", string="Seller")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Float(compute="_compute_total_area", string="Total Area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_offer = fields.Float(
        compute="_compute_best_offer",
        inverse="_inverse_best_offer",
        string="Best Offer",
    )

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            best_offer_price = 0
            for offer in record.offer_ids:
                if offer.price > best_offer_price:
                    best_offer_price = offer.price
            record.best_offer = best_offer_price

    def _inverse_best_offer(self):
        for record in self:
            # Solo crear una nueva oferta si el mejor precio ingresado es más alto que cualquier oferta existente
            if record.best_offer > max(record.offer_ids.mapped("price"), default=0):
                self.env["estate.property.offer"].create(
                    {
                        "price": record.best_offer,
                        "property_id": record.id,
                        # Aquí puedes agregar más campos necesarios para la creación de la oferta, como 'partner_id' si es requerido.
                    }
                )
    
    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = False
                
    def action_cancel(self):
        for record in self:
            if record.status == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            record.status = 'cancelled'
        return True

    def action_sold(self):
        for record in self:
            if record.status == 'cancelled':
                raise UserError("Cancelled properties cannot be sold.")
            record.status = 'sold'
        return True
    
    _sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('selling_price_positive', 'CHECK(selling_price >= 0)', 'The selling price must be positive.'),
    ]
    
    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < record.expected_price * 0.9:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")