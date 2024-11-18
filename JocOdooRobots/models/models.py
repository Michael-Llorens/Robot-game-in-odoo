# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)

class player(models.Model):


     _name = 'res.partner'
     _inherit = 'res.partner'
     #_description = 'El joc'

     @api.depends('birth_date')
     def _compute_age(self):
         for rec in self:
             today = date.today()
             if rec.birth_date:
                 rec.age = today.year - rec.birth_date.year
             else:
                 rec.age = 0

     def _get_cash_default(self):
         cash = 1000
         _logger.warning('\030[94m'+str(cash)+'\033[0m')
         return cash

     #name = fields.Char(string="Nombre", required="true", help='Este es el nombre del jugador')
     enrollment_date = fields.Date(string="Fecha de alta")
     birth_date = fields.Date()
     age = fields.Integer(compute='_compute_age', store=True)
     description = fields.Text(string="Descripcion", help='Descripcion del jugador')
     is_player = fields.Boolean(string="Es un jugador")
     level = fields.Integer(string="Nivel", default=1)
     cash = fields.Integer(string="Dinero", default=1000)
     photo_player = fields.Image(string="Foto", max_width=200, max_height=200)
     photo_mini_player = fields.Image(related='photo_player', max_width=50, max_height=50)

     robots = fields.One2many(comodel_name="joc.robot", inverse_name="player",help='Al jugador que pertenece')

     @api.onchange('level')
     def _onchange_level(self):
         if self.level != 0:
             self.level = 0
             return {'warning' : {'title':'Error: Nivel','message': 'El nivel no se puede modificar'}}


     @api.onchange('level')
     def _onchange_level(self):
         if self.level > 99:
             self.level = 0

     @api.onchange('age')
     def _onchange_age(self):
         if self.age < 12:
             self.birth_date = '2012-01-01'

             return {'warning' : {'Edad':'Error: Edad','message': 'Tiene que tener mas de 12 años','type':'notification'}}


     def boton_fecha(self):
         self.enrollment_date = date.today();

     # def contar(self):
     #     p = 0;
     #     for s in self:
     #         if s.is_player:
     #             p = p + 1;
     #             return {'warning': {'jugadores': 'Cantidad: jugadores', 'message': 'Entre todos los seleccionados hay: '+p+' jugadores',
     #                                 'type': 'notification'}}

     def boton_new_player(self):
         for s in self:
             action = self.env.ref('joc.action_new_player').read()[0]
             return action

     # def boton_open_player(self):
     #     for s in self:
     #         action = self.env.ref('joc.action_new_player').read()[0]
     #         return action


     @api.model
     def update_level(self):
         players = self.search([])
         for p in players:
             if p.level >= 50:
                 p.level = 1;
             else:
                 p.level += 0;




class robot(models.Model):

     _name = 'joc.robot'
     _description = 'El robot'

     @api.depends('speed')
     def _compute_armor(self):
         for rec in self:
            if rec.speed == 0:
               rec.armor = 200;
            else:
                rec.armor = 200 - rec.speed;
            if rec.speed >= 200:
                rec.armor = 200;
                rec.speed = 0;

     @api.depends('speed')
     def _damage_total_robot(self):
         for r in self:
             r.damage_total = 0;
             for a in r.armas:
                 r.damage_total += a.damage_final;

     @api.constrains('speed')
     def _check_speed(self):
         for rec in self:
             if rec.speed < 200:
                 _logger.info('La velocidad es correcta, se puede guardar el robot')
             else:
                 rec.armor = 200;
                 rec.speed = 0;
                 raise ValidationError('La Velocidad no puede ser mayor o igual a 200 ya que no tendia Armadura')

     _sql_constraints = [('name_uniq', 'unique(name)', 'El nom del robot no se puede repetir')]

     name = fields.Char(string="Nombre", required=True, help='Este es el nombre del robot')
     description = fields.Text(string="Descripcion", help='Descripcion del robot')
     level = fields.Integer(string="Nivel")
     speed = fields.Integer(string="Velocidad", help='La velocidad del robot, cuanta mas velocidad menos armadura')
     armor = fields.Integer(string="Armadura", help='Armadura del robot', compute='_compute_armor')
     photo_robot = fields.Image(string="Foto", max_width=200, max_height=200)
     photo_mini_robot = fields.Image(related='photo_robot', max_width=50, max_height=50)
     unemployed =  fields.Boolean(string="Esta utilizado");
     damage_total = fields.Integer(string="Daño total", compute='_damage_total_robot')

     player = fields.Many2one(string='Player', comodel_name="res.partner", help='Los robots que tiene')

     armas = fields.Many2many(comodel_name="joc.arma", help='Las armas que contiene',
                              relation="armas_robots",
                              column1="robot_id",
                              column2="arma_id")


