from odoo import fields, models


class student_audit_log(models.Model):
    _name = 'student.audit.log'
    _rec_name = 'name'
    _description = 'New Description'

    name = fields.Char()
    user_id = fields.Integer(string="User ID", required=False, )
    date = fields.Datetime(string="Date", required=False, )
    student_info = fields.Char(string="Student Inf", required=False, )
    status = fields.Selection(string="", selection=[('create', 'Created'), ('write', 'Updated'), ('delete', 'Deleted'),
                                                    ('copy', 'Copied'), ], required=False, )
