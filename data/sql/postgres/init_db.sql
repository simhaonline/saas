/**
 * initialize database
 */

set schema 'public';

/** pre init **/

begin;
\ir common/pre_init.sql
\ir iam/pre_init.sql
\ir accounting/pre_init.sql
\ir crm/pre_init.sql
\ir inventory/pre_init.sql

/** post init **/
\ir clients/post_init.sql
\ir iam/post_init.sql
\ir accounting/post_init.sql
commit;