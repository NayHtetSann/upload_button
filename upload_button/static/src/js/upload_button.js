/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ListController } from "@web/views/list/list_controller";
import { PurchaseDashBoard } from "@purchase/views/purchase_dashboard";
import { PurchaseDashBoardRenderer } from "@purchase/views/purchase_listview";
import { FileUploader } from "@web/views/fields/file_handler";
import { listView } from "@web/views/list/list_view";
import { useService } from "@web/core/utils/hooks";

export class PurchaseListController extends ListController {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.attachmentIdsToProcess = [];
        this.extraContext = {};
    }

    async onFileUploaded(file) {
        const att_data = {
            name: file.name,
            mimetype: file.type,
            datas: file.data,
        };
        const [att_id] = await this.orm.create("ir.attachment", [att_data], {
            context: { ...this.extraContext, ...this.env.searchModel.context },
        });
        this.attachmentIdsToProcess.push(att_id);
    }

    async onUploadComplete() {
        const action = await this.orm.call("purchase.order", "create_document_from_attachment", ["", this.attachmentIdsToProcess], {
            context: { ...this.extraContext, ...this.env.searchModel.context },
        });
        this.attachmentIdsToProcess = [];
        if (action.context && action.context.notifications) {
            for (let [file, msg] of Object.entries(action.context.notifications)) {
                this.notification.add(
                    msg,
                    {
                        title: file,
                        type: "info",
                        sticky: true,
                    });
            }
            delete action.context.notifications;
        }
        this.action.doAction(action);
    }

    async onDeleteSelectedRecords() {
    }
};

PurchaseListController.components = {
    ...ListController.components,
    FileUploader,
};

export const PurchaseDashBoardListViewExt = {
    ...listView,
    Controller: PurchaseListController,
    Renderer: PurchaseDashBoardRenderer,
    buttonTemplate: "upload_button.PurchaseViewUploadButton",
};

registry.category("views").add("purchase_dashboard_list_ext", PurchaseDashBoardListViewExt);