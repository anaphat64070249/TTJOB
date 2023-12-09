create table Employee(
	emp_id int(8) primary key not null auto_increment,
    email varchar(255) not null unique,
    phone varchar(10) not null,
    user_status int(1) default 0,
    free_status boolean default true
);
alter table Employee auto_increment = 10000000;

create table Emp_address(
	address_code int (8) not null auto_increment,
    emp_id int(8) not null,
    district varchar(150) not null,
    tumbon varchar(150) not null,
    province varchar(150) not null,
    zipCode varchar(10) not null,
    address text not null,
    primary key(address_code)
    -- foreign key(emp_id) references Employee(emp_id)
);
alter table Emp_address auto_increment = 10000000;

create table Personal_infomations(
	personal_infoID int(8) not null auto_increment,
    emp_id int(8) not null,
    firstName varchar(100) not null,
    lastName varchar(100) not null,
    nickName varchar(100) not null,
    age int(4) not null,
    gender varchar(40) not null,
    personal_id varchar(13) not null,
    date_of_birth date not null,
    weight real not null,
    height real not null,
    occupation varchar(120) not null,
    education varchar(120) not null,
    abilities text null,
    image_profile text null,
    image_personalID text not null,
    address_code int(8) not null,
    intro_message text null,
    vehicle varchar(120) not null,
    driver_license varchar(120) not null,
    experience_hour real default 0.0,
    avg_score real default 0.0,
	primary key(personal_infoID)
--     foreign key (emp_id) references Employee(emp_id),
--     foreign key (address_code) references Emp_address(address_code)
);
alter table Personal_infomations auto_increment = 10000000;

create table Company(
	com_id int(8) not null auto_increment,
    email varchar(255) not null,
    phone varchar(10) not null unique,
    user_status int(1) default 0,
    primary key(com_id)
);
alter table Company auto_increment = 10000000;


create table Com_address(
	address_code int (8) not null auto_increment,
    com_id int(8) not null,
    district varchar(150) not null,
    tumbon varchar(150) not null,
    province varchar(150) not null,
    zipCode varchar(10) not null,
    address text not null,
    primary key(address_code)
--     foreign key(com_id) references Company(com_id)
);
alter table Com_address auto_increment = 10000000;

create table Company_infomations(
	com_infoID int(8) not null auto_increment,
    com_id int not null,
    companyName varchar(255) not null,
    juristic_id varchar(255) null unique,
	image_juristic text null ,
    image_company text not null default "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKg8T74L-rk32oPK9vtoiWHNXFDOHTfYCmsQ&usqp=CAU",
    bussines_type text not null,
    address_code int(8) not null,
    descriptions text null,
    primary key(com_infoID)
-- 	foreign key(com_id) references Company(com_id)
);
alter table Company_infomations auto_increment = 10000000;

create table Jobs(
	job_id int(10) not null auto_increment,
    com_id int(8) not null,
    position varchar(100) not null,
    job_scope text not null,
    job_infomation text not null,
    job_date_declear date not null,
    day_start date not null,
    day_end date not null,
    time_start varchar(10) not null,
    time_end varchar(10) not null,
    working_hours varchar(10) not null,
    day_work int(2) not null,
    pay real not null,
    status boolean default false,
    emp_amount int(4) not null,
	manager_name varchar(100) not null,
    apply_type int (2) not null,
    primary key(job_id)
--     foreign key(com_id) references Company(com_id)
);
alter table Jobs auto_increment = 10000000;


create table Job_registor(
	job_id int(10) not null,
    emp_id int(8) not null,
    data_apply date not null,
    com_confirm boolean default false,
    emp_confirm boolean default false,
    date_emp_confirm date null,
    date_com_confirm date null,
    cancel_status boolean default false,
    primary key(job_id, emp_id),
    job_doing boolean default false,
    isFinish boolean default false
--     foreign key(job_id) references Jobs(job_id),
--     foreign key(emp_id) references Employee(emp_id)
);

create table Job_employees(
	job_id int (10) not null,
    emp_id int(8) not null,
    primary key(job_id, emp_id)
--     foreign key(job_id) references Jobs(job_id),
--     foreign key(emp_id) references Employee(emp_id)
);

create table Emp_job_history(
	job_id int(10) not null,
    emp_id int(8) not null,
    pay real not null,
    work_hour real not null,
    job_status boolean null,
    annotation text null,
    primary key(job_id, emp_id)
--     foreign key(job_id) references Jobs(job_id),
--     foreign key(emp_id) references Employee(emp_id)
);


create table Reviews(
	emp_id int(8) not null,
    job_id int(10) not null,
    reviewer_name varchar(255) not null,
    score real not null,
    comments text null,
    report varchar(200) null,
    primary key(emp_id, job_id)
--     foreign key(emp_id) references Employee(emp_id),
--     foreign key(job_id) references Jobs(job_id)
);












