import sys, os, subprocess, argparse, re, time, datetime, io, glob
from datetime import timedelta
import logging
from functools import wraps

# Global variables
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SCRIPT_NAME = os.path.basename(os.path.realpath(__file__))
SIGN_TOOL = 'Signtool.exe'
INF_TO_CAT = 'inf2cat.exe'
TIMESTAMP_URLS = [
    'http://timestamp.iglb.intel.com/TSS/HttpTspServer'
]
RETRIES = 6
RETRY_DELAY = 30

CAT_OS_SUPPORT = [
    '7_X64',
    '8_X64',
    '10_X64',
    'Server10_X64',
    '10_AU_X64',
    'Server2016_X64',
    '10_RS2_X64',
    'ServerRS2_X64',
    '10_RS3_X64',
    'ServerRS3_X64',
    '10_RS4_X86',
    '10_RS4_X64',
    'ServerRS4_X64'
]

def retry(Exception, tries=4, delay=3, backoff=2):
    def decorator_retry(func):

        @wraps(func)
        def func_retry(*args, **kwargs):
            tries_left, delay_seconds = tries, delay
            while tries_left > 1:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    message = "%s, Retrying in %d seconds..." % (str(e), delay_seconds)
                    log.warning(message)
                    time.sleep(delay_seconds)
                    tries_left -= 1
                    delay_seconds *= backoff
            return func(*args, **kwargs)
        return func_retry
    return decorator_retry


def init_logging():
    """ Initializes logging capabilities """
    global log
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    logformatter = logging.Formatter("%(asctime)-20s %(levelname)8s: %(message)s",
                                     datefmt='%b %d %H:%M:%S')

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logformatter)
    log.addHandler(consoleHandler)

    log.info('*' * 48)
    log.info('Starting')
    log.info('*' * 48)


