set feed off
set verify off
set pagesize 0
set linesize 132
set echo off
set heading off
set termout off

col ba noprint new_value ba
col dc noprint new_value dc
col dn noprint new_value dn
col ds noprint new_value ds
col ht noprint new_value ht
col sa noprint new_value sa
col sd noprint new_value sd
col st noprint new_value st
col su noprint new_value su

SELECT to_char(sysdate,'dd/mm/yy hh24:mi:ss') as sd from dual;
SELECT banner ba from v$version;
SELECT to_char(created,'dd/mm/yy hh24:mi:ss') as dc from v$database;
SELECT instance_name dn, host_name ht, to_char(startup_time,'dd/mm/yy hh24:mi:ss') ds, status st FROM v$instance;
SELECT to_char(sum(bytes)/1024/1024/1024,'9,999.99') as sa from dba_data_files;
SELECT to_char(sum(bytes)/1024/1024/1024,'9,999.99') as su from dba_segments;

set termout on

prompt Current Time   : &sd
prompt
prompt Database Details
prompt ===============================================
prompt Hostname        : &ht
prompt Database Name   : &dn
prompt Version         : &ba
prompt Date Created    : &dc
prompt Date Started    : &ds
prompt DB Status       : &st
prompt Allocated Space : &sa GB
prompt Used Space      : &su GB

prompt
EXIT
