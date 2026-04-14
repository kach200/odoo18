/**
 * Author: Jorge Luis
 * Email: jorgeluis@resolvedor.dev
 * Website: https://joguenco.dev
 */
import { patch } from '@web/core/utils/patch'
import { PosStore } from '@point_of_sale/app/store/pos_store'
// import { OrderReceipt } from '@point_of_sale/app/screens/receipt_screen/receipt/order_receipt'

patch(PosStore.prototype, {
  /**
   * Normalize account_move variants to a single invoice id.
   * @param {*} invoiceCandidate
   * @returns {number|false}
   */
  _extractInvoiceId(invoiceCandidate) {
    if (!invoiceCandidate) {
      return false
    }

    if (Array.isArray(invoiceCandidate)) {
      return invoiceCandidate[0] || false
    }

    if (typeof invoiceCandidate === 'object') {
      return invoiceCandidate.id || false
    }

    return invoiceCandidate
  },

  _extractSessionId(sessionCandidate) {
    if (!sessionCandidate) {
      return false
    }

    if (Array.isArray(sessionCandidate)) {
      return sessionCandidate[0] || false
    }

    if (typeof sessionCandidate === 'object') {
      return sessionCandidate.id || false
    }

    return typeof sessionCandidate === 'number' ? sessionCandidate : false
  },

  _extractSessionName(sessionCandidate) {
    if (!sessionCandidate) {
      return ''
    }

    if (Array.isArray(sessionCandidate)) {
      return sessionCandidate[1] || ''
    }

    if (typeof sessionCandidate === 'object') {
      return sessionCandidate.name || sessionCandidate.display_name || ''
    }

    return typeof sessionCandidate === 'string' ? sessionCandidate : ''
  },

  /**
   * Load invoice details required by receipt template before printing/reprinting.
   * @param {*} order
   */
  async _ensureInvoiceDataForReceipt(order) {
    if (!order?.is_to_invoice?.() || !order?.set_invoice) {
      return
    }

    const currentInvoice = order.get_invoice?.()
    if (currentInvoice?.name && currentInvoice?.invoice_date) {
      return
    }

    const invoiceId = this._extractInvoiceId(
      currentInvoice || order.raw?.account_move || order.account_move || order.finalized_invoice_id
    )

    if (!invoiceId) {
      return
    }

    try {
      const invoices = await this.data.searchRead(
        'account.move',
        [['id', '=', invoiceId]],
        ['id', 'name', 'display_name', 'invoice_date']
      )

      if (invoices?.length) {
        order.set_invoice(invoices[0])
      } else {
        order.set_invoice({ id: invoiceId })
      }
    } catch {
      order.set_invoice({ id: invoiceId })
    }
  },

  async _ensureSessionNameForReceipt(order) {
    const sessionCandidate =
      order?.raw?.session_id ||
      order?.session_id ||
      this.session ||
      false

    const currentName = this._extractSessionName(sessionCandidate)
    if (currentName) {
      this._receiptSessionName = currentName
      return
    }

    const sessionId = this._extractSessionId(sessionCandidate) || this.session?.id || false
    if (!sessionId) {
      return
    }

    try {
      const sessions = await this.data.searchRead(
        'pos.session',
        [['id', '=', sessionId]],
        ['name']
      )
      this._receiptSessionName = sessions?.[0]?.name || ''
    } catch {
      this._receiptSessionName = ''
    }
  },

  /**
   * Override `getReceiptHeaderData` method to add the invoice to the header.
   * @param {*} order
   * @returns
   */
  getReceiptHeaderData(order) {
    const result = super.getReceiptHeaderData(...arguments)
    const safeOrder = order || this.get_order?.()

    const sessionCandidate =
      safeOrder?.raw?.session_id ||
      safeOrder?.session_id ||
      this.session?.name ||
      false

    const sessionName = this._extractSessionName(sessionCandidate) || this._receiptSessionName || ''

    const configCandidate =
      safeOrder?.raw?.config_id ||
      safeOrder?.config_id ||
      this.config ||
      false

    let posConfigName = ''
    if (Array.isArray(configCandidate)) {
      posConfigName = configCandidate[1] || ''
    } else if (typeof configCandidate === 'object' && configCandidate !== null) {
      posConfigName = configCandidate.name || configCandidate.display_name || ''
    } else if (typeof configCandidate === 'string') {
      posConfigName = configCandidate
    }

    if (safeOrder?.get_invoice) {
      result.invoice_id = safeOrder.get_invoice()
    }

    // Ensure pos_name is available for the header (print + reprint + fallback calls)
    result.pos_name =
      safeOrder?.name ||
      safeOrder?.pos_reference ||
      safeOrder?.uid ||
      result.pos_name ||
      ''

    // Fallback: if config name is unavailable, derive it from order reference (e.g. Tienda1/0013).
    const derivedPosConfigName = result.pos_name.includes('/')
      ? result.pos_name.split('/')[0]
      : ''

    result.pos_session_name = sessionName
    result.pos_config_name = posConfigName || derivedPosConfigName

    return result
  },

  async printReceipt() {
    const targetOrder = arguments[0]?.order || this.get_order?.()
    await this._ensureInvoiceDataForReceipt(targetOrder)
    await this._ensureSessionNameForReceipt(targetOrder)
    return await super.printReceipt(...arguments)
  }
  
})

