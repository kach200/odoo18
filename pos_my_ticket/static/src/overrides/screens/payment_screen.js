
import { patch } from '@web/core/utils/patch'
import { _t } from '@web/core/l10n/translation'
import { AlertDialog } from '@web/core/confirmation_dialog/confirmation_dialog'
import { PaymentScreen } from '@point_of_sale/app/screens/payment_screen/payment_screen'

patch(PaymentScreen.prototype, {

  async validateOrder(isForceValidate) {
    const order = this.currentOrder;

    if (!order) return false;

    // ✅ Validación correcta
    if (!order.get_partner()) {

      // 🔔 Mensaje
      this.env.services.dialog.add(AlertDialog, {
        title: _t('Cliente requerido'),
        body: _t('Debe seleccionar un cliente para continuar.')
      });

      return false; 
    }

    return await super.validateOrder(...arguments);
  },
  /**
   * Overrides `shouldDownloadInvoice` method to never downloading invoice.
   * @returns {boolean}
   */
  shouldDownloadInvoice () {
    return false
  },
  /**
   * Overrides `afterOrderValidation` method to query invoice and set the invoice in the order.
   */
  async afterOrderValidation () {
    const order = this.currentOrder

    // In auto-print mode, super.afterOrderValidation() triggers printing,
    // so invoice data must be loaded first to be available in the template.
    if (order?.is_to_invoice()) {
      const invoiceCandidate =
        order.raw?.account_move ||
        order.account_move ||
        order.finalized_invoice_id ||
        false

      let invoiceId = false
      if (Array.isArray(invoiceCandidate)) {
        invoiceId = invoiceCandidate[0]
      } else if (typeof invoiceCandidate === 'object' && invoiceCandidate !== null) {
        invoiceId = invoiceCandidate.id || false
      } else {
        invoiceId = invoiceCandidate
      }

      if (invoiceId) {
        try {
          const invoice = await this.invoiceService.getInvoice(invoiceId)
          if (invoice && invoice.length > 0) {
            order.set_invoice(invoice[0])
          } else {
            order.set_invoice({ id: invoiceId })
          }
        } catch {
          // Keep a minimal payload so the template can still render a fallback.
          order.set_invoice({ id: invoiceId })
        }
      }
    }

    await super.afterOrderValidation(...arguments)
  }

})
