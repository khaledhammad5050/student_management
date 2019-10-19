# -*- coding: utf-8 -*-

from odoo import models, fields


class student_student(models.Model):
    _name = 'student.student'
    _rec_name = 'name'
    _description = 'Student Management Module For Learning'

    # Global Variables
    STATE = [('draft', 'Draft'),
             ('med_interview', 'Medical Interview'),
             ('acad_interview', 'Academic Interview'),
             ('first_register', 'First Register'),
             ('second_register', 'Second Registered'),
             ('third_register', 'Third Registered'),
             ('fourth_register', 'Fourth Registered'),
             ('dismiss', 'Dismissed'),
             ('alumni', 'Alumni')]

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True, )
    image = fields.Binary(string="Image", )
    uni_no = fields.Char(string="Ministry University NO.", required=True, copy=False, )
    seat_no = fields.Char(string="Seat NO.", copy=False)
    dob = fields.Date(string="Date Of Birth", required=True, )
    age = fields.Integer(string="Age", )
    fdate = fields.Date(string="First Registration Date", )
    ldate = fields.Datetime(string="Last Registration Date", )
    gender = fields.Selection(string="Gender", selection=[('male', 'Male'), ('female', 'Female'), ],
                              default='male', )
    regfees = fields.Float(string="Registration Fees", default='0.0', )
    tutfees = fields.Float(string="Tuition Fees", default='0.0', )
    totfees = fields.Float(string="Total Fees", default='0.0', )
    ref_link = fields.Char(string="External Link", required=False, )
    health_issues = fields.Selection(string="Health Issues Details", selection=[('yes', 'Yes'), ('no', 'No'), ],
                                     required=False, default='no', )
    template = fields.HTML(string="Template", )
    state = fields.Selection(string="Status", selection=STATE, default='draft', readonly=True, )
