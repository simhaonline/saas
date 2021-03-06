/**
 * inventory management
 */
set schema 'inventory';


/** functions **/
\ir procs/categories/categories_all.sql
\ir procs/categories/category_add.sql

\ir procs/items/item_add.sql
\ir procs/items/item_update.sql
\ir procs/items/items_add_substitute.sql
\ir procs/items/item_substitutes.sql

\ir procs/items/item_components.sql
\ir procs/items/item_component_add.sql

\ir procs/items/items_all.sql
\ir procs/items/items_by_name.sql
\ir procs/items/item_by_id.sql
\ir procs/items/items_filter.sql

\ir procs/warehouses/warehouse_add.sql
\ir procs/warehouses/warehouse_update.sql
\ir procs/warehouses/warehouses_all.sql
\ir procs/warehouses/warehouses_filter.sql
\ir procs/warehouses/warehouses_get.sql

\ir procs/locations/location_add.sql
\ir procs/locations/location_update.sql
\ir procs/locations/location_filter.sql
\ir procs/locations/location_get.sql


set schema 'public';