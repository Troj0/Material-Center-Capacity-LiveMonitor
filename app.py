from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import customtkinter
from shelves import buttonPositionsM, buttonPositionsA_to_L
from query import *
import sched, time
from CTkTable import *
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("KhPD MC Capacity")
        self.geometry(f"{3840}x{2160}")
        rows = [31, 32]
        for i in rows:
            self.rowconfigure(i, weight=1)
        #Labels
        labelCount = range(1, 13)
        labelTexts = ['M\nReliability', 'L\nOil Train 3, 4 & 5', 'K\nOil Train 1&2', 'J\nPCU & Mech Shop', 'H\nPCU & Shipping', 'G\nGas Processing', 'F\nUtilities', 'E\nWip', 'D\nI-Field', 'C\nGaskets & General', 'B\nGeneral', 'A\nGaskets & General']

        for i in labelCount:
            self.label = customtkinter.CTkLabel(self, text=labelTexts[i-1], font=customtkinter.CTkFont(size=20, weight="bold"))
            self.label.grid(row=0, column=i, padx=0, pady=(0, 0))
        
        # Frames
        # M Frame
        self.frame_M = customtkinter.CTkFrame(self, corner_radius=10, fg_color="#40403f")
        self.frame_M.grid(row=1, column=1, rowspan=24, padx=1)
        # Other Frames
        frameCount = range(2, 13)
        self.frames = []  # Create an empty list to store the frame objects
        # Create the frames and store them in the list
        for i in frameCount:
            frame = customtkinter.CTkFrame(self, corner_radius=10, fg_color="#40403f")
            frame.grid(row=1, column=i, rowspan=24, padx=1)
            self.frames.append(frame)
        bg = buttonGenaration(self)
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=10)
        self.sidebar_frame.grid(row=100, column=0, columnspan=50, sticky="sew")
        # Needed for the developedByLabel
        #self.sidebar_frame.grid_columnconfigure(12, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Menu", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=30, column=4, padx=20, pady=(0, 0))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Query", font=customtkinter.CTkFont(size=20, weight="bold"), command=materialQuery)
        self.sidebar_button_1.grid(row=30, column=5, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Update", font=customtkinter.CTkFont(size=20, weight="bold"), command=bg.updateFunction)
        self.sidebar_button_2.grid(row=30, column=6, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Modify Location", font=customtkinter.CTkFont(size=18, weight="bold"), command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=30, column=7, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=30, column=8, padx=10, pady=(10, 10))
        self.developedBy_label = customtkinter.CTkLabel(self.sidebar_frame, text="Developed By: Muhammad Alshammari", font=customtkinter.CTkFont(size=14, weight="normal"), anchor="w")
        self.developedBy_label.grid(row=30, column=13, padx=10, pady=(10, 10))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=30, column=9, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=30, column=10, padx=10, pady=(10, 10))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["70%", "80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=30, column=11, padx=10, pady=(10, 10))
        self.radio_var = tkinter.IntVar(value=0)
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("80%")
        customtkinter.set_widget_scaling(80 / 100)
        # # CTkTable
        # headerTexts = ["Material Number","Material Description","UoM","QTY","Area", "Location"]
        # values = [
        #  [1,2,3,4,5,6],
        #  [1,2,3,4,5,6],
        #  [1,2,3,4,5,6]
        #  ]
        # for rep, text in range(len(headerTexts)), headerTexts:
        #     table = CTkTable(master=self, row=5, column=6)
        #     table.insert(row=rep, value=text)
        # table.grid( row=31, column=1, columnspan=50, padx=10, pady=(10, 10), sticky="nsew")
        existPercentage = int(bg.existCount / 528 * 100)
        nonExistPercentage = int(bg.nonExistCount / 528 * 100)
        barPercentageNonExist = int(nonExistPercentage / 2) # for now equals 27
        barPercentageExist = int(50 - barPercentageNonExist) # for now equals 23
        #print(existPercentage, nonExistPercentage, barPercentageNonExist, barPercentageExist)
        #Statistics Containers
        footerContainer = customtkinter.CTkFrame(self, corner_radius=10, fg_color="#40403f")
        
        # self.container_M = customtkinter.CTkFrame(self, corner_radius=10, fg_color="#40403f")
        # self.container_M.grid(row=32, column=1, padx=1, sticky='ew')

        # containerCount = range(2, 13)
        # self.containers = []  
        # for i in containerCount:
        #     container = customtkinter.CTkFrame(self, corner_radius=10, fg_color="#40403f")
        #     container.grid(row=32, column=i, padx=1, sticky='ew')
        #     self.containers.append(frame)

        for i in range(1, 50):
            footerContainer.columnconfigure(i, weight=1)
        
        #footerContainer.rowconfigure(1, weight=1)
        footerContainer.grid(row=34, column=1, columnspan=50, sticky='nsew', padx=(2, 2), pady=(5, 5))
        OverallUsedFrame = customtkinter.CTkFrame(footerContainer, corner_radius=10, fg_color="#135958")
        OverallUsedFrame.grid(row=2, column=1, columnspan=barPercentageNonExist, sticky='ew')
        OverallUsedFrame2 = customtkinter.CTkFrame(footerContainer, corner_radius=10, fg_color="#87302f")
        OverallUsedFrame2.grid(row=2, column=barPercentageNonExist, columnspan=barPercentageExist, sticky='ew',)
        # OverallUsedFrame3 = customtkinter.CTkFrame(footerContainer, corner_radius=10, fg_color="#40403f")
        # OverallUsedFrame3.grid(row=33, column=1, columnspan=2,  sticky='ew', padx=(20, 5), pady=(5, 5))
        #Overall Labels
        
        percentageLabel = customtkinter.CTkLabel(OverallUsedFrame, text='  Available Shelves ', font=customtkinter.CTkFont(size=16))
        percentageLabel2 = customtkinter.CTkLabel(OverallUsedFrame, text='{} {}%'.format(bg.nonExistCount, nonExistPercentage), font=customtkinter.CTkFont(size=24, weight="bold"))
        percentageLabel.grid(row=1, column=1)
        percentageLabel2.grid(row=2, column=1)
        percentageLabel3 = customtkinter.CTkLabel(OverallUsedFrame2, text='  Used Shelves ', font=customtkinter.CTkFont(size=16))
        percentageLabel4 = customtkinter.CTkLabel(OverallUsedFrame2, text=' {} {}%'.format(bg.existCount, existPercentage), font=customtkinter.CTkFont(size=24, weight="bold"))
        percentageLabel3.grid(row=1, column=1)
        percentageLabel4.grid(row=2, column=1)
        # percentageLabel5 = customtkinter.CTkLabel(OverallUsedFrame3, text='Used Percentage ', font=customtkinter.CTkFont(size=16))
        # percentageLabel6 = customtkinter.CTkLabel(OverallUsedFrame3, text=bg.existCount, font=customtkinter.CTkFont(size=24, weight="bold"))
        # percentageLabel5.place(relx=0.25, rely=0.3)
        # percentageLabel6.place(relx=0.4, rely=0.5)
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
        print("#########################\n", btn)
        
class buttonGenaration():
    def __init__ (self, App):
        self.content_window = None
        # Buttons
        buttonSuffix = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]
        ## A to L
        buttonNumbers = ['01', '02', '03', '06', '07', '08']
        noOfGeneratedLists = range(1, 528)
        buttonTexts = "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L"
        buttonListA_to_L = []
        self.buttonListA_to_L_initialAvailability = {}  # Initialize an empty dictionary outside the loop
        self.buttonList_M_initialAvailability = {}
        self.button_list = []
        self.existCount = 0
        self.nonExistCount = 0
        for rep in range(len(buttonNumbers)):
            for suffix in buttonSuffix:
                for buttonText in buttonTexts:
                    buttonListA_to_L.append(buttonText + buttonNumbers[rep] + suffix)
                
        # Sort the button list based on the dictionary values
        sortedButtonPositionsA_to_L = sorted(buttonListA_to_L, key=lambda x: buttonPositionsA_to_L[x])
        self.button_objects = {}
        button = None  # Initialize button outside the loop

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
            frame = App.frames[frame_index] 
            fgColor = colorOnContents(buttonName)

            # Assign fgColor based on initial availability
            initial_availability = locationUsed(buttonName)
            fgColor = "red" if initial_availability else "green"
            self.buttonListA_to_L_initialAvailability[buttonName] = {"buttonName": buttonName, "Used": locationUsed(buttonName)}
            button = customtkinter.CTkButton(frame, text=buttonName, command=lambda btn=buttonName: self.open_content_window(btn), fg_color=fgColor, width=2)
            if frame_index == 10: button.grid(row=row, column=column, padx=12, pady=13, sticky="nsew")
            else: button.grid(row=row, column=column, padx=5, pady=13, sticky="nsew")
            
            # Create the percentage label

            if(initial_availability == True):
                self.existCount = self.existCount +1
            if(initial_availability == False):
                self.nonExistCount = self.nonExistCount +1
    

            # Store button object in self.button_objects
            self.button_objects[buttonName] = button

        ## M
        buttonTextsM = "M"
        buttonNumbersM = ['01', '02', '03', '04', '05', '06', '07', '08']
        buttonList_M = []
        self.M_button_objects = {}
        for rep in range(len(buttonNumbersM)):
            for suffix in buttonSuffix:
                buttonList_M.append(buttonTextsM + buttonNumbersM[rep] + suffix)

        def buttonStatusUpdate(self):
            # Placeholder for future feature
            print("Button M01A1 status update logic goes here")

        # Sort the button list based on the dictionary values
        sortedButtons_M = sorted(buttonList_M, key=lambda x: buttonPositionsM[x])
        self.mButtons = []
        for i, buttonName in enumerate(sortedButtons_M):
            row = buttonPositionsM[buttonName][1]
            column = buttonPositionsM[buttonName][0]
            # Assign fgColor based on initial availability
            #initial_availability = locationUsed(buttonName)
            #fgColor = "red" if initial_availability else "green"
            self.buttonList_M_initialAvailability[buttonName] = {"buttonName": buttonName, "Used": locationUsed(buttonName)}
            fgColor = "Orange"
            button = customtkinter.CTkButton(App.frame_M, text=buttonName, command=lambda btn=buttonName: self.open_content_window(btn), fg_color=fgColor, width=2)
            button.grid(row=row, column=column, padx=5, pady=4, sticky="nsew")
            button.configure(text_color="black")
            self.mButtons.append(button)

            # Store button object in self.button_objects
            self.button_objects[buttonName] = button
    def updateFunction(self):
        # A to L
        for buttonName, button_info in self.buttonListA_to_L_initialAvailability.items():
            current_availability = locationUsed(buttonName)

            if button_info["Used"] != current_availability:
                self.buttonListA_to_L_initialAvailability[buttonName] = {"Used": current_availability}
                print(f"Button {buttonName} has been updated. New availability: {current_availability}")
                # Retrieve the correct button instance
                updated_button = self.button_objects[buttonName]
                # Assign fg_color based on current availability
                fg_color = colorOnContents(buttonName)
                updated_button.configure(fg_color=fg_color)
        # M
        # for buttonName, button_info in self.buttonList_M_initialAvailability.items():
        #     current_availability = locationUsed(buttonName)

        #     if button_info["Used"] != current_availability:
        #         self.buttonList_M_initialAvailability[buttonName] = {"Used": current_availability}
        #         print(f"Button {buttonName} has been updated. New availability: {current_availability}")
        #         # Retrieve the correct button instance
        #         updated_button = self.M_button_objects[buttonName]
        #         # Assign fg_color based on current availability
        #         fg_color = colorOnContents(buttonName)
        #         updated_button.configure(fg_color=fg_color)
    def get_transaction(self, callback, btn):
        response = locationButtonOnClick(btn)
        callback(response)
    def process_location_data(self, txn_data):
        if txn_data is not None:
            self.content_window = locationContentTopLevel(self, txn_data)
            self.content_window.lift()

    def open_content_window(self, btn):
        if self.content_window is None or not self.content_window.winfo_exists():
            self.get_transaction(self.process_location_data, btn)
        else:
            self.content_window.focus()
            
class locationContentTopLevel(customtkinter.CTkToplevel):
    def __init__(self, app_instance, txn_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f'{1366}x{768}')
        self.state("zoomed")
        #self.app = app_instance
        self.bg = buttonGenaration
        self.txn_data = txn_data
        if txn_data:
            self.locationMainId = self.txn_data[0]['Location']
        style = ttk.Style()
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame_left = customtkinter.CTkFrame(master=self, width=170, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky='nswe')
        first_txn_location = self.locationMainId
        self.title('{} Content'.format(first_txn_location))
        self.historylabel = customtkinter.CTkLabel(master=self.frame_left, text='{}'.format(self.locationMainId), font=customtkinter.CTkFont(size=24, weight='bold'), width=142)
        self.historylabel.grid(row=2, column=0,padx=15, pady=15)
        self.refresh_button = customtkinter.CTkButton(master=self.frame_left, text='Refresh', font=customtkinter.CTkFont(size=20, weight="bold"), width=142, command=self.refresh_data)
        self.refresh_button.grid(row=5, column=0, padx=15, pady=15)
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky='nswe', padx=15, pady=15)
        self.frame_left.grid_rowconfigure(0, minsize=10)
        self.frame_left.grid_rowconfigure(8, minsize=20)
        self.frame_left.grid_rowconfigure(11, minsize=10)
        self.add_menu_display211 = customtkinter.CTkFrame(master=self.frame_right, corner_radius=15)
        self.add_menu_display211.grid(pady=15, padx=15, sticky='nws')
        columns = ('Material', 'Descripition', 'Quantity', 'Location', 'Owner Area')
        treeview_height = 17
        self.table = ttk.Treeview(master=self, columns=columns, selectmode='browse', show='headings')

        style = ttk.Style(self)
        # set ttk theme to "clam" which support the fieldbackground option
        style.theme_use("clam")
        style.configure("Treeview", background="#40403f", 
                fieldbackground="#40403f", foreground="white")

        style.configure('Treeview', rowheight=25, font=('Arial', 10), show='tree')
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        
        style.configure('Treeview.Cell', borderwidth=0.5, relief='solid')
        for column in columns:
            self.table.heading(column, text=column, anchor='center')
            self.table.column(column, anchor='center')
        self.table.column('#1', anchor='c', minwidth=46, width=46)
        self.table.column('#2', anchor='w', minwidth=185, width=185)
        self.table.column('#3', anchor='c', minwidth=112, width=12)
        self.table.column('#4', anchor='c', minwidth=24, width=24)
        self.table.column('#5', anchor='c', minwidth=24, width=24)
        self.table.heading('Material', text='Material')
        self.table.heading('Descripition', text='Descripition')
        self.table.heading('Quantity', text='Quantity')
        self.table.heading('Location', text='Location')
        self.table.heading('Owner Area', text='Owner Area')
        self.table.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        self.table.bind('<Motion>', 'break')
        scrollbar = tkinter.Scrollbar(self, orient='vertical', command=self.table.yview)
        scrollbar.grid(row=0, column=2, sticky='ns')
        self.table.configure(yscrollcommand=scrollbar.set)
        self.process_txn_data(self.txn_data)
    
    def process_txn_data(self, txn_data):
        if txn_data is not None:
            for txn in txn_data:
                materialNo = txn['Material']
                description = fetchDescription(materialNo)
                self.table.insert('', 'end', values=(txn['Material'], 
                                                    description['Description'],
                                                    txn['Quantity'], 
                                                    txn['Location'], 
                                                    txn['Owner Area']))

    def refresh_data(self):
        self.table.delete(*self.table.get_children())
        self.txn_data = self.bg.get_transaction(self, self.process_txn_data, self.locationMainId)

if __name__ == "__main__":
    app = App()
    app.mainloop()
    