def main(argv):
    init_logging()

    parser = argparse.ArgumentParser(description='Sign driver files')
    parser.add_argument('-d', '--driver-dir', help='Directory of driver file(s) to sign', required=True)
    parser.add_argument('-s', '--signtool-dir', help='Directory of sign tool')
    parser.add_argument('-k', '--kmcs', action='store_true', help='Generate CAT file and sign driver files')
    parser.add_argument('-ha', '--hash', help='Hash digest, SHA384 minimum', default='SHA384')
    parser.add_argument('-th', '--t-hash', help='Timestamp hash digest, SHA384 minimum', default='SHA384')
    parser.add_argument('-c', '--cert', help='Certificate name to sign with', default=None)
    parser.add_argument('-pd', '--pfx-file-dir', help='Directory of .pfx file')
    parser.add_argument('-ss', '--self-sign', action='store_true',
                        help='Indicate a self-signed cert to disable /kp Chain-to-Microsoft verification', default=True)
    parser.add_argument('-ic', '--import-cert-only', action='store_true',
                        help='Import certificate and exit', default=False)
    parser.add_argument('-v', '--verbose', action='store_true', help='Stream logs directly to console')
    parser.add_argument('-rt', '--retries', help='Set the number of retries for signing operations, default=6.', default=6)
    parser.add_argument('-rd', '--retry-delay', help='Set the retry delay increment in seconds, default=30.', default=30)
    parser.add_argument('-ks1', '--kmcs-sha1', help='KMCS Certificate SHA1 thumbprint', default=None)
    args = parser.parse_args()

    # Set verbosity
    if not args.verbose:
        log.setLevel(logging.WARNING)
    # Make sure user only supplies EITHER a cert or a sha1
    if args.kmcs:
        if args.cert and args.kmcs_sha1:
            log.error('Both --cert and --kmcs-sha1 were provided; please use only one.')
            sys.exit(1)
        if not args.cert and not args.kmcs_sha1 and not args.self_sign:
            log.error('No --cert or --kmcs-sha1 provided.')
            sys.exit(1)

    # Import self-signed cert if not imported already
    pfx_file_path = None
    pfx_thumbprint = None
    if args.self_sign:
        if not args.pfx_file_dir:
            log.error('Argument --self-sign requires --pfx-file-dir to be specified')
            sys.exit(1)
        # Get PFX file path
        pfx_file_dir = os.path.abspath(args.pfx_file_dir)
        pfx_file_path = glob.glob(os.path.join(pfx_file_dir, '*.pfx'))
        if not pfx_file_path:
            log.error('Failed to get PFX file path from directory %s', pfx_file_dir)
            sys.exit(1)
        if len(pfx_file_path) > 1:
            log.error('Multiple PFX files found in directory %s', pfx_file_dir)
            sys.exit(1)
        pfx_file_path = pfx_file_path[0]
        try:
            pfx_thumbprint = import_certificate(pfx_file_path)
        except:
            sys.exit(1)
        if args.import_cert_only:
            return 0

    if args.signtool_dir:
        sign_tool_path = os.path.join(args.signtools_dir, SIGN_TOOL)
    else:
        # Get signtool path
        sign_tool_path = glob.glob(os.path.join(SCRIPT_DIR, '..', '..', '..', '..', 'build', 'ewdk', 'Program Files',
                                                'Windows Kits', '10', 'bin', '**', 'x64', SIGN_TOOL), recursive=True)[0]

    # Get inf2cat path
    # TODO: use inf2cat from eWDK - It may not be used today due OS
    # dependency returning error: Operating systems parameter invalid
    inf_to_cat_path = glob.glob(os.path.join(SCRIPT_DIR, '..', '..', '..', '..', 'build', 'wdk',
                                             'bin', '**', 'x86', INF_TO_CAT), recursive=True)[0]

    # Verify if signtool and inf2cat exist
    for tool in [sign_tool_path, inf_to_cat_path]:
        if not tool or not os.path.exists(tool):
            log.error('Unable to find tool')
            sys.exit(1)

    # Make sure driverpath is an absolute path
    driver_dir = os.path.abspath(args.driver_dir)

    # Get inf paths from driver directory and subfolders
    inf_files = glob.glob(os.path.join(driver_dir, '**', '*.inf'), recursive=True)

    global RETRIES
    RETRIES = args.retries
    global RETRY_DELAY
    RETRY_DELAY = args.retry_delay

    if args.kmcs:
        # Generate catalog files
        try:
            generate_cat_files(driver_dir, inf_to_cat_path , inf_files)
        except:
            sys.exit(1)

        # List of file patterns to sign
        file_patterns = ['*.sys', '*.cat']
        all_files, _ = sign_files_aux(args, file_patterns, driver_dir, sign_tool_path,
                                      pfx_file_path, pfx_thumbprint, cert_thumbprint=args.kmcs_sha1)

        try:
            # Create .sys and .cat dictionary
            sys_cat_dict = create_sys_cat_dict(inf_files)
        except:
            sys.exit(1)

        verify_signature_aux(args, all_files, sign_tool_path, sys_cat_dict)

        log.info('Exiting %s with exit code 0', SCRIPT_NAME)
        return 0


def inf_to_dictionary(inf_content):
    # Helper function to struct Inf content as dictionary.

    inf_section = ''
    json_obj = {}
    json_obj['sections'] = {}

    for line in inf_content:
        if line.startswith('['):
            inf_section = re.search('\[(.*)\]', line).group(1)
            if not inf_section in json_obj['sections']:
                json_obj['sections'][inf_section] = []
        else:
            if inf_section:
                if not line.strip() == '' and not line.startswith(';'):
                    json_obj['sections'][inf_section].append(line)
    return json_obj


def read_inf_as_dictionary(inf_file):
    # Read Inf content and return as dictionary
    json_obj = {}
    # Setting default encoding order
    encodings = ['utf_16_le', 'utf-8', 'ascii']

    for encoding in encodings:
        try:
            with open(inf_file, 'r', encoding=encoding) as inf_content:
                json_obj = inf_to_dictionary(inf_content)
        except UnicodeDecodeError:
            continue

        if json_obj['sections']:
            return json_obj

    log.error('Unable to parse %s using encodings %s', inf_file, ', '.join(encodings))
    raise Exception('Failure in read_inf_as_dictionary()')


