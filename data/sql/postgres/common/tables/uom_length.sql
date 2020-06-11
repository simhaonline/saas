create table if not exists uom_length (
    id int not null,
    name varchar(30) not null,
    constraint pk_uom_length primary key (id),
    constraint u_uom_length unique (name)
);