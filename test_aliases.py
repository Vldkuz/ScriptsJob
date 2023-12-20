import argparse
import os.path
import sys
import urllib.request
import re
from http import HTTPStatus
from os import path
from pathlib import Path
from urllib.error import URLError, HTTPError

def check_refs_file(file, dir, out):
    last = os.getcwd()
    os.chdir(dir)
    sample = os.getcwd()
    ok_flag = True

    for ref in get_refs(file):

        if ref.startswith('http'):
            if not check_web_ref(ref):
                text = "\033[31m{}".format(f'{sample + os.sep + file}: Failure')
                print(text, ref, file = out)

                ok_flag = False
        else:
            if ref.count("#") > 0:
                idx_rs = ref.find("#")
                ref = ref[:idx_rs]
                if len(ref) == 0:
                    continue

            if not path.exists(ref):
                text = "\033[31m{}".format(f'{sample + os.sep + file}, {ref} : Failure')
                print(text, file = out)
                ok_flag = False
    if ok_flag:
        text = "\033[32m{}".format(f"{sample + os.sep + file}: Success")
        print(text, file = out)
    os.chdir(last)


def check_all_refs(root_dir, out):
    all_dirs = os.walk(root_dir)
    for sample in all_dirs:
        files_dir = sample[2]
        files_dir = list(filter(lambda file: Path(file).suffix == '.md', files_dir))
        for file in files_dir:
            check_refs_file(file, sample[0], out)
    print("All refs checked", file=out)


def get_refs(file):
    refs = None
    with open(file,'r', buffering=True, encoding='utf-8') as content:
        text = content.read()
        regex_refs = re.compile(r'\]\(|img .*src=\"')
        refs = regex_refs.finditer(text)

    clear_refs = []

    if refs is None:
        return iter(clear_refs)

    for ref in refs:
        raw_ref = ref.group()

        if raw_ref[0] == ']':
            start_ref = ref.end() + 1 # Будем резать от скобки до ближайшей правой скобки
            end_ref = text.find(')', start_ref)
            clear_refs.append(text[start_ref - 1 :end_ref])
        elif raw_ref[0] == 'i':
            start_ref = ref.end()+1 # В конце регвыра всегда будет кавычка
            end_ref = text.find(r'"', start_ref) # Будем резать до ближайшей кавычки правой
            clear_refs.append(text[start_ref-1:end_ref])
        else:
            print("Что-то с ссылкой")

    return iter(clear_refs)

def check_refs_yaml(file_yaml, out):
    count_rows = 1
    dir_idx = file_yaml.rfind('/')
    file = file_yaml
    if dir_idx != -1:
        cur_dir = os.getcwd()
        dir = file_yaml[:dir_idx]
        file = file_yaml[dir_idx + 1:]
        os.chdir(dir)

    with open(file, 'r', buffering=True, encoding='utf-8') as files:
        for line in files:
            count_rows += 1

            ref_file = line[line.rfind(":") + 2: -1]

            if len(ref_file) == 0:
                continue


            if not os.path.exists(ref_file):
                print(f'No such file: {ref_file}', f'row = {count_rows}', file=out)

    os.chdir(cur_dir)

def check_web_ref(ref):
    header = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
              'Accept-Encoding': 'none',
              'Accept-Language': 'en-US,en;q=0.8',
              'Connection': 'keep-alive'}

    request = urllib.request.Request(ref, headers=header)

    # Эти сайты содержат капчу, которую не представляется возможным обойти


    try:
        resp = urllib.request.urlopen(request)
        resp_code = resp.getcode()
    except HTTPError as e:
        if e.code == 403:
            return True
        resp_code = HTTPStatus.NOT_FOUND
    except BaseException:
        resp_code = HTTPStatus.NOT_FOUND

    return resp_code==HTTPStatus.OK



def check_aliases(file_yaml, version, out):
    url = f'https://docs.ideco.dev/v/{version}/'
    excepts = ['structure', 'readme', 'summary', 'redirects']
    regex__alias = re.compile(r'([a-z].*):')
    count_rows = 1

    with open(file_yaml, 'r', buffering=True, encoding='utf-8') as file:
        for line in file:
            count_rows += 1

            if line == '\n':
                continue

            alias_obj = re.search(regex__alias, line)

            if alias_obj:
                alias = alias_obj.group(1)

                if alias in excepts:
                    continue

                if check_web_ref(url+alias):
                    text = f'{alias}: Success'
                    print("\033[32m{}".format(text), file = out)
                else:
                    text = f'{alias}: Failure'
                    print("\033[31m{}".format(text), file = out)

            else:
                print(f'row:{count_rows}, {line}', file = out)
                raise Exception(alias_obj)




# -cr - check refs -ca-check aliases
# -h - help
def main():
    description_text = "Help check-aliases and refs_aliases"
    help_text = description_text + "\n" + 'For checking refs - -cr, --check_refs' + "\n" + 'For checking aliases - -ca, --check_aliases'

    parser = argparse.ArgumentParser(add_help=True, description=help_text, epilog="DocHelperScripts",)

    parser.add_argument('-cr', '--check_refs', action='store_true')
    parser.add_argument('-ca', '--check_aliases', action='store_true')
    parser.add_argument('-C', '--check_all_refs', action='store_true')
    parser.add_argument('-D', '--directory', action='store_true')
    parser.add_argument('-f', '--file', action='store_true')
    args, unknown = parser.parse_known_args()

    out_file = sys.stdout

    if args.file:
        parser.add_argument('out_file', type=str, help='File to output')
        args, unknown = parser.parse_known_args()
        out_file = open(args.out_file, 'w')
    if args.directory:
        parser.add_argument('dir', type=str, help='Directory to change', default=os.getcwd())
        args, unknown = parser.parse_known_args()
        os.chdir(args.dir)
    if args.check_refs:
        parser.add_argument('file_with_refs', type=str, help='file with refs in current directory', default=None)
        args, unknown = parser.parse_known_args()

        if not args.file_with_refs:
            print("Укажите файл с ссылками")
            sys.exit(-1)

        rslash = args.file_with_refs.find('/')
        sample = args.file_with_refs[:rslash]
        args.file_with_refs = args.file_with_refs[rslash+1:]

        check_refs_file(args.file_with_refs, sample, out_file)
    if args.check_aliases:
        parser.add_argument('file_yaml', type=str, help='file with aliases in current directory', default=None)
        parser.add_argument('version_doc', type=str, help='Version of documentation')
        args, unknown = parser.parse_known_args()

        if not (args.file_yaml and args.version_doc):
            print("Укажите файл yaml или версию документации")
            sys.exit(-1)

        check_refs_yaml(args.file_yaml, out_file)
        check_aliases(args.file_yaml, args.version_doc, out_file)
    if args.check_all_refs:
        parser.add_argument('start_dir', type=str, help='Starting directory for checking all refs', default=os.getcwd())
        args, unknown = parser.parse_known_args()
        if not args.start_dir:
            print("Укажите стартовую директорию")
            sys.exit(-1)

        check_all_refs(args.start_dir, out_file)

    out_file.close()


if __name__ == '__main__':
    main()
