import argparse
import urllib.request
import re
from http import HTTPStatus


def check_aliases(file_yaml, version):
    url = f'https://docs.ideco.dev/v/{version}/'
    excepts = ['structure', 'readme', 'summary', 'redirects']
    regex__alias = re.compile(r'([a-z].*):')

    header = {'User-Agent': 'Mozilla/5.0'}

    with open(file_yaml, 'r', buffering=True) as file:
        for line in file:

            if line == '\n':
                continue

            alias_obj = re.search(regex__alias, line)

            if alias_obj:
                alias = alias_obj.group(1)

                if alias in excepts:
                    continue

                request = urllib.request.Request(url + alias,headers=header)

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
                raise Exception(alias_obj)


def main():
    parser = argparse.ArgumentParser(description="DocHelperScripts")
    parser.add_argument('file_yaml', type=str, help='Input file with aliases')
    parser.add_argument('version_doc', type=str, help='Version of documentation')
    args = parser.parse_args()

    check_aliases(args.file_yaml, args.version_doc)


if __name__ == '__main__':
    main()
