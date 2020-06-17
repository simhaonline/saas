/**
 * accounting
 */
create schema if not exists accounting;
set schema 'accounting';

\echo '** ACCOUNTING **'

/** tables **/
\ir tables/account_types.sql

\ir tables/accounts.sql
\ir tables/account_tree.sql
\ir tables/account_balances.sql


set schema 'public';