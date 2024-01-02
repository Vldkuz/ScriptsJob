import os
import re
import sys
from pathlib import Path
from GitManager import GitManager
from WebWorker import WebWorker


class CheckRefsWorker:
    def __init__(self, directory=os.getcwd(), verbose=False, out_stream=sys.stdout):
        self.verbose = verbose
        if self.check_dir(directory):
            self.directory = directory
            os.chdir(self.directory)
        else:
            raise FileNotFoundError("Directory does not exist")
        self.out = out_stream

    def change_verbose(self, verbose):
        self.verbose = verbose

    def change_out(self, file):
        self.out = file

    def check_content_refs(self, url_repo, branch):
        with GitManager(url_repo, branch):
            for sample in os.walk(self.directory):
                files = filter(lambda x: Path(x).suffix == '.md', sample[2])
                for file in files:
                    self.check_refs_file(file, sample[0])
            print('All refs checked', file=self.out)

    def check_local_aliases(self, url_repo, branch):
        with GitManager(url_repo, branch):
            yaml_file = self.get_files_by_suffix('.yaml')[0]
            count_rows = 1

            with open(yaml_file, 'r', buffering=True, encoding='utf-8') as files:
                for line in files:
                    count_rows += 1

                    ref_file = line[line.rfind(":") + 2: -1]

                    if len(ref_file) == 0:
                        continue

                    if not os.path.exists(ref_file):
                        print(f'No such file: {ref_file}', f'row = {count_rows}', file=self.out)

    def check_web_aliases(self, url, url_repo, version, official):
        with GitManager(url_repo, version):
            if official:
                url_to_check = f'{url}/v/{version}/'
            else:
                url_to_check = url
            web = WebWorker(url_to_check)
            excepts = ['structure', 'readme', 'summary', 'redirects']
            regex__alias = re.compile(r'([a-z].*):')
            yaml_file = self.get_files_by_suffix('.yaml')[0]
            count_rows = 0

            with open(yaml_file, 'r', buffering=True, encoding='utf-8') as file:
                for line in file:
                    count_rows += 1

                    if line == '\n':
                        continue

                    alias_obj = re.search(regex__alias, line)

                    if alias_obj:
                        alias = alias_obj.group(1)

                        if alias in excepts:
                            continue

                        if web.check_alias(alias):
                            if self.verbose:
                                text = f'{alias}: Success'
                                print(text, file=self.out)
                        else:
                            text = f'{alias}: Failure'
                            print(text, file=self.out)

                    else:
                        print(f'row:{count_rows}, {line}', file=self.out)
                        raise Exception(alias_obj)
                print('All aliases checked', file=self.out)

    @staticmethod
    def get_files_by_suffix(suffix):
        return list(filter(lambda x: Path(x).suffix == suffix, os.listdir(os.getcwd())))

    @staticmethod
    def check_dir(directory):
        return os.path.exists(directory)

    @staticmethod
    def get_refs(file):
        with open(file, 'r', buffering=True, encoding='utf-8') as content:
            text = content.read()
            regex_refs = re.compile(r'\]\(|img .*src=\"')
            refs = regex_refs.finditer(text)

        clear_refs = []

        for ref in refs:
            raw_ref = ref.group()

            if raw_ref[0] == ']':
                start_ref = ref.end() + 1  # Будем резать от скобки до ближайшей правой скобки
                end_ref = text.find(')', start_ref)
                clear_refs.append(text[start_ref - 1:end_ref])
            elif raw_ref[0] == 'i':
                start_ref = ref.end() + 1  # В конце регвыра всегда будет кавычка
                end_ref = text.find(r'"', start_ref)  # Будем резать до ближайшей кавычки правой
                clear_refs.append(text[start_ref - 1:end_ref])
            else:
                print(f'Что-то с ссылкой: {raw_ref}')

        return iter(clear_refs)

    def check_refs_file(self, file, directory):
        last = os.getcwd()
        os.chdir(directory)
        ok_flag = True

        for ref in CheckRefsWorker.get_refs(file):
            if ref.startswith('http'):
                if not WebWorker.check_ref(ref) or WebWorker.check_ref_forbidden(ref):
                    text = f'{last + os.sep + file}: Failure'
                    print(text, ref, file=self.out)
                    ok_flag = False
            else:
                if ref.count("#") > 0:
                    idx_rs = ref.find("#")
                    ref = ref[:idx_rs]
                    if len(ref) == 0:
                        continue

                if not os.path.exists(ref):
                    text = f'{last + os.sep + file}, {ref} : Failure'
                    print(text, file=self.out)
                    ok_flag = False

        if ok_flag and self.verbose:
            text = f"{last + os.sep + file}: Success"
            print(text, file=self.out)
        os.chdir(last)
