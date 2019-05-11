from visidata import Sheet, ColumnItem, asyncthread, globalCommand, ENTER
import vgit


class GitGrep(vgit.GitSheet):
    rowtype = 'results' # rowdef: list(file, line, line_contents)
    columns = [
        ColumnItem('filename', 0),
        ColumnItem('linenum', 1),
        ColumnItem('line', 2),
    ]
    @asyncthread
    def reload(self):
        self.rows = []
        for line in self.git_lines('grep', '--no-color', '-z', '--line-number', '--ignore-case', self.regex):
            self.addRow(line.split('\0'))


Sheet.unbindkey('g/')
globalCommand('g/', 'git-grep', 'rex=input("git grep: "); vd.push(GitGrep(rex, regex=rex, source=sheet))', 'find in all files in this repo'),

GitGrep.addCommand(ENTER, 'dive-row', 'vs=GitFileSheet(cursorRow[0]); vs.cursorRowIndex=int(cursorRow[1])-1; vd.push(vs).reload()', 'go to this match')
GitGrep.addCommand('^O', 'sysopen-row', 'launchExternalEditorPath(Path(cursorRow[0]), linenum=cursorRow[1]); reload()', 'open this file in $EDITOR')