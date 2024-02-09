from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'
    _order = "name desc"

    name = fields.Char('Name', required=True)
    # color = fields.Integer('Color Index')  # Opcional, para UI
    
    _sql_constraints = [
        ('tag_name_unique', 'UNIQUE(name)', 'The tag name must be unique.'),
    ]
