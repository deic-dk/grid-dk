#!/usr/bin/python 
# 
# This MiG python script was autogenerated by the MiG User Script Generator !!!
# Any changes should be made in the generator and not here !!!

import sys
import os
import getopt

def version():
	print "MiG User Scripts: $Revision: 2506 $,$Revision: 2506 $"

def check_var(name, var):

        if not var:
           print name + " not set! Please set in configuration file or through the command line"
           sys.exit(1)

def read_conf(conf, option):

        try:
            conf_file = open(conf, 'r')
            for line in conf_file.readlines():
                line = line.strip()
                # split on any whitespace and assure at least two parts
                parts = line.split() + ['', '']
                opt, val = parts[0], parts[1]
                if opt == option:
                    return val
            conf_file.close()
        except Exception, e:
            return ''


def expand_name(path_list, server_flags, destinations):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl --compressed'
        target = ''
        location = "cgi-bin/expand.py"
        post_data = 'output_format=txt;flags=%s;%s;with_dest=%s' % (server_flags, path_list, destinations)
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def cancel_job(job_id):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl '
        target = ''
        location = "cgi-bin/canceljob.py"
        post_data = 'output_format=txt;flags=%s;job_id=%s' % (server_flags, job_id)
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def cat_file(path_list):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl --compressed'
        target = ''
        location = "cgi-bin/cat.py"
        post_data = 'output_format=txt;flags=%s;%s' % (server_flags, path_list)
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def show_doc(search, show):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl --compressed'
        target = ''
        location = "cgi-bin/docs.py"
        post_data = 'output_format=txt;flags=%s;search=%s;show=%s' % (server_flags, search, show)
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def get_file(src_path, dst_path):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl --compressed --create-dirs'
        target = '--output %s' % dst_path
        location = "cert_redirect/%s" % src_path.lstrip("/")
        post_data = ""
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def head_file(lines, path_list):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl --compressed'
        target = ''
        location = "cgi-bin/head.py"
        post_data = 'output_format=txt;flags=%s;%s;lines=%s' % (server_flags, path_list, lines)
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def ls_file(path_list):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl --compressed'
        target = ''
        location = "cgi-bin/ls.py"
        post_data = 'output_format=txt;flags=%s;%s' % (server_flags, path_list)
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def mk_dir(path_list):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl '
        target = ''
        location = "cgi-bin/mkdir.py"
        post_data = 'output_format=txt;flags=%s;%s' % (server_flags, path_list)
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def mv_file(src_list, dst):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl --compressed'
        target = ''
        location = "cgi-bin/mv.py"
        post_data = 'output_format=txt;flags=%s;dst=%s;%s' % (server_flags, dst, src_list)
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def put_file(src_path, dst_path, submit_mrsl, extract_package):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

        content_type = "''"
        if submit_mrsl and extract_package:
           content_type = 'Content-Type:submitandextract'
        elif submit_mrsl:
           content_type = 'Content-Type:submitmrsl'
        elif extract_package:
           content_type = 'Content-Type:extractpackage'

	# import StringIO

        curl = 'curl --compressed'
        target = '--upload-file %s --header %s -X CERTPUT' % (src_path, content_type)
        location = "%s" % dst_path.lstrip("/")
        post_data = ""
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def read_file(first, last, src_path, dst_path):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl --compressed'
        target = '--output %s' % dst_path
        location = "cgi-bin/rangefileaccess.py"
        post_data = ""
        query = '?output_format=txt;flags=%s;file_startpos=%s;file_endpos=%s;path=%s' % (server_flags, first, last, src_path)
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def rm_file(path_list):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl '
        target = ''
        location = "cgi-bin/rm.py"
        post_data = 'output_format=txt;flags=%s;%s' % (server_flags, path_list)
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def rm_dir(path_list):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl '
        target = ''
        location = "cgi-bin/rmdir.py"
        post_data = 'output_format=txt;flags=%s;%s' % (server_flags, path_list)
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def stat_file(path_list):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl --compressed'
        target = ''
        location = "cgi-bin/stat.py"
        post_data = 'output_format=txt;flags=%s;%s' % (server_flags, path_list)
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def job_status(job_list):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)
	max_job_count  = 100
        if not max_job_count:
           max_jobs = ''
        else:
           max_jobs = "max_jobs=%s" % (max_job_count)

	# import StringIO

        curl = 'curl --compressed'
        target = ''
        location = "cgi-bin/jobstatus.py"
        post_data = 'output_format=txt;flags=%s;max_jobs=%s;%s' % (server_flags, max_job_count, job_list)
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def submit_file(src_path, dst_path, submit_mrsl, extract_package):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

        content_type = "''"
        if submit_mrsl and extract_package:
           content_type = 'Content-Type:submitandextract'
        elif submit_mrsl:
           content_type = 'Content-Type:submitmrsl'
        elif extract_package:
           content_type = 'Content-Type:extractpackage'

	# import StringIO

        curl = 'curl '
        target = '--upload-file %s --header %s -X CERTPUT' % (src_path, content_type)
        location = "%s" % dst_path.lstrip("/")
        post_data = ""
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def tail_file(lines, path_list):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl --compressed'
        target = ''
        location = "cgi-bin/tail.py"
        post_data = 'output_format=txt;flags=%s;lines=%s;%s' % (server_flags, lines, path_list)
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def touch_file(path_list):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl '
        target = ''
        location = "cgi-bin/touch.py"
        post_data = 'output_format=txt;flags=%s;%s' % (server_flags, path_list)
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def truncate_file(size, path_list):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl --compressed'
        target = ''
        location = "cgi-bin/truncate.py"
        post_data = 'output_format=txt;flags=%s;size=%s;%s' % (server_flags, size, path_list)
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def wc_file(path_list):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl '
        target = ''
        location = "cgi-bin/wc.py"
        post_data = 'output_format=txt;flags=%s;%s' % (server_flags, path_list)
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def write_file(first, last, src_path, dst_path):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl --compressed'
        target = '--upload-file %s' % src_path
        location = "cgi-bin/rangefileaccess.py"
        post_data = ""
        query = '?output_format=txt;flags=%s;file_startpos=%s;file_endpos=%s;path=%s' % (server_flags, first, last, dst_path)
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)


