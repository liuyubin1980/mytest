import paramiko
import requests
import json
import time
from openpyxl import load_workbook
import logging,os
import configparser
import sys
import pandas as pd
from onebox import OneBox

curpath = os.path.dirname(os.path.realpath(sys.argv[0]))
filename = os.path.join(curpath,'sysinfo.xlsx')
df = pd.read_excel(filename)

loglevel = "DEBUG"
log = logging.getLogger(name='logger')
pycharm = logging.StreamHandler()
logfilename= sys.argv[0][:-3] + '.log'
file = logging.FileHandler(logfilename,encoding='utf-8')
fmt1 = "%(asctime)s - [%(funcName)s-->line:%(lineno)d] - %(levelname)s:%(message)s"
fmt2 = '[%(asctime)s-%(name)s-%(levelname)s-%(filename)s-%(lineno)d]:%(message)s'
pycharm_fmt = logging.Formatter(fmt=fmt1)
file_fmt = logging.Formatter(fmt=fmt2)
pycharm.setFormatter(fmt=pycharm_fmt)
file.setFormatter(fmt=file_fmt)
log.setLevel(loglevel)
log.addHandler(pycharm)
log.addHandler(file)



def getsysbak(name_in,hostname_in,username_in,password_in,datalink_in,datestr_in):

    log.info("name_in:"+name_in)
    log.info("hostname_in:" + hostname_in)
    log.info("username_in:" + username_in)
    log.info("password_in:" + password_in)
    log.info("datestr_in:" + datestr_in)
    log.info("datalink_in:" + datalink_in)

    name = name_in
    hostname = hostname_in
    username = username_in
    password = password_in
    datestr = datestr_in
    datalink = datalink_in

    # sftp.put(localpath=filename_o,remotepath='/home/gaussdba/002.csv')
    # sftp.put(localpath=filename_sql,remotepath='/home/gaussdba/002.sql')

    paramiko.util.log_to_file('syslogin.log') #发送paramiko日志到sy sLogi n.Log文件
    ssh = paramiko.SSHClient() #创建一个SSH客户端cLient对象
    ssh.load_system_host_keys() #获取客户端host_keys,默认~/.ssh/known_hosts,非默认路径需
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname=hostname,username=username,password=password) #创建SSH连接
    stdin,stdout,stderr = ssh.exec_command('rm -r -f /opt/databasebak/*') #调用远程执行命令方法exec_command()
    # stdin,stdout,stderr = ssh.exec_command('zsql gaussproject/gaussdba_123@127.0.0.1:1888 -q ; y;BACKUP DATABASE FULL FORMAT /opt/databasebak/20250726 AS COMPRESSED BACKUPSET;') #调用远程执行命令方法exec_command()
    rst = stdout.read().decode( 'utf-8' )
    log.info(rst)

    stdin,stdout,stderr = ssh.exec_command('true > /opt/databasebak/003.sql;echo "BACKUP DATABASE FULL FORMAT \'/opt/databasebak/'+datestr+'\'AS COMPRESSED BACKUPSET;"  >> /opt/databasebak/003.sql') #调用远程执行命令方法exec_command()
    # stdin,stdout,stderr = ssh.exec_command('zsql gaussproject/gaussdba_123@127.0.0.1:1888 -q ; y;BACKUP DATABASE FULL FORMAT /opt/databasebak/20250726 AS COMPRESSED BACKUPSET;') #调用远程执行命令方法exec_command()
    rst = stdout.read().decode( 'utf-8' )
    log.info(rst)

    stdin,stdout,stderr = ssh.exec_command(datalink+' -q -f "/opt/databasebak/003.sql"') #调用远程执行命令方法exec_command()
    # stdin,stdout,stderr = ssh.exec_command('zsql gaussproject/gaussdba_123@127.0.0.1:1888 -q ; y;BACKUP DATABASE FULL FORMAT /opt/databasebak/20250726 AS COMPRESSED BACKUPSET;') #调用远程执行命令方法exec_command()
    rst = stdout.read().decode( 'utf-8' )
    log.info(rst)

    stdin,stdout,stderr = ssh.exec_command('cd /opt/databasebak;tar -czvf '+datestr+'.tar.gz '+datestr) #调用远程执行命令方法exec_command()
    rst = stdout.read().decode( 'utf-8' )
    log.info(rst)


    #下载文件
    client = paramiko.Transport((hostname,22))
    client.connect(username=username,password=password)
    sftp = paramiko.SFTPClient.from_transport(client)
    sftp.get(localpath='d:/sysbak/'+name+'_'+datestr+'.tar.gz',remotepath='/opt/databasebak/'+datestr+'.tar.gz')
    time.sleep(3)
    sftp.close()
    ssh.close()



def getsysbak_V5(name_in,hostname_in,username_in,password_in,datalink_in,datestr_in):

    log.info("name_in:"+name_in)
    log.info("hostname_in:" + hostname_in)
    log.info("username_in:" + username_in)
    log.info("password_in:" + password_in)
    log.info("datestr_in:" + datestr_in)
    log.info("datalink_in:" + datalink_in)

    name = name_in
    hostname = hostname_in
    username = username_in
    password = password_in
    datestr = datestr_in
    datalink = datalink_in
    paramiko.util.log_to_file('syslogin.log')  # 发送paramiko日志到sy sLogi n.Log文件
    ssh = paramiko.SSHClient()  # 创建一个SSH客户端cLient对象
    ssh.load_system_host_keys()  # 获取客户端host_keys,默认~/.ssh/known_hosts,非默认路径需
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname=hostname, username=username, password=password)  # 创建SSH连接
    stdin, stdout, stderr = ssh.exec_command('rm -r -f /opt/databasebak/*')  # 调用远程执行命令方法exec_command()
    rst = stdout.read().decode('utf-8')

    stdin, stdout, stderr = ssh.exec_command(datalink)  # 调用远程执行命令方法exec_command()
    rst = stdout.read().decode('utf-8')

    # # 下载文件
    client = paramiko.Transport((hostname, 22))
    client.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(client)
    sftp.get(localpath='d:/sysbak/' + name + '_' + datestr + '.tar.gz',
             remotepath='/opt/databasebak/overallview.tar')
    time.sleep(3)
    sftp.close()
    ssh.close()







timeTuple = time.localtime(time.time())
datestr = str(timeTuple[0]) + "%02d" % timeTuple[1] + "%02d" % timeTuple[2]
log.info("datestr:"+datestr)


for row in df.itertuples():
    name = str(getattr(row, 'name'))
    hostname = str(getattr(row, 'hostname'))
    username = str(getattr(row, 'username'))
    password = str(getattr(row, 'password'))
    datalink = str(getattr(row, 'datalink'))
    type = str(getattr(row, 'type'))
    backflag = str(getattr(row, 'backflag'))
    try:
        if backflag == "n":
            continue
        if type == "V3":
            getsysbak(name, hostname, username, password, datalink, datestr)
        elif type == ("V5"):
            getsysbak_V5(name, hostname, username, password, datalink, datestr)
        file_path = 'd:/sysbak/'+name+'_'+datestr+'.tar.gz'
        onebox = OneBox(file_path)
        result = onebox.upload_file()
        if result is True:
            log.info("上传成功！"+file_path)
        else:
            log.info("上传失败！"+file_path)
    except Exception as e:
        log.info(name +" fail.")
        log.info(e)



