import winrm
import getpass

server = 'beth-pc2'
username = 'beth'

password = getpass.getpass(
    'server: {}\nusername: {}\npassword: '.format(
        server, username))


s = winrm.Session(server, auth=(username, password))
cmd = 'ipconfig'
params = ['/all']

cmd = 'Powershell -Command "& {Get-Process}"'
params = []
r = s.run_cmd(cmd, params)
print r.status_code
print r.std_out
print r.std_err
