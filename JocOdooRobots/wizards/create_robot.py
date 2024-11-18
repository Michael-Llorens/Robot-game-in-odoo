# -*- coding: utf-8 -*-

from odoo import models, fields, api

class createrobot(models.TransientModel):

    _name = 'joc.createrobot'
    name = fields.Char(string='Robot')
    description = fields.Text(string='Descripción')

    def crear_robot(self):
        self.env['joc.robot'].create({
            'name': self.name,
            'description': self.description,
        })