def get_file_names_from_inf(inf_file, matched_files, lookup_section, lookup_property, lookup_index):
    """ Parse the Inf and return files corresponding to the lookup section, property and index """
    try:
        inf_content = read_inf_as_dictionary(inf_file)
    except:
        log.error('Unable to get inf content')
        sys.exit(1)

    if not inf_content:
        log.info('No sections found in %s', inf_file)
        return matched_files

    if 'sections' in inf_content:
        if lookup_section in inf_content['sections']:
            for line in inf_content['sections'][lookup_section]:
                if lookup_property in line:
                    file = line.split('=')[lookup_index].strip()
                    if not file in matched_files:
                        matched_files.append(file)
    return matched_files


def get_files_to_sign(driver_dir, file_types):
        # Create a list of paths for files to sign
        files_to_sign = []
        for file_type in file_types:
            files_to_sign.append(glob.glob(os.path.join(driver_dir, '**', file_type), recursive=True))
        # Convert files_to_sign into flat list
        if any(isinstance(elem, list) for elem in files_to_sign):
            files_to_sign = [item for elem in files_to_sign for item in elem]
        return files_to_sign


def generate_cat_files(driver_dir, inf_to_cat_path, inf_files):
    log.info('Generating the .cat files')
    cmd = list()
    cmd = [inf_to_cat_path, '/verbose', '/driver:' + driver_dir]
    cmd += [f'/os:{",".join(CAT_OS_SUPPORT)}']
    exit_code, _ = execute_cmd(cmd, os.path.dirname(inf_to_cat_path))
    if exit_code != 0:
        log.error('Generating CAT files returned error code: ' + str(exit_code))
        raise Exception('Failure in generate_cat_files()')
    else:
        log.info('Succesfully generated the .cat files')


def create_sys_cat_dict(inf_files):
    # Get .sys and .cat from Inf and create a dictionary
    sys_cat_dict = {}
    for inf_file in inf_files:
        sys_file_names = []
        cat_file_names = []
        inf_file_dir = os.path.dirname(inf_file)
        cat_file_names = get_file_names_from_inf(inf_file, cat_file_names, 'Version', 'CatalogFile', 1)
        if len(cat_file_names) > 1:
            log.error('Multiple .cat files found in %s', inf_file)
            raise Exception('Failure in create_sys_cat_dict()')
        cat_file_name = cat_file_names[0]
        # Convert to lower case to avoid case mismatch between file name and inf entry
        cat_file_path = os.path.join(inf_file_dir, cat_file_name).lower()

        for lookup_section in ['SourceDisksFiles', 'SourceDisksFiles.amd64']:
            sys_file_names = get_file_names_from_inf(inf_file, sys_file_names, lookup_section, '.sys', 0)

        for sys_file_name in sys_file_names:
            # Convert to lower case to avoid case mismatch between file name and inf entry
            sys_file_path = os.path.join(inf_file_dir, sys_file_name).lower()
            if sys_file_path not in sys_cat_dict:
                sys_cat_dict[sys_file_path] = cat_file_path

    if len(sys_cat_dict) == 0:
        log.error('Unable to create .sys and .cat dictionary')
        raise Exception('Failure in create_sys_cat_dict()')
    return sys_cat_dict


def sign_files_aux(args, file_patterns, driver_dir, sign_tool_path,
                   pfx_file_path, pfx_thumbprint, cert_thumbprint=None):
    all_files = files_to_sign = get_files_to_sign(driver_dir, file_patterns)
    if not files_to_sign:
        log.error('Could not find %s files in %s', ','.join(file_patterns), driver_dir)
        sys.exit(1)

    # Remove signed binaries from files to sign
    if pfx_thumbprint or cert_thumbprint:
        files_to_sign = get_unsigned_files(all_files, sign_tool_path,
                                           thumbprint = pfx_thumbprint if pfx_thumbprint else cert_thumbprint)

    # Sign files
    if files_to_sign:
        try:
            sign_files(sign_tool_path, files_to_sign, args.hash, args.t_hash,
                       args.cert, pfx_file_path, cert_thumbprint=cert_thumbprint)
        except:
            sys.exit(1)
    return all_files, files_to_sign


