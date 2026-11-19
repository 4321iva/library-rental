from odoo import fields, models


class LibraryMember(models.Model):
    _name = "library.member"
    _description = "Library Member"
    _order = "name, id"

    name = fields.Char(string="Ім’я", required=True)
    membership_number = fields.Char(string="Номер читацького квитка", required=True)
    loan_ids = fields.One2many("library.loan", "member_id", string="Видачі")

    _membership_number_unique = models.Constraint(
        "UNIQUE(membership_number)", "Такий номер читацького квитка вже існує."
    )
