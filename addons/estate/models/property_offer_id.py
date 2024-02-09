from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        string='Status'
    )
    partner_id = fields.Many2one('res.partner', string="Partner")
    property_id = fields.Many2one('estate.property', string="Property")

    def action_accept_offer(self):
        for offer in self:
            # Establecer la oferta como aceptada
            offer.status = 'accepted'
            # Actualizar la propiedad relacionada
            property = offer.property_id
            property.write({
                'buyer_id': offer.partner_id.id,
                'selling_price': offer.price,
                # Asegúrate de actualizar el estado de la propiedad si es necesario
            })
            # Rechazar todas las demás ofertas para esta propiedad
            other_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', property.id),
                ('id', '!=', offer.id)
            ])
            other_offers.write({'status': 'refused'})
        return True

    def action_refuse_offer(self):
        self.write({'status': 'refused'})
        return True
    
    _sql_constraints = [
        ('offer_price_positive', 'CHECK(price > 0)', 'The offer price must be strictly positive.'),
    ]