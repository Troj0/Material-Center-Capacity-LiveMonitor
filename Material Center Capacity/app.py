from tkinter import *
import tkinter.messagebox
import customtkinter
from shelves import buttonPositionsM, buttonPositionsA_to_L
from query import *
import sched, time

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("KhPD MC Capacity")
        self.geometry(f"{1920}x{1024}")

       # self.grid_columnconfigure(0, weight=1)
       # self.grid_columnconfigure((15, 18, 21, 27, 30, 33, 36, 39, 42, 45, 48), weight=1)
        #self.grid_rowconfigure((0), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=10)
        self.sidebar_frame.grid(row=30, column=0, columnspan=50, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Menu", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=30, column=4, padx=20, pady=(0, 0))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Query", command=materialQuery)
        self.sidebar_button_1.grid(row=30, column=5, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Update", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=30, column=6, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="future", command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=30, column=7, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=30, column=8, padx=10, pady=(10, 10))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=30, column=9, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=30, column=10, padx=10, pady=(10, 10))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["70%", "80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=30, column=11, padx=10, pady=(10, 10))

        self.radio_var = tkinter.IntVar(value=0)
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")

        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        
        #Labels
        labelCount = range(1, 13)
        labelTexts = ['M', 'L', 'K', 'J', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']

        for i in labelCount:
            self.label = customtkinter.CTkLabel(self, text=labelTexts[i-1], font=customtkinter.CTkFont(size=20, weight="bold"))
            self.label.grid(row=0, column=i, padx=0, pady=(0, 0))
        
        # Frames
        # M Frame
        self.frame_M = customtkinter.CTkFrame(self, corner_radius=10, fg_color="grey")
        self.frame_M.grid(row=1, column=1, rowspan=24, padx=1, pady=5)
        
        # Other Frames
        frameCount = range(2, 13)
        frames = []  # Create an empty list to store the frame objects

        # Create the frames and store them in the list
        for i in frameCount:
            frame = customtkinter.CTkFrame(self, corner_radius=10, fg_color="grey")
            frame.grid(row=1, column=i, rowspan=24, padx=1)
            frames.append(frame)
            
        # Buttons
        buttonSuffix = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]
        ## A to L
        buttonNumbers = ['01', '02', '03', '06', '07', '08']
        noOfGeneratedLists = range(1, 528)
        buttonTexts = "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L"
        buttonListA_to_L = []
        
        for rep in range(len(buttonNumbers)):
            for suffix in buttonSuffix:
                for buttonText in buttonTexts:
                    buttonListA_to_L.append(buttonText + buttonNumbers[rep] + suffix)
                
        # Sort the button list based on the dictionary values
        sortedButtonPositionsA_to_L = sorted(buttonListA_to_L, key=lambda x: buttonPositionsA_to_L[x])
        self.aToLButtons = []
        for i, buttonName in enumerate(sortedButtonPositionsA_to_L):
            row = buttonPositionsA_to_L[buttonName][1]
            column = buttonPositionsA_to_L[buttonName][0]
            frame_index = 1
            # Adjust the column index to matchprint(existCount) the frame index in the list
            if buttonName.startswith('L') == True: frame_index = 0
            elif buttonName.startswith('K') == True: frame_index = 1
            elif buttonName.startswith('J') == True: frame_index = 2
            elif buttonName.startswith('H') == True: frame_index = 3
            elif buttonName.startswith('G') == True: frame_index = 4
            elif buttonName.startswith('F') == True: frame_index = 5
            elif buttonName.startswith('E') == True: frame_index = 6
            elif buttonName.startswith('D') == True: frame_index = 7
            elif buttonName.startswith('C') == True: frame_index = 8
            elif buttonName.startswith('B') == True: frame_index = 9
            elif buttonName.startswith('A') == True: frame_index = 10
            frame = frames[frame_index]
            fgColor = colorOnContents(buttonName)
            prefixGroup = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L"]
            DictExist = {buttonText: 0 for buttonText in buttonTexts}
            DictNonExist = {buttonText: 0 for buttonText in buttonTexts}

            buttonPrefix = ''
            for prefix in prefixGroup:
                if buttonName.startswith(prefix):
                    buttonPrefix = prefix
                    break

            if(locationUsed):
                DictExist[buttonPrefix] =+ 1
            else:
                DictNonExist[buttonPrefix] =+ 1
            
            button = customtkinter.CTkButton(frame, text=buttonName, command=lambda btn=buttonName: locationButtonOnClick(btn), fg_color=fgColor, width=2)
            button.grid(row=row, column=column, padx=5, pady=13, sticky="nsew")
            self.aToLButtons.append(button)
        print(DictExist, DictNonExist)
        ## M
        buttonTextsM = "M"
        buttonNumbersM = ['01', '02', '03', '04', '05', '06', '07', '08']
        buttonList_M = []
        
        for rep in range(len(buttonNumbersM)):
            for suffix in buttonSuffix:
                buttonList_M.append(buttonTextsM + buttonNumbersM[rep] + suffix)

        
        # Sort the button list based on the dictionary values
        sortedButtons_M = sorted(buttonList_M, key=lambda x: buttonPositionsM[x])
        self.mButtons = []
        for i, buttonName in enumerate(sortedButtons_M):
            row = buttonPositionsM[buttonName][1]
            column = buttonPositionsM[buttonName][0]
            fgColor = colorOnContents(buttonName)
            if buttonName == "M01A1":
                button = customtkinter.CTkButton(self.frame_M, text=buttonName, command=lambda btn=buttonName: self.buttonStatusUpdate(), fg_color=fgColor, width=2)
                button.grid(row=row, column=column, padx=5, pady=4, sticky="nsew")
            else:
                button = customtkinter.CTkButton(self.frame_M, text=buttonName, command=lambda btn=buttonName: locationButtonOnClick(btn), fg_color=fgColor, width=2)
                button.grid(row=row, column=column, padx=5, pady=4, sticky="nsew")
            self.mButtons.append(button)

    def activate_progress_bar_event(self):
        self.progressbar_1 = customtkinter.CTkProgressBar(self)
        self.progressbar_1.grid(row=6, column=1, columnspan=3, padx=(20, 10), pady=(5, 5), sticky="nsew")
        self.progressbar_1.configure(mode="indeterminnate")

        self.progressbar_1.start()

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print(("CTkInputDialog:", dialog.get_input()))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self, btn):
        print(btn)
    

    def buttonStatusUpdate(self):
        for b in self.aToLButtons:
            
            fgColor = colorOnContents(b.cget("text"))
            b.configure(fg_color = fgColor)
        for b in self.mButtons:
            
            fgColor = colorOnContents(b.cget("text"))
            b.configure(fg_color = fgColor)
    
if __name__ == "__main__":
    app = App()
    app.mainloop()
    

