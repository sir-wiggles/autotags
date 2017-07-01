import json
import os
import subprocess

import neovim


@neovim.plugin
class Main(object):
    def __init__(self, vim):
        self.vim = vim
        self.snooper_rule_file = self.vim.vars.get("snooper_rule_file", ".snooper")
        self.snooper_ctags_bin = self.vim.vars.get("snooper_ctags_bin", "ctags")

    def get_packages(self):
        try:
            with open(self.snooper_rule_file, 'r') as f:
                data = f.read()
        except FileNotFoundError:
            data = '[]'
        rules = json.loads(data)
        packages = []
        for rule in rules:
            dir = rule.get("directory", None)
            if dir is None:
                continue
            pkg = rule.get("packages", [""])
            packages.extend(list(map(lambda p: os.path.join(dir, p), pkg)))
        return packages

    @neovim.command('SnooperUpdate')
    def update(self):
        cmd = self.snooper_ctags_bin + " ".join(self.get_packages())
        self.vim.command("echo '%s'" % cmd)
        subprocess.run(cmd, shell=True)

