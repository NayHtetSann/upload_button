from odoo import models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _create_document_from_attachment(self, attachment_ids):
        """ Create the purchase orders from files."""

        attachments = self.env['ir.attachment'].browse(attachment_ids)
        if not attachments:
            raise UserError(_("No attachment was provided"))
        all_purchases = self.env['purchase.order']
        for attachment in attachments:
            purchase = self.env['purchase.order'].create({'partner_id': self.env.user.partner_id.id})
            all_purchases |= purchase
            purchase.message_post(attachment_ids=attachment.ids)
            attachment.write({'res_model': 'purchase.order', 'res_id': purchase.id})

        return all_purchases

    def create_document_from_attachment(self, attachment_ids):
        purchases = self._create_document_from_attachment(attachment_ids)
        action_vals = {
            'name': _('Generated Documents'),
            'domain': [('id', 'in', purchases.ids)],
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'context': self._context
        }
        if len(purchases) == 1:
            action_vals.update({
                'views': [[False, "form"]],
                'view_mode': 'form',
                'res_id': purchases[0].id,
            })
        else:
            action_vals.update({
                'views': [[False, "list"], [False, "kanban"], [False, "form"]],
                'view_mode': 'list, kanban, form',
            })
        return action_vals
