from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "name desc"

    name = fields.Char(required=True)
    description = fields.Text()
    
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    _sql_constraints = [
        ('type_name_unique', 'UNIQUE(name)', 'The property type name must be unique.'),
    ]