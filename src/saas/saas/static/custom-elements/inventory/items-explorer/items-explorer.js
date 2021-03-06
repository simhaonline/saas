'use strict';
import { notify, showInTab } from '/static/js/ui/ui.js';
import { InventoryItem } from '/static/js/modules/inventory/items.js';

class ItemsExplorer extends HTMLElement {

    constructor() {
        const self = super();

        const style = document.createElement("link");
        style.setAttribute('rel', 'stylesheet');
        style.setAttribute('href', '/static/custom-elements/inventory/items-explorer/items-explorer.css');

        const google_web_fonts = document.createElement("link");
        google_web_fonts.setAttribute('rel', 'stylesheet');
        google_web_fonts.setAttribute('href', 'https://fonts.googleapis.com/icon?family=Material+Icons');

        const div = document.createElement('div');
        div.classList.add('component-wrapper');

        this._init(div);

        const shadow = this.attachShadow({ mode: 'open' });
        shadow.appendChild(style);
        shadow.appendChild(google_web_fonts);
        shadow.appendChild(div);

        this._attachEventHandlers = this._attachEventHandlers.bind(this);
        this.setItems = this.setItems.bind(this);
        this._getClientId = this._getClientId.bind(this);

        this._attachEventHandlers();
    }

    _init(container) {
        const self = this;

        const client_id = this.getAttribute('client-id');

        const div = document.createElement('div');
        div.classList.add('wrapper');
        div.innerHTML = `
            <div class="form-wrapper">
                <div class="toolbar" role="toolbar">
                    <button type="button" class="btn btn-item-new" title="New Item">
                        <span class="material-icons">widgets</span>
                    </button> 
                </div><!-- .toolbar -->
                <form class="form-item-search">
                    <input type="hidden" id="client_id" value="${client_id}" />
                    <!-- filter -->
                    <label for="filter">Item</label>
                    <input type="search" id="filter" name="filter" class="form-input-search" title="Search for Item" placeholder="Item" />
                    <button type="button" class="btn btn-search" title="Search">
                        <span class="material-icons">search</span>
                    </button>
                </form>
            </div><!-- form-wrapper -->
            <div class="table-wrapper">
                <table class="tbl-items">
                    <caption>Items</caption>
                    <colgroup>
                    </colgroup>
                    <thead>
                        <tr>
                            <th></th>
                            <th>Name</th>
                            <th>SKU</th>
                            <th>UPC</th>
                        </tr>
                    </thead>
                    <tbody>
                    </tbody>
                    <tfoot>
                    </tfoot>
                </table>
            </div><!-- .table-wrapper -->
        `;

        container.appendChild(div);
    }

    _getClientId() {
        const self = this;
        const shadow = this.shadowRoot;

        const client = shadow.getElementById('client_id');
        return client.value;
    }

    _attachEventHandlers() {
        const self = this;
        const shadow = this.shadowRoot;

        const client_id = self._getClientId();

        const beginsearch = function(filter) {
            InventoryItem.find(client_id, filter, 10, 1).then((r) => {
                if (r.status == 'success') {
                    self.setItems(r.json.items, filter);
                } else {
                    notify(r.status, r.message);
                }
            });
        };

        const filter = shadow.getElementById('filter');
        filter.addEventListener('keyup', function(e) {
            if (e.keyCode == 13) {
                beginsearch(filter.value);
                e.preventDefault();
            }
        });

        const btnsearch = shadow.querySelector('button.btn-search');
        btnsearch.addEventListener('click', function(e) {
            beginsearch(filter.value);
            e.preventDefault();
        });

        const btnitemnew = shadow.querySelector('button.btn-item-new');
        btnitemnew.addEventListener('click', function(e) {
            showInTab('inventory-item', 'New Item', `<item-editor client-id="${client_id}"></item-editor>`);
            e.preventDefault();
        });
    }

    setItems(items = [], filter = '') {
        const self = this;
        const shadow = this.shadowRoot;

        const client_id = self._getClientId();

        const tbody = shadow.querySelector('table.tbl-items tbody');
        while(tbody.firstChild) {
            tbody.removeChild(tbody.lastChild);
        }

        items.forEach((item) => {
            const item_name = item.name.replace(filter, `<strong>${filter}</strong>`);
            const item_sku = item.sku.replace(filter, `<strong>${filter}</strong>`);
            const item_upc = item.upc.replace(filter, `<strong>${filter}</strong>`);

            const td = [];
            td.push(`<td><a class="link-edit-item" title="Edit Item" href="#" data-itemid="${item.id}"><span class="material-icons">edit</a></td>`);
            td.push(`<td>${item_name}</td>`);
            td.push(`<td>${item_sku}</td>`);
            td.push(`<td>${item_upc}</td>`);
            const tdall = td.join('');

            const tr = document.createElement('tr');
            tr.innerHTML = `${tdall}`;

            tbody.appendChild(tr);

            // event handlers
            const edititem = tr.querySelector('.link-edit-item');
            edititem.addEventListener('click', function(e) {
                const item_id = edititem.dataset.itemid;
                showInTab(`inventory.item.${item_id}`, 'Item', `<item-editor client-id="${client_id}" item-id="${item_id}"></item-editor>`);
                e.preventDefault();
            });
        });
    }
}
customElements.define('items-explorer', ItemsExplorer);
export { ItemsExplorer };