from odoo import api, fields, models
from datetime import date

class wiz_calc_age(models.TransientModel):
    _name = 'wiz.calc.age'
    _description = 'New Description'

    from_date = fields.Date(string="From Date", required=True, )
    to_date = fields.Date(string="To Date", required=True, )

    @api.multi
    def calc_age(self):
        student_obj = self.env['student.student']
        for rec in self:
            students = student_obj.search([('dob', '>=', rec.from_date), ('dob', '<=', rec.to_date)])

            for student in students:
                if student.dob:
                    today = date.today()
                    age = today.year - student.dob.year - (
                                (today.month, today.day) < (student.dob.month, student.dob.day))
                    print(age)
                    student.age = age

                    return True
