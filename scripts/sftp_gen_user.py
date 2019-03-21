#!/usr/bin/python
import os
import pwd
import grp
import sys

main_dir = "/data/sftp/"

def check_user_exists(name):
	try:
		return pwd.getpwnam(name)
	except KeyError:
		return None


def create_users(username, userpass):
	if not username or not userpass:
		print("Invalid user name or password error...")
		return False
	else:
		if not check_user_exists(username):
			cmd = "useradd -g sftpusers -d /" + username + " -s /sbin/nologin -p $(openssl passwd -1 " + userpass +  ") " + username
			os.system(cmd)
			return True
		else:
			print("User already exitsted!")
			return False

def create_work_directory(username):
	sub_dir = main_dir + username + '/upload'
	usr_dir = main_dir + username
	try:
		uid = pwd.getpwnam(username).pw_uid
		gid = grp.getgrnam("sftpusers").gr_gid
		os.makedirs(sub_dir)
		os.chown(usr_dir, 0, gid)
		os.chown(sub_dir, uid, gid)
	except OSError:
		if not os.path.isdir(sub_dir):
			raise

def main():
	username = raw_input("Please enter user name: ")
	userpass = raw_input("Please enter user password: ")
	try:
		create_users(username, userpass)
		create_work_directory(username)
	except:
        	print("Program terminated")
 	        sys.exit()

if __name__ == "__main__":
	main()
