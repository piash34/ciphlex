/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";

patch(ListController.prototype, "sh_sale_product_profit", {
  /**
   * @override
   */

  setup() {
    this._super();
    this.action = useService("action");
    this.is_sale_profit_mode = false;
    if (this["model"]) {
      if (this["model"]["rootParams"]) {
        if (this["model"]["rootParams"]["resModel"]) {
          if (this["model"]["rootParams"]["resModel"]) {
            if (
              this["model"]["rootParams"]["resModel"] ===
              "sh.sale.product.profit"
            ) {
              this.is_sale_profit_mode = true;
            }
          }
        }
      }
    }
  },

  async onDirectExportData(e) {
    if (this.is_sale_profit_mode == true) {
      this.action.doAction({
        type: "ir.actions.act_window",
        name: "Sales Product Profit",
        target: "new",
        res_id: e.id,
        res_model: "sh.sale.product.profit.wizard",
        views: [[false, "form"]],
      });
    } else {
      this._super();
    }
  },
});
