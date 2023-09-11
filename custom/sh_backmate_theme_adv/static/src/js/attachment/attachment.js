/* @odoo-module */
import { ListRenderer } from "@web/views/list/list_renderer";
import core from "web.core";
var _t = core._t;
import { patch } from "@web/core/utils/patch";
const { Component, useState, useRef, useExternalListener, onWillUpdateProps, onWillStart, onPatched } = owl;
import { useService } from "@web/core/utils/hooks";
import { ListController } from "@web/views/list/list_controller";
import { WebClientViewAttachmentViewContainer } from "@mail/components/web_client_view_attachment_view_container/web_client_view_attachment_view_container";
var shDocumentViewer = require("sh_attachment_in_tree_view.shDocumentViewer");

patch(ListRenderer.prototype, 'sh_attachment_in_tree_view/static/src/js/list_controller.js', {

    setup(){

        this.dialogService = useService("dialog");
        this.orm = useService("orm");
        this.notificationService = useService("notification");
        this.messaging = useService("messaging");

        onWillStart(async () => {
            
            const data = await this.orm.call('res.users', 'get_attachment_data', [this.props.list.resModel, this.props.list.records.map((rec)=>rec.resId)], {});

            this.sh_attachments = data[0]
            this.sh_show_attachment_in_list_view = data[1]
            
        });
        this._super()
        
    },

    _shloadattachmentviewer: function (ev) {

        let attachment_id = parseInt($(ev.currentTarget).data("id"));
        let record_id = parseInt($(ev.currentTarget).data("record_id"));
        let attachment_mimetype = $(ev.currentTarget).data("mimetype");
        let mimetype_match = attachment_mimetype.match("(image|application/pdf|text|video)");
        let attachment_name = $(ev.currentTarget).data("data-name");
        var attachment_data = this.sh_attachments[0];

      if (mimetype_match) {

        var sh_attachment_id = attachment_id;
        var sh_attachment_list = [];
          attachment_data[record_id].forEach((attachment) => {
              if (attachment.attachment_mimetype.match("(image|application/pdf|text|video)")) {
                  sh_attachment_list.push({
                      id: attachment.attachment_id,
                      filename: attachment.attachment_name,
                      name: attachment.attachment_name,
                      url: "/web/content/" + attachment.attachment_id + "?download=true",
                      type: attachment.attachment_mimetype,
                      mimetype: attachment.attachment_mimetype,
                      is_main: false,
                  });
              }
          });
        var sh_attachmentViewer = new shDocumentViewer(self,sh_attachment_list,sh_attachment_id);
        sh_attachmentViewer.appendTo($(".o_DialogManager"));

      }
      else{

        this.notificationService.add(this.env._t("Preview for this file type can not be shown"), {
            title: this.env._t("File Format Not Supported"),
            type: 'danger',
            sticky: false
        });
      }

    }
})

Object.assign(ListRenderer.components, {
    WebClientViewAttachmentViewContainer,
});
