from odoo import fields, models


class LibraryLoan(models.Model):
    _name = "library.loan"
    _description = "Library Loan"
    _rec_name = "copy_id"
    _order = "loan_date desc, id desc"

    copy_id = fields.Many2one(
        "library.copy", string="Примірник", required=True, ondelete="restrict"
    )
    member_id = fields.Many2one(
        "library.member", string="Читач", required=True, ondelete="restrict"
    )
    book_name = fields.Char(related="copy_id.book_id.name", string="Книга")
    book_author = fields.Char(related="copy_id.book_id.author", string="Автор")
    member_number = fields.Char(
        related="member_id.membership_number", string="Номер читацького квитка"
    )
    loan_date = fields.Date(
        string="Дата видачі", required=True, default=fields.Date.context_today
    )
    due_date = fields.Date(string="Повернути до", required=True)
    return_date = fields.Date(string="Фактична дата повернення")
    state = fields.Selection(
        [("active", "Активна"), ("returned", "Повернено")],
        string="Статус",
        required=True,
        default="active",
    )
