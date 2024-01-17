import customtkinter as ctk
from ctypes import windll, byref, sizeof, c_int

class TopLevel(ctk.CTkToplevel):
    def __init__(self,text,):
        super().__init__()
        self.geometry('200x100+800+400')
        self.resizable(False,False)
        self.attributes("-topmost", 1)
        

        self.label = ctk.CTkLabel(self,text=f'{text} wins the game',font=('Helvetica', 18))
        self.label.pack(padx=20, pady=20)

        self.button = close_button(self,self.func,)
        self.wait_window(self)
      
    def func(self):
        
        self.destroy()
    
class close_button(ctk.CTkButton):
    def __init__(self,parent,func,):
        super().__init__(
            parent,
            width=5,
            text='close',
            font=('Helvetica', 18),
            command=func
        )
        self.place(relx=0.67,rely=0.67)

class Tik(ctk.CTk):
    def __init__(self,title,size):
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0],size[1])
        # self.title_bar()

        #layouts
        self.rowconfigure((0,1,2),weight=1,uniform='a')
        self.columnconfigure((0,1,2,3,4),weight=1,uniform='a')

        #data
        self.turn="X"

        self.buttons=[[None] * 3 for _ in range(3)]

        self.create()
        
        self.turn_display=label(self,self.turn)
        self.reset_btn=ctk.CTkButton(self,text='RESET',command=self.RESET).grid(row=1,column=3,columnspan=2,sticky='ew',padx=20)

        self.mainloop()

    def title_bar(self):
        HWND  =windll.user32.GetParent(self.winfo_id())
        title_color  =0x242424
        windll.dwmapi.DwmSetWindowAttribute(HWND,35,byref(c_int(title_color)),sizeof(c_int))

    
    def create(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]=button(self,i,j,self.play)
                self.buttons[i][j].grid(row = i,column=j,padx=0.5,pady= 0.5,sticky='nsew')
        # display turn

    def play(self,row,col):
        self.buttons[row][col].configure(text=self.turn)
        self.buttons[row][col].configure(state='disabled')
        self.check_win(row,col)
        self.switch_turn()
        self.turn_display.configure(text=self.turn)

    def check_win(self,row,col):
        if all([self.buttons[row][c].cget("text")==self.turn for c in range(3)]):
            self.winerr()

        if all([self.buttons[r][col].cget("text")==self.turn for r in range(3)]):
            self.winerr()
        
        if all([self.buttons[r][r].cget("text") == self.turn for r in range(3)]):
            self.winerr()
        
        if row+col==2:
            if all([self.buttons[r][2-r].cget("text") == self.turn for r in range(3)]):
                self.winerr()

    def winerr(self,):
        # messagebox.showinfo('WINNER',f'{self.turn} wins the game')
        self.disable_game()
        TopLevel(self.turn)
        # self.grab_set()

        pass

    def disable_game(self):    
        [self.buttons[i][j].configure(state = "disabled")for i in range(3) for j in range(3)]

    def enable_game(self):
        [self.buttons[i][j].configure(state = "enabled")for i in range(3) for j in range(3)]

    def switch_turn(self):
        self.turn = "X" if self.turn=="O" else "O"
    
    def RESET(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].configure(text=" ")
        self.enable_game()                

class button(ctk.CTkButton):
    def __init__(self,parent,row,col,func,text=" "):
        
        super().__init__(
            parent,
            font=ctk.CTkFont(family='Helvetica',size=70),
            text=text,
            corner_radius=0,
            command=lambda: func(row,col))

class label(ctk.CTkLabel):
    def __init__(self,parent,text):
        super().__init__(parent,text=text,font=ctk.CTkFont(family='Helvetica',size=70))
        self.grid(row = 0,column= 3,columnspan=2,)

size=(500,300)
title="Tic Tac Toe"

if __name__=='__main__':
    Tik(title,size)
