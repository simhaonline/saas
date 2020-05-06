'use strict';

class PermissionsTable extends HTMLElement {

    constructor() {
        self = super();

        const div = document.createElement('div');
        div.classList.add('wrapper');

        this.initTable(self, div);

        const shadow = this.attachShadow({ mode: 'open' });
        shadow.appendChild(div);

        this.setPermissions = this.setPermissions.bind(this);
        this.getSelected = this.getSelected.bind(this);
    }

    setPermissions(permissions, options) {
        const self = this;
        if (Array.isArray(permissions)) {
            const tbl = this.shadowRoot.querySelector('table.tbl-permissions tbody');
            while(tbl.firstChild) {
                tbl.removeChild(tbl.lastChild);
            }
            permissions.forEach(p => {
                const tr = document.createElement('tr');
                tr.classList.add('permission-item');
                if (options && options.multiselect == true) {
                    tr.innerHTML = `
                        <td>
                            <input type="checkbox" name="selectedPermission" title="Select" class="form-input-radio permission-select" value="${p.id}" />
                        </td>
                        <td>
                            <a title="Toggle Active" class="nav-link permission-active" href="#" data-id="${p.id}" data-active="${p.active}">${p.active}</a>
                        </td>
                        <td>${p.name}</td>
                    `;
                } else {
                    tr.innerHTML = `
                        <td>
                            <input type="radio" name="selectedPermission" title="Select" class="form-input-radio permission-select" value="${p.id}" />
                        </td>
                        <td>
                            <a title="Toggle Active" class="nav-link permission-active" href="#" data-id="${p.id}" data-active="${p.active}">${p.active}</a>
                        </td>
                        <td>${p.name}</td>
                    `;
                }

                tbl.appendChild(tr);

                const permSelect = tr.querySelector('input.permission-select');
                permSelect.addEventListener('change', function(e) {
                    self.dispatchEvent(new CustomEvent('onselectpermission', {
                        bubbles: true,
                        cancelable: true,
                        detail: {
                            permissionId: permSelect.value
                        }
                    }));
                });

                const aActive = tr.querySelector('a.permission-active');
                aActive.addEventListener('click', function(e) {
                    self.dispatchEvent(new CustomEvent('onupdatepermissionactive', {
                        bubbles: true,
                        cancelable: true,
                        detail: {
                            permissionId: aActive.dataset.id,
                            active: aActive.dataset.active
                        }
                    }));
                });
            });

            if (options && options.allowAdd == true) {
                const tr = document.createElement('tr');
                tr.classList.add('permission-add');
                tr.innerHTML = `
                    <td colspan="3">
                        <a id="permissionAdd" class="nav-link permission-add" title="Add Permission" href="#">Add</a>
                    </td>
                `;
                tbl.appendChild(tr);

                const lAdd = tr.querySelector('a#permissionAdd');
                lAdd.addEventListener('click', function(e) {
                    self.dispatchEvent(new CustomEvent('onaddpermission', {
                        bubbles: true,
                        cancelable: true
                    }));
                });
            }
        } else {
            self.dispatchEvent(new CustomEvent('onerror', {
                bubbles: true,
                cancelable: true,
                detail: "Expected an array of permissions"
            }));
        }
    }

    getSelected() {
        const self = this;
        const shadow = this.shadowRoot;
        const permissions = [];
        const nl = shadow.querySelectorAll('input.permission-select:checked');
        nl.forEach(n => {
            permissions.push(n.value);
        });
        return permissions;
    }

    initTable(component, container) {
        const div = document.createElement('div');
        div.classList.add('table-wrapper');
        div.innerHTML = `
            <form class="form-permissions">
                <table class="tbl-permissions">
                    <caption>Permissions</caption>
                    <thead>
                        <tr>
                            <th><th>
                            <th>Active</th>
                            <th>Name</th>
                        </tr>
                    </thead>
                    <tbody>
                    </tbody>
                </table><!-- .tbl-permissions -->
            </form>
        `;

        container.appendChild(div);
    }
}

customElements.define('permissions-table', PermissionsTable);
export { PermissionsTable };