class arma(models.Model):

     _name = 'joc.arma'
     _description = 'La arma'

     @api.depends('damage')
     def _compute_dps(self):
         for rec in self:
            if rec.damage > 10:
                rec.dps = 1;
            else:
                if rec.damage > 5:
                    rec.dps = 2;
                else:
                    rec.dps = 3;

     @api.depends('dps')
     def _compute_damage_final(self):
         for rec in self:
             rec.damage_final = 2 * rec.dps + rec.damage;

     @api.depends('damage')
     def _compute_cash_arma(self):
        for rec in self:
            rec.cash_arma = rec.damage * 100;

     name = fields.Char(string="Nombre", required="true", help='Este es el nombre de la arma')
     description = fields.Text(string="Descripcion", help='Descripcion de la arma')
     level = fields.Integer(string="Nivel")
     cash_arma = fields.Integer(string="Precio del arma", compute="_compute_cash_arma")
     damage = fields.Integer(string="Daño Base", required="true", help='Daño base de la arma')
     damage_final = fields.Integer(string="Daño Final", help='Daño final de la arma', compute="_compute_damage_final")
     dps = fields.Integer(string="Segundos", compute="_compute_dps")
     photo_arma = fields.Image(string="Foto", max_width=200, max_height=200)
     photo_mini_arma = fields.Image(related='photo_arma', max_width=50, max_height=50)

     robots = fields.Many2many(comodel_name="joc.robot", help='Los robots que la utilizan',
                               relation="armas_robots",
                               column1="arma_id",
                               column2="robot_id")


class taller(models.Model):

    _name = 'joc.taller'
    _description = 'El taller'

    @api.depends('hours')
    def _compute_presupuesto(self):
        for rec in self:
            rec.presupuesto = rec.hours * 7;

    name = fields.Char(string="Nombre", required="true", help='Este es el nombre del taller');
    description = fields.Text(string="Descripcion", help='Descripcion del taller');
    date = fields.Datetime(string="Fecha inicial de reparacion");
    finish = fields.Datetime(string="Fecha fin de la reparacion");
    presupuesto = fields.Integer(string="Presupuesto", compute="_compute_presupuesto")
    hours = fields.Integer(string="Horas de reparacion");
    taller = fields.Many2one(string='Reparando', comodel_name="joc.robot", help='El robot que esta reparandose');
    photo_taller = fields.Image(string="Foto", max_width=200, max_height=200);
    photo_mini_arma = fields.Image(related='photo_taller', max_width=50, max_height=50);



    # La Batalla  --------------------------------------------------------------------------

class batalla(models.Model):

    _name = 'joc.batalla'
    _description = 'La Batalla'

    name = fields.Char(string="Nombre", required="true", help='Nombre de la batalla');
    description = fields.Text(string="Descripcion", help='Descripcion de la batalla');
    fecha_batalla = fields.Date(string="Fecha de la Batalla");
    attack = fields.Many2many('joc.robot', relation='robot_attacks', column1='b_a', column2='p_a',
                              domain="[('unemployed','=',False)]");
    defend = fields.Many2many('joc.robot', relation='robot_defends', column1='b_d', column2='p_d',
                              domain="[('unemployed','=',False)]");

    state = fields.Selection([('1', 'Creation'), ('2', 'Character Selection'), ('3', 'Waiting'), ('4', 'Finished')],
                             compute='_get_state')
    time_remaining = fields.Char(compute='_get_state')

    ganador = fields.Text(string="Ganador de la batalla", default="");

    def _get_date(self):
        date = datetime.now() + timedelta(minutes=5)
        return fields.Datetime.to_string(date)

    date = fields.Datetime(default=_get_date)
    finished = fields.Boolean()

    @api.model
    def _get_state(self):
        for b in self:
            b.state = '1'
        if len(b.attack) > 0 and len(b.defend) > 0:
            b.state = '2'
        if len(b.attack) > 0 and len(b.defend) > 0:
            b.state = '3'
        if b.finished == True:
            b.state = '4'
        start = datetime.now()
        end = fields.Datetime.from_string(b.date)
        relative = relativedelta(end, start)
        if end > start:
            b.time_remaining = str(relative.hours) + ":" + str(relative.minutes)
        else:
            b.time_remaining = '00:00'


    def boton_lucha(self):
        atake1 = 0;
        atake2 = 0;
        defensa1 = 0;
        defensa2 = 0;
        for r in self:
            for a in r.attack:
                # print(a.name);
                # print(a.damage_total);
                # print(a.armor);
                atake1 += a.damage_total;
                defensa1 += a.armor;

        for r in self:
            for a in r.defend:
                # print(a.name);
                # print(a.damage_total);
                # print(a.armor);
                atake2 += a.damage_total;
                defensa2 += a.armor;

        # print(str(atake1) +" VS " +str(atake2));
        # print(defensa1);
        # print(atake2);
        # print(defensa2);

        while True:
            if defensa1 == 0:
                if defensa2 == 0:
                    r.ganador = "No hay robots en ningun equipo para luchar";
                    break;

            if defensa1 == 0:
                r.ganador = "Falta elegir los robots del equipo 1";
                break;

            if defensa2 == 0:
                r.ganador = "Falta elegir los robots del equipo 2";
                break;

            if defensa1 == defensa1:
                if atake1 == atake2:
                    r.ganador = "Empate";
                    break;

            defensa1 -= atake2;
            defensa2 -= atake1;

            if defensa1 <= 0:
                r.ganador = "Equipo 2";
                for r in self:
                    for a in r.attack:
                        a.level += 1;
                break;
            if defensa2 <= 0:
                r.ganador = "Equipo 1";
                for r in self:
                    for a in r.attack:
                        a.level += 1;
                break;

        # print("++++/////////////////////");
        # print(defensa1);
        # print(defensa2);

        # return {'warning': {'Luchaa': 'Error: Lucha', 'message': 'Este es el mensaje de la lucha', 'type': 'notification'}}

    def boton_fecha(self):
        self.fecha_batalla = date.today();

    @api.onchange('ganador')
    def _onchange_level(self):
        self.ganador = ""
        return {'warning' : {'title':'Error: Ganador','message': 'No puedes modificar el ganador'}}