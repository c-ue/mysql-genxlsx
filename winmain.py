import time
import tkinter as tk

import xlsxwriter as xl

import mysql as ms


class win(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.ui()
    def ui(self):
        self.UserLabel = tk.Label(self)
        self.UserLabel['text'] = "User"
        self.UserLabel.grid(row=0, column=0)

        self.UserEntry = tk.Entry(self)
        self.UserEntry['width'] = 10
        self.UserEntry.grid(row=0, column=1)

        self.PasswdLabel = tk.Label(self)
        self.PasswdLabel['text'] = "Password"
        self.PasswdLabel.grid(row=1, column=0)

        self.PasswdEntry = tk.Entry(self)
        self.PasswdEntry['width'] = 10
        self.PasswdEntry.grid(row=1, column=1)

        self.UnitLabel = tk.Label(self)
        self.UnitLabel['text'] = "Per Cycle Time(sec)"
        self.UnitLabel.grid(row=2, column=0)

        self.UnitTime = tk.Entry(self)
        self.UnitTime['width'] = 10
        self.UnitTime.grid(row=2, column=1)

        self.UntilLabel = tk.Label(self)
        self.UntilLabel['text'] = "Until(hh:mm)"
        self.UntilLabel.grid(row=3, column=0)

        self.UntilTime = tk.Entry(self)
        self.UntilTime['width'] = 10
        self.UntilTime.grid(row=3, column=1)

        self.StartBtn = tk.Button(self)
        self.StartBtn['text'] = "Start"
        self.StartBtn.grid(row=4, column=0, columnspan=2)
        self.StartBtn['command'] = self.Start

        self.Msg = tk.Label(self)
        self.Msg['text'] = ""
        self.Msg.grid(row=5, column=0,columnspan=2)

    def Start(self):
        user=self.UserEntry.get()
        passwd=self.PasswdEntry.get()
        UnitTime = self.UnitTime.get()
        Until=self.UntilTime.get()
        if not (UnitTime !='' and UnitTime.isdigit() and Until !='' and len(Until.split(':')) == 2 and
                Until.split(':')[0].isdigit() and Until.split(':')[1].isdigit() and
                0 <= int(Until.split(':')[0]) < 24 and 0 <= int(Until.split(':')[1]) < 59 and
                user !='' and passwd !='' ):
            self.Msg['text'] = 'Field Empty.'
            return False
        UnitTime = int(UnitTime)
        Until=int(Until.split(':')[0])*60+int(Until.split(':')[1])
        msobj=ms.core(user=user,passwd=passwd)
        if msobj.error is not None:
            self.Msg['text'] = msobj.error
            return
        TeamList = msobj.GetAllTeamName()
        if not TeamList:
            self.Msg['text'] = msobj.error
            return False
        f = xl.Workbook('./Score-Log.xlsx')
        sheet = f.add_worksheet('page 1')
        for i in range(len(TeamList)):
            sheet.write(i + 1, 0, TeamList[i]['teamname'])
        i = 1
        while True:
            if int(time.strftime("%H")) * 60 + int(time.strftime("%M")) >= Until:
                break
            sheet.write(0, i, time.asctime())
            for j in range(len(TeamList)):
                score = msobj.GetTotalScoreByTid(tid=TeamList[j]['teamid'])
                sheet.write(j + 1, i, score[0]['totalscore'])
            i += 1
            time.sleep(UnitTime)
        f.close()
        return

def main():
    global root
    root = tk.Tk()
    xwin = win(master=root)
    xwin.mainloop()

if __name__ == '__main__':
    main()