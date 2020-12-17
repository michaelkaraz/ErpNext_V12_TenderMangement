# -*- coding: utf-8 -*-
# Copyright (c) 2020, Michael Karamanolis and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class BillOfMaterial(Document):
    def validate(self):
        calc(self)

    @frappe.whitelist()
    def reCalc(self):
        calc(self)


def calc(self):
    total = float(0)
    for d in self.get('labour_resource_cost'):
        lc = frappe.get_doc('Labour Resource', d.labour_resource)
        d.cost = float(lc.rate) * float(d.qty)
        total += d.cost
    for m in self.get('material_resource_cost'):
        mr = frappe.get_doc('Material Resource', m.material_resource)
        m.cost = float(mr.rate) * float(m.qty)
        total += m.cost
    for s in self.get('sub_contractor_cost'):
        sc = frappe.get_doc('Sub Contractor Management',
                            s.sub_contractor_management)
        s.cost = float(sc.rate) * float(s.qty)
        total += s.cost
    for e in self.get('equipment_management_cost'):
        em = frappe.get_doc('Equipment Management', e.equipment_management)
        e.cost = float(em.rate) * float(e.qty)
        total += e.cost
    self.total_cost = total
