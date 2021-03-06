import os
import sys
import subprocess
import logging
import time

def retrieve_data(analysis_id, cghub_key, output_dir, logger=None):
    if not os.path.isdir(os.path.join(output_dir, analysis_id)):

        cmd = ['gtdownload', '-v', '-c', cghub_key, '-p', output_dir, analysis_id]
        run_command(cmd, logger)

        #os.system("gtdownload -v -c %s -p %s %s" %(cghub_key, output_dir, analysis_id))

def run_command2(cmd, logger=None):
    """ Run a subprocess command """

    #stdoutdata, stderrdata = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    child = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    stdoutdata, stderrdata = child.communicate()
    exit_code = child.returncode

    if logger != None:
        stdoutdata = stdoutdata.split("\n")
        for line in stdoutdata:
            logger.info(line)

        stderrdata = stderrdata.split("\n")
        for line in stderrdata:
            logger.info(line)

    return exit_code

def run_command(cmd):
    """ Run a subprocess command """

    exit_code = subprocess.check_call(cmd, shell=True)
    return exit_code

def log_function_time(fn, analysis_id, cmd, logger=None):
    """ Log the time taken by a command to the logger """

    start_time = time.time()
    exit_code = run_command(cmd)
    end_time = time.time()

    if logger != None:
        logger.info("%s_TIME\t%s\t%s" %(fn, analysis_id,  (end_time - start_time)/60.0))
    return exit_code

def remove_dir(dirname):
    """ Remove a directory and all it's contents """

    if os.path.isdir(dirname):
        for filename in os.listdir(dirname):
            filename = os.path.join(dirname, filename)
            os.remove(filename)
        assert(os.listdir(dirname) == [])
        os.rmdir(dirname)
    else:
        raise Exception("Invalid directory: %s" % dirname)
