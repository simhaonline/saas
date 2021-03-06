/**
 * initialize iam schema
 */

-- permissions
insert into iam.permissions (name) values
('user.authenticated'),
('admin.clients'),
('admin.security.permissions'),
('admin.security.roles'),
('admin.security.users'),
('clients.admin'),
('clients.admin.users'),
('clients.admin.roles'),
('accounting.dashboard'),
('accounting.admin'),
('inventory.admin'),
('inventory.dashboard'),
('inventory.items'),
('inventory.transactions.receiving'),
('inventory.transactions.receiving.add')
on conflict do nothing;