from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from datetime import datetime


class student_student(models.Model):
    _name = 'student.student'
    _rec_name = 'name'
    _description = 'Student Management Module For Learning'
    _order = 'name'
    _inherit = 'mail.thread'

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
    code = fields.Text(string="Code", required=False, copy=False)
    active = fields.Boolean(string='Active', default=True, )
    image = fields.Binary(string="Image", )
    sec_cert = fields.Binary(string="Upload your Secondary Certification", )
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
    dorf_id = fields.Many2one(comodel_name="dorf.information", string="Department of Faculty", required=False, )
    fac = fields.Char(related="dorf_id.name")
    tutfees = fields.Float(string="Tuition Fees", default='0.0', oldname='x', digits=(6, 2), readonly=True, )
    totfees = fields.Float(string="Total Fees", default='0.0', compute='_get_total_fees', store=True, )
    ref_link = fields.Char(string="External Link", required=False, )
    health_issues = fields.Selection(string="Health Issues Details", selection=[('yes', 'Yes'), ('no', 'No'), ],
                                     required=False, default='no', )
    templates = fields.Html(string="Template", )
    ref = fields.Reference(string='Reference',
                           selection=[('res.partner', 'partner'), ('res.user', 'user'),
                                      ('student.student', 'student',)])
    state = fields.Selection(string="Status", selection=STATE, default='draft', readonly=True, )

    @api.one
    @api.depends('tutfees', 'regfees')
    def _get_total_fees(self):
        self.totfees = self.regfees + self.tutfees

    @api.onchange('degree_id')
    def _get_degree_fees(self):
        if self.degree_id:
            self.tutfees = self.degree_id.degfees

    _sql_constraints = [('check_student_age', 'check(age>=18)', 'The age of the student must be at least 18 Year')]
    _sql_constraints = [('unique_student_code', 'unique(code)', 'The student code must be unique value')]


    # @api.constrains(health_notes)
    # def _check_no_characters(self):
    #     if self.health_notes:
    #         if len(self.health_notes) <= 25:
    #             raise ValidationError('Please Enter a detailed description')

    @api.multi
    def generate_seat_no(self):
        print('generate_seat_no button Work')

    @api.multi
    def test_x2many(self):
        print('test_x2many button Work')

    @api.model
    def create(self, vals_list):
        print(vals_list)
        rec = super(student_student, self).create(vals_list)
        print('result: ', rec)
        audit_log_data = {'user_id': self._uid,
                          'date': datetime.today(),
                          'student_info': str(self.ids)+' '+str(self.name)+' '+str(self.uni_no),
                          'status': 'create'}
        self.env['student.audit.log'].create(audit_log_data)
        return rec

    @api.multi
    def copy(self, default=None):
        res = super(student_student, self).copy()
        audit_log_data = {'user_id': self._uid,
                          'date': datetime.today(),
                          'student_info': str(self.ids)+' '+str(self.name)+' '+str(self.uni_no),
                          'status': 'copy'}
        self.env['student.audit.log'].create(audit_log_data)
        return res

    @api.multi
    def write(self, vals):
        print(vals)
        res = super(student_student, self).write(vals)
        audit_log_data = {'user_id': self._uid,
                          'date': datetime.today(),
                          'student_info': str(self.ids)+' '+str(self.name)+' '+str(self.uni_no),
                          'status': 'write'}
        self.env['student.audit.log'].create(audit_log_data)
        return res

    @api.multi
    def unlink(self):
        res = super(student_student, self).unlink()
        if self.state != 'draft':
            raise Warning("You are not allowed to delete this Record")
        audit_log_data = {'user_id': self._uid,
                          'date': datetime.today(),
                          'student_info': str(self.ids)+' '+str(self.name)+' '+str(self.uni_no),
                          'status': 'Delete'}
        self.env['student.audit.log'].create(audit_log_data)
        return res
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
    _rec_name = 'name'
    _description = 'A Registry of All departments of faculties'

    code = fields.Char()
    name = fields.Char()


###################################################################################
class dord_information(models.Model):
    _name = 'dord.information'
    _rec_name = 'name'
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
    degfees = fields.Float(string="Degree Fees",  required=False, )

    @api.multi
    @api.depends('name', 'dorf_id', 'dord_id')
    def name_get(self):
        for rec in self:
            rec.name = str(rec.name) + '/' + str(rec.dord_id.name)
        return super(degree_detail, self).name_get()
###################################################################################
class resPartner(models.Model):
    _inherit = 'res.partner'

    national_id = fields.Char(string="National ID", required=False, )
