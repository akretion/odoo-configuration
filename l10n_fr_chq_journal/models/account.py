# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class WizardMultiChartsAccounts(models.AbstractModel):
    _inherit = 'wizard.multi.charts.accounts'

    @api.model
    def _prepare_all_journals(self, chart_template_id, acc_template_ref,
                              company_id):
        data = super(WizardMultiChartsAccounts, self)._prepare_all_journals(
            chart_template_id, acc_template_ref, company_id)
        debit_tmpl_acc = self.env.ref('l10n_fr_chq_journal.pcg_51121')
        credit_tmpl_acc = self.env.ref('l10n_fr_chq_journal.pcg_51123')
        data.append({
            'type': 'bank',
            'name': 'Paiement par Chèque',
            'code': 'CHQ',
            'company_id': company_id,
            'centralisation': False,
            'analytic_journal_id': False,
            'default_credit_account_id': acc_template_ref[credit_tmpl_acc.id],
            'default_debit_account_id': acc_template_ref[debit_tmpl_acc.id],
        })

        debit_tmpl_acc = self.env.ref('l10n_fr_chq_journal.pcg_51122')
        credit_tmpl_acc = self.env.ref('l10n_fr_chq_journal.pcg_51122')
        data.append({
            'type': 'bank',
            'name': 'Remise de Chèque',
            'code': 'RCHQ',
            'company_id': company_id,
            'centralisation': False,
            'analytic_journal_id': False,
            'default_credit_account_id': acc_template_ref[credit_tmpl_acc.id],
            'default_debit_account_id': acc_template_ref[debit_tmpl_acc.id],
        })
        return data


class AccountTemplate(models.Model):
    _inherit = 'account.account.template'

    @api.model
    def generate_account(self, chart_template_id, tax_template_ref,
                         acc_template_ref, code_digits, company_id):
        acc_tmpl_ref = super(AccountTemplate, self).generate_account(
            chart_template_id, tax_template_ref, acc_template_ref,
            code_digits, company_id)
        company = self.env['res.company'].browse(company_id)
        check_account = self.env.ref('l10n_fr_chq_journal.pcg_51122')
        if acc_tmpl_ref.get(check_account.id):
            company.write({
                'check_deposit_account_id': acc_tmpl_ref[check_account.id],
                })
        return acc_tmpl_ref