def job_liveoutput(job_list):

        if not ca_cert_file:
           ca_check = '--insecure'
        else:
           ca_check = "--cacert %s" % (ca_cert_file)

        if not password:
           password_check = ''
        else:
           password_check = "--pass %s" % (password)

        timeout = ''
        if max_time:
           timeout += "--max-time %s" % (max_time)
        if connect_timeout:
           timeout += " --connect-timeout %s" % (connect_timeout)

	# import StringIO

        curl = 'curl --compressed'
        target = ''
        location = "cgi-bin/liveoutput.py"
        post_data = 'output_format=txt;flags=%s;%s' % (server_flags, job_list)
        query = ""
        data = ''
        if post_data:
            data = '--data "%s"' % post_data
        command = "%s --fail --silent --cert %s --key %s %s %s %s %s %s --url '%s/%s%s'" % (curl, cert_file, key_file, data, ca_check, password_check, timeout, target, mig_server, location, query)
        # TODO: should we replace popen4 call with this next section?
        #from subprocess import Popen, PIPE, STDOUT
        #proc = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT,
        #                     close_fds=True)
        #out = proc.stdout.readlines()
        #proc.stdout.close()
        #exit_code = proc.returncode
        (_, all_out) = os.popen4(command, 'r', 0)
        out = all_out.readlines()
        status = all_out.close()
        if status:
            exit_code = status >> 8
        else:
            exit_code = 0

	return (exit_code, out)



# === Main ===

recursive = 0
verbose = 0
conf = os.path.expanduser("~/.mig/miguser.conf")
flags = ""
mig_server = ""
server_flags = ""
script_path = sys.argv[0]
script_name = os.path.basename(script_path)
script_dir = os.path.dirname(script_path)

if not os.path.isfile(conf):
   print "Failed to read configuration file: %s" % (conf)
   sys.exit(1)

if verbose:
    print "using configuration in %s" % (conf)

if not mig_server:
   mig_server = read_conf(conf, 'migserver')

cert_file = read_conf(conf, 'certfile')
key_file = read_conf(conf, 'keyfile')
ca_cert_file = read_conf(conf, 'cacertfile')
password = read_conf(conf, 'password')
connect_timeout = read_conf(conf, 'connect_timeout')
max_time = read_conf(conf, 'max_time')

check_var("migserver", mig_server)
check_var("certfile", cert_file)
check_var("keyfile", key_file)