# Sign files with 6 retries (delay of 30..60..120..240..480..960 seconds - 31 min, 30 sec total)
@retry(Exception, tries=RETRIES, delay=RETRY_DELAY)
def sign_files(sign_tool_path, file_list, file_digest, time_digest,
               cert_name=None, pfx_file_path=None, cert_thumbprint=None):
    log.info('Signing files')
    timestamp_choice = 0
    current_date = None
    unsigned_list = file_list
    for attempt in range(int(RETRIES)):
        cmd = [sign_tool_path, 'sign', '/a', '/v',
                   '/fd', file_digest,
                   '/td', time_digest,
                   '/tr', TIMESTAMP_URLS[timestamp_choice]
        ]

        if cert_thumbprint:
            cmd += ['/sha1', cert_thumbprint]
        elif cert_name:
            cmd += ['/n', cert_name]
        elif pfx_file_path:
            cmd += ['/f', pfx_file_path]
        else:
            log.error('Signtool requires certificate thumbprint, name or PFX file to sign')
            raise Exception('Failure in sign_files()')
        file_list = unsigned_list
        cmd += file_list

        exit_code = None
        output = None
        exit_code, output = execute_cmd(cmd, os.path.dirname(sign_tool_path))
        log.info('Sign attempt %d exited with code %d', attempt, exit_code)
        if exit_code == 0:
            break
        else:
            if output is not None and output.find("SignTool Error: The specified timestamp server either could "
                                                  "not be reached or returned an invalid response"):
                timestamp_choice = (timestamp_choice + 1 ) % len(TIMESTAMP_URLS)
                log.info('Changing timestamp server to: ' + TIMESTAMP_URLS[timestamp_choice])
            # Remove the successfully signed files from the list
            for line in output.splitlines():
                if line.startswith('Successfully signed: '):
                    signed_file = line.split("signed: ",1)[1]
                    log.info('Removing {0}'.format(signed_file))
                    unsigned_list.remove(signed_file)
    if exit_code != 0:
        raise Exception('Failure in sign_files()')


def verify_signature_aux(args, files, sign_tool_path, sys_cat_dict=None):
    # Verify signatures
    log.info('Verifying signatures')
    for file in files:
        cat_file_path = None
        if sys_cat_dict:
            # Convert to lower case to avoid case mismatch between file name and inf entry
            file = file.lower()
            cat_file_path = sys_cat_dict.get(file, None)
        try:
            verify_signature(file, sign_tool_path, args.self_sign, cat_file_path, verbose=False)
        except:
            sys.exit(1)


def verify_signature(file_to_sign, sign_tool_path, self_sign=False, cat_file_path=None,
                     raise_exceptions=True, thumbprint=None, verbose=True):
    if verbose:
        log.info('Verifying signature for ' + file_to_sign)
    verify_switch = '/kp'
    if self_sign:
        verify_switch = '/pa'
    cmd = list()
    cmd = [sign_tool_path, 'verify',
           verify_switch
    ]
    if thumbprint:
        cmd += ['/sha1', thumbprint]
    if verbose:
        cmd += ['/v']
    cmd += [file_to_sign]

    exit_code, _ = execute_cmd(cmd, os.path.dirname(sign_tool_path), log_cmd=verbose)

    # Verify the .sys files against the .cat
    if exit_code == 0 and cat_file_path and not '.cat' in file_to_sign:
        cmd = [sign_tool_path, 'verify',
               verify_switch
        ]
        if verbose:
            cmd += ['/v']
        cmd += ['/c', cat_file_path,
                file_to_sign
        ]
        if verbose:
            log.info('Verifying %s in catalog %s', file_to_sign, cat_file_path)
        exit_code, _ = execute_cmd(cmd, os.path.dirname(sign_tool_path), log_cmd=verbose)

    if exit_code != 0 and raise_exceptions:
        raise Exception('Failure in verify_signature()')
    return exit_code


