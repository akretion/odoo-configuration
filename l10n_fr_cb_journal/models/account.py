# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models

class WizardMultiChartsAccounts(models.AbstractModel):
    _inherit = 'wizard.multi.charts.accounts'

    @api.model
    def _prepare_all_journals(self, chart_template_id, acc_template_ref, company_id):
        data = super(WizardMultiChartsAccounts, self)._prepare_all_journals(
           chart_template_id, acc_template_ref, company_id)
        debit_tmpl_acc = self.env.ref('l10n_fr_cb_journal.pcg_5115')
        credit_tmpl_acc = self.env.ref('l10n_fr_cb_journal.pcg_5115')
        data.append({
            'type': 'bank',
            'name': 'Paiement par carte Bancaire',
            'code': 'CB',
            'company_id': company_id,
            'centralisation': False,
            'analytic_journal_id': False,
            'default_credit_account_id': acc_template_ref[credit_tmpl_acc.id],
            'default_debit_account_id': acc_template_ref[debit_tmpl_acc.id],
        })
        return data
