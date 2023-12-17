import argparse
import os.path
import urllib.request
import re
from http import HTTPStatus

def check_all_refs(root_dir):


def get_refs(file):
    # Получает все ссылки с документа


def check_refs_yaml(file_yaml):
    count_rows = 1

    with open(file_yaml, 'r', buffering=True) as file:
        for line in file:
            count_rows += 1

            if line == '\n':
                continue

            ref_file = line[line.find(" "):]

            if not os.path.exists(ref_file):
                print(f'No such file: {ref_file}', f'row = {count_rows}')


def check_aliases(file_yaml, version):
    url = f'https://docs.ideco.dev/v/{version}/'
    excepts = ['structure', 'readme', 'summary', 'redirects']
    regex__alias = re.compile(r'([a-z].*):')
    count_rows = 1

    header = {'User-Agent': 'Mozilla/5.0'}

    with open(file_yaml, 'r', buffering=True) as file:
        for line in file:
            count_rows += 1

            alias_obj = re.search(regex__alias, line)

            if alias_obj:
                alias = alias_obj.group(1)

                if alias in excepts:
                    continue

                request = urllib.request.Request(url + alias, headers=header)

                try:
                    resp = urllib.request.urlopen(request)
                    resp_code = resp.getcode()
                except BaseException as e:
                    resp_code = HTTPStatus.NOT_FOUND

                if resp_code == HTTPStatus.OK:
                    text = f'{alias}: Success'
                    print("\033[32m{}".format(text))
                else:
                    text = f'{alias}: Failure'
                    print("\033[31m{}".format(text))

            else:
                print(f'row:{count_rows}, {line}')
                raise Exception(alias_obj)


def check_refs(file_summary, version):
    ''' Регулярка на вырезку ссылок \(.*\)'''


# -cr - check refs -ca-check aliases
# -h - help
def main():
    description_text = "Help check-aliases and refs_aliases"
    help_text = description_text + "\n" + 'For checking refs - -cr, --check_refs' + "\n" + 'For checking aliases - -ca, --check_aliases'

    parser = argparse.ArgumentParser(add_help=True, description=help_text, epilog="DocHelperScripts",)

    parser.add_argument('-cr', '--check_refs', action='store_true')
    parser.add_argument('-ca', '--check_aliases', action='store_true')
    parser.add_argument('file_yaml', type=str, help='Input file with aliases')
    parser.add_argument('version_doc', type=str, help='Version of documentation')
    args = parser.parse_args()

    if args.check_refs:
        check_refs_yaml(args.file_yaml)
    if args.check_aliases:
        check_aliases(args.file_yaml, args.version_doc)

if __name__ == '__main__':
    main()
