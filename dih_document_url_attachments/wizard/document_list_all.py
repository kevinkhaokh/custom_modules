# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import fields, orm
try:
    # Python 3
    from urllib import parse as urlparse
except:
    from urlparse import urlparse

from openerp.api import Environment


class DummyListAll(orm.TransientModel):

    _name = 'ir.attachment.dummy.list.all'

    def action_list_all(self, cr, uid, ids, context=None):
        proxy = self.pool.get('ir.attachment')
        valid_attachment_ids = proxy.search(cr, uid, [('res_id', '=', context['active_id'])], context=context)
        #viewid = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'dih_document_url_attachments', 'document.view_document_file_tree')[1] 
        aEnv = Environment(cr,uid,context)

        viewid = aEnv.ref('document.view_document_file_tree', False).id
        view = {
            'views': [(viewid,'tree'), (False,'form')], #get the external ID, you can't guess this one.
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'domain':"[('id', 'in',%s)]" %(valid_attachment_ids),
            'target': 'current',
            'flags': {'action_buttons': False},
        }
        
        return view