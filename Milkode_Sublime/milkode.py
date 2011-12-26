# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import subprocess


class MilkGrepNewFileCommand(sublime_plugin.WindowCommand):
    def panel_search_done(self, str):
        pipe = subprocess.Popen('gmilk -a ' + str, shell=True, stdout=subprocess.PIPE).stdout
        results = unicode(pipe.read(), 'cp932')
        pipe.close()
        newv = self.window.new_file()
        newv.set_name('gmilk result')
        newv.set_syntax_file('Packages/Milkode_Sublime/gmilk Results.tmLanguage')
        newv.set_scratch(True)
        e = newv.begin_edit()
        # print results
        newv.insert(e, 0, results)
        newv.end_edit(e)

    def panel_dummy0(self):
        pass

    def panel_dummy(self, str):
        pass

    def run(self):
        defval = self.window.active_view().substr(self.window.active_view().sel()[0])
        self.window.show_input_panel('gmilk: ', defval, self.panel_search_done, self.panel_dummy, self.panel_dummy0)


class MilkGrepCommand(sublime_plugin.WindowCommand):
    def panel_done(self, picked):
        if picked != -1:
            newv = self.window.open_file(self.lines[picked][1], sublime.ENCODED_POSITION)
            lnum = self.lines[picked][1].split(':')[-1]
            pt = newv.text_point(int(lnum) - 1, 0)
            newv.sel().clear()
            newv.sel().add(sublime.Region(pt))

    def panel_search_done(self, str):
        pipe = subprocess.Popen('gmilk -a ' + str, shell=True, stdout=subprocess.PIPE).stdout
        lists = pipe.readlines()
        pipe.close()
        self.lines = []
        for line in lists:
            l = unicode(line.lstrip().rstrip(), 'cp932')
            if l == '':
                continue
            tempList = l.split(':')
            fst = ''
            scd = ''
            if tempList[1].isdigit():
                fst = (':').join(tempList[:2])
                scd = (':').join(tempList[2:])
            elif tempList[2].isdigit():
                fst = (':').join(tempList[:3])
                scd = (':').join(tempList[3:])
            self.lines.append([scd, fst])
        self.window.show_quick_panel(self.lines, self.panel_done)

    def panel_dummy0(self):
        pass

    def panel_dummy(self, str):
        pass

    def run(self):
        defval = self.window.active_view().substr(self.window.active_view().sel()[0])
        self.window.show_input_panel('gmilk: ', defval, self.panel_search_done, self.panel_dummy, self.panel_dummy0)
