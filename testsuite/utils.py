import subprocess
import sys
from pathlib import Path


def shell_cmd(cmd, lowarn=False):
    p = subprocess.Popen(cmd,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         universal_newlines=True)
    out, err = p.communicate()
    print(str(out))
    print(str(err))

    return p.returncode, (str(out) + str(err))


def file_exists(path_file):
    if not path_file.is_file():
        sys.exit('The file ' + str(path_file) + ' was not created')


def co_flag(plot_name):
    status, _ = shell_cmd('python ' + plot_name + '/' + plot_name + '.py -co')
    assert status == 0, 'The -co flag does not work'


def plotting(plot_name, config_files, input_files):
    output_dir = 'testsuite/output'
    for i in range(0, len(config_files)):
        for j in range(0, len(input_files)):
            output_file = plot_name + '_' + config_files[
                i] + '_' + input_files[j] + '.png'
            output_dir_file = Path(output_dir, output_file)
            output_dir_file.unlink(missing_ok=True)
            cmd = 'python ' + plot_name + '/' + plot_name + '.py -d ' + output_dir + ' -o ' + output_file +\
                    ' -c testsuite/configs/' + config_files[i] + '.ini -i data/' + input_files[j] + '.nc'
            status, _ = shell_cmd(cmd)
            assert status == 0, 'Failed with config ' +\
                    config_files[i] + ' and input file ' + input_files[j]

            file_exists(output_dir_file)