# Execute the specified command array, capturing and printing
# standard out and err and passing along the return code
def execute_cmd(cmd, cwd, log_cmd=True):
    if log_cmd:
        log.info('Working directory: %s', cwd)
        log.info('Command line: %s', ' '.join(cmd))
    with subprocess.Popen(cmd,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          cwd=cwd) as proc:
        out, error = proc.communicate()
        output = out.decode('utf8')
        log.info(output)
        return proc.returncode, output


def get_unsigned_files(all_files, sign_tool_path, thumbprint):
    # Return list of files that are not signed with provided thumbprint
    log.info('Getting list of files not signed with thumbprint %s', thumbprint)
    unsigned_files = []
    for file in all_files:
        try:
            exit_code = verify_signature(file, sign_tool_path, self_sign=True,
                                         raise_exceptions=False, thumbprint=thumbprint,
                                         verbose=False)
        except:
            sys.exit(1)
        if exit_code == 0:
            log.info('File already signed: %s', file)
        else:
            unsigned_files.append(file)
    if not unsigned_files:
        log.info('All files are already signed with thumbprint %s', thumbprint)
    return unsigned_files


def import_certificate(pfx_file_path):
    """ Import certificate to certificates store if it is not imported already """
    # Get public key thumbprint from PFX file
    log.info("PFX file path = %s", pfx_file_path)
    log.info('+++++ Getting public key thumbprint from PFX file +++++')

    if 'intel' in os.environ['USERDNSDOMAIN'].lower():
        cmd = ['powershell',
            '(Get-PfxCertificate',
            '-FilePath', pfx_file_path,
            ').Thumbprint']
        exit_code, pfx_thumbprint = execute_cmd(cmd, os.getcwd(), log_cmd=False)
    else:
        log.error('System is not in Intel domain')
    if exit_code or not pfx_thumbprint:
        log.error('Failed to get public key thumbprint from %s', pfx_file_path)
        raise Exception('Failure in import_certificate()')
    pfx_thumbprint = pfx_thumbprint.strip()
    log.info('Public key thumbprint for %s is %s', pfx_file_path, pfx_thumbprint)

    # Get thumbprints for keys from LocalMachine\Root certificates store
    log.info('+++++ Getting thumbprints for keys from LocalMachine\Root certificates store +++++')
    cmd = ['powershell',
           '(Get-ChildItem',
           '-Path', 'Cert:\\LocalMachine\\root).Thumbprint'
    ]
    exit_code, root_keys_thumbprints = execute_cmd(cmd, os.getcwd(), log_cmd=False)
    if exit_code or not root_keys_thumbprints:
        log.error('Failed to get thumbprints for keys from from LocalMachine\Root certificates store')
        raise Exception('Failure in import_certificate()')

    # Verify if PFX file thumbprint is already imported to LocalMachine\Root certificates store
    log.info('+++++ Looking for PFX file thumbprint in LocalMachine\Root certificates store +++++')
    if pfx_thumbprint in root_keys_thumbprints:
        log.info ('PFX thumbprint %s is already imported in LocalMachine\Root certificates store', pfx_thumbprint)
    else:
        # Import PFX file thumbprint to LocalMachine\Root certificates store
        log.info ('PFX thumbprint %s is not imported in LocalMachine\Root certificates store', pfx_thumbprint)
        log.info('+++++ Importing PFX file thumbprint to LocalMachine\Root certificates store +++++')
        cmd = ['powershell',
               'Import-PfxCertificate',
               '-FilePath', pfx_file_path,
               '-CertStoreLocation', 'Cert:\\LocalMachine\\Root'
        ]

        exit_code, cmd_output = execute_cmd(cmd, os.getcwd(), log_cmd=False)
        if exit_code:
            if 'Access denied' in cmd_output:
                log.error("Access to certificates store is denied, please execute with admin privileges")
            log.error('Failed to import PFX file thumbprint to LocalMachine\Root certificates store')
            raise Exception('Failure in import_certificate()')
        log.info ('PFX thumbprint %s has been imported to LocalMachine\Root certificates store', pfx_thumbprint)
    return pfx_thumbprint

sys.exit(main(sys.argv[1:]))
