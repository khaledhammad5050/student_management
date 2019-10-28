from odoo import models, fields, api
from odoo.exceptions import Warning


class student_student(models.Model):
    _name = 'student.student'
    _rec_name = 'name'
    _description = 'Student Management Module For Learning'
    _order = 'name'

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

    name = fields.Char(string='Name', help='full student name will be used on its ID card')
    code = fields.Text(string="Code", required=False, )
    active = fields.Boolean(string='Active', default=True, )
    image = fields.Binary(string="Image", )
    uni_no = fields.Char(string="Ministry University NO.", required=False, copy=False, )
    seat_no = fields.Char(string="Seat NO.", copy=False, )
    dob = fields.Date(string="Date Of Birth", required=True, )
    age = fields.Integer(string="Age", )
    fdate = fields.Date(string="First Registration Date", )
    ldate = fields.Datetime(string="Last Registration Date", )
    health_notes = fields.Text(string="Health issues Details", required=False, )
    gender = fields.Selection(string="Gender", selection=[('male', 'Male'), ('female', 'Female'), ],
                              default='male', )
    results_ids = fields.One2many(comodel_name="schoolresults.details", inverse_name="student_id",
                                  string="School Results", required=False, )
    hobbies_ids = fields.Many2many(comodel_name="hobbies.details", relation="student_hobbies_rel", column1="student_id",
                                   column2="hobbie_id", string="Student Hoppies", )
    responsible_id = fields.Many2one(comodel_name="res.partner", string="Responsible Person", required=False, )
    email = fields.Char(related='responsible_id.email', string="Email", required=False, )
    phone = fields.Char(related='responsible_id.phone', string="Phone", required=False, )
    degree_id = fields.Many2one(comodel_name="degree.detail", string="Degree to register for", required=False, )
    regfees = fields.Float(string="Registration Fees", default='0.0', )
    tutfees = fields.Float(string="Tuition Fees", default='0.0', oldname='x', digits=(6, 2), )
    totfees = fields.Float(string="Total Fees", default='0.0', compute='_get_total_fees', store=True, )
    ref_link = fields.Char(string="External Link", required=False, )
    health_issues = fields.Selection(string="Health Issues Details", selection=[('yes', 'Yes'), ('no', 'No'), ],
                                     required=False, default='no', )
    # template = fields.HTML(string="Template", )
    state = fields.Selection(string="Status", selection=STATE, default='draft', readonly=True, )

    @api.one
    @api.depends('tutfees', 'regfees')
    def _get_total_fees(self):
        self.totfees = self.regfees + self.tutfees

    _sql_constraints = [('check_student_age', 'check(age>=18)', 'The age of the student must be at least 18 Year')]
    _sql_constraints = [('unique_student_code', 'unique(code)', 'The student code must be unique value')]

    # @api.one
    # @api.constrains(health_notes)
    # def _check_no_characters(self):
    #     if len(self.health_notes) < 25:
    #         raise Warning('Please Enter a detailed description')

###################################################################################
class schoolresults_details(models.Model):
    _name = 'schoolresults.details'
    _rec_name = 'name'
    _description = 'students secondary school education results'

    name = fields.Char(string="Name", required=False, )
    student_id = fields.Many2one(comodel_name="student.student", string="Student", required=False, ondelete="cascade")
    subject_id = fields.Many2one(comodel_name="schoolresults.subject", string="Subject", required=False, )
    result = fields.Float(string="Result", required=False, )


###################################################################################
class schoolresults_subject(models.Model):
    _name = 'schoolresults.subject'
    _rec_name = 'name'
    _description = 'students secondary school subjects'

    name = fields.Char(string='Subject')


###################################################################################
class dorf_information(models.Model):
    _name = 'dorf.information'
    _rec_name = 'code'
    _description = 'A Registry of All departments of faculties'

    code = fields.Char()
    name = fields.Char()


###################################################################################
class dord_information(models.Model):
    _name = 'dord.information'
    _rec_name = 'code'
    _description = 'A Registry of All divisions of departments'

    code = fields.Char()
    name = fields.Char()
    dorf_id = fields.Many2one(comodel_name="dorf.information", string="Department of Faculty", required=False, )


###################################################################################
class hobbies_details(models.Model):
    _name = 'hobbies.details'
    _rec_name = 'name'
    _description = 'Student Hoppies'

    name = fields.Char(string='Name')


###################################################################################
class degree_detail(models.Model):
    _name = 'degree.detail'
    _rec_name = 'name'
    _description = 'All offered degrees offered by the university to students '

    name = fields.Char(string='Name')
    dorf_id = fields.Many2one(comodel_name="dorf.information", string="Department of Faculty", required=False, )
    dord_id = fields.Many2one(comodel_name="dord.information", string="Division of Department", required=False, )


###################################################################################
class resPartner(models.Model):
    _inherit = 'res.partner'

    national_id = fields.Char(string="National ID", required=False, )
