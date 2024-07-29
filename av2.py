from customtkinter import *
import tkinter as tk
from numpy import random
import time
import threading

class Data:
    def __init__(self, num, algo, gui) -> None:
        self.num = num
        self.algo = algo
        self.gui = gui

    def get_data(self):
        return [self.num, self.algo]
    
    def set_num(self, num):
        self.num = num
        self.gui.initGraph()
        print(self.num)

    def set_algo(self, algo):
        self.algo = algo
        self.gui.initGraph()
        print(self.algo)

    def get_num(self):
        return int(self.num)

    def get_algo(self):
        return str(self.algo)

class GUI:
    def __init__(self) -> None:
        self.app = CTk(fg_color='#230C33')
        self.app.state('zoomed')
        self.app.title("Sorting Algorithm Visualizer")
        self.data = Data(120, 'Selection Sort', self)
        self.nums = []
        self.canvas_nums = []
        self.stop_event = threading.Event()

        self.app.rowconfigure(0, weight=1)
        self.app.columnconfigure(0, weight=1)

        self.sort_frame = tk.Canvas(self.app, bg="#592E83")
        self.sort_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.app.update()

        self.initGraph()

        self.menu = Menu(self)

        self.app.update()
        self.app.mainloop()

    def initGraph(self):
        # Init stuff
        n = self.data.get_num()
        canvas_width = self.sort_frame.winfo_width()
        canvas_height = self.sort_frame.winfo_height()
        bar_width = canvas_width / n
        x = 0
        scale = 600/n
        self.nums = []

        # Get array of nums
        self.nums = [x+1 for x in range(n)]
        random.shuffle(self.nums)

        # Reset Canvas
        self.sort_frame.delete("all")
        self.canvas_nums.clear()
        self.canvas_nums = []

        # Create bars
        for number in self.nums:
            new_rectangle = self.sort_frame.create_rectangle(x, canvas_height, x+bar_width, canvas_height-number*scale, fill='gray', width=1)
            self.canvas_nums.append(new_rectangle)
            x += bar_width

        # Forget the pack
        self.sort_frame.pack_forget()

        # Replace Pack
        self.sort_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def get_gui_data(self):
        print(self.nums)

    def start_sort(self):
        algo = self.data.get_algo()
        self.stop_event.clear()
        print(algo)
        match algo:
            case 'Selection Sort':
                threading.Thread(target=self.selection_sort).start()
            case 'Bubble Sort':
                threading.Thread(target=self.bubble_sort).start()
            case 'Insertion Sort':
                threading.Thread(target=self.insertion_sort).start()
            case 'Merge Sort':
                threading.Thread(target=self.merge_sort_thread).start()
                print(self.nums)
            case 'Quick Sort':
                threading.Thread(target=self.quick_sort_thread).start()
                print(self.nums)
            case 'Heap Sort':
                threading.Thread(target=self.heap_sort_thread).start()
                print(self.nums)
            case 'Counting Sort':
                threading.Thread(target=self.count_sort).start()
                print(self.nums)
            case 'Bucket Sort':
                print('here')
            case 'Bingo Sort':
                print('here')

    def stop_sort(self):
        self.stop_event.set()

    def reset_sort(self):
        self.initGraph()

    def update_graph(self, index1, index2):
        # Ensure thread safety with a lock
        with threading.Lock():
            # Init things
            n = self.data.get_num()
            canvas_width = self.sort_frame.winfo_width()
            canvas_height = self.sort_frame.winfo_height()
            bar_width = canvas_width / n
            scale = 600 / n

            # Get coordinates for the rectangles
            x1 = index1 * bar_width
            y1 = canvas_height - self.nums[index1] * scale
            x2 = index2 * bar_width
            y2 = canvas_height - self.nums[index2] * scale

            # Delete the old rectangles
            self.sort_frame.delete(self.canvas_nums[index1])
            self.sort_frame.delete(self.canvas_nums[index2])

            # Create new RED rectangles
            self.canvas_nums[index1] = self.sort_frame.create_rectangle(x1, canvas_height, x1 + bar_width, y1, fill='red', width=1)
            self.canvas_nums[index2] = self.sort_frame.create_rectangle(x2, canvas_height, x2 + bar_width, y2, fill='red', width=1)

            # Force update to ensure canvas is correctly refreshed
            self.app.update_idletasks()
            time.sleep(0.03)

            # Delete the RED rectangles
            self.sort_frame.delete(self.canvas_nums[index1])
            self.sort_frame.delete(self.canvas_nums[index2])

            # Create new GRAY rectangles
            self.canvas_nums[index1] = self.sort_frame.create_rectangle(x1, canvas_height, x1 + bar_width, y1, fill='gray', width=1)
            self.canvas_nums[index2] = self.sort_frame.create_rectangle(x2, canvas_height, x2 + bar_width, y2, fill='gray', width=1)

            # Force update to ensure canvas is correctly refreshed
            self.app.update_idletasks()
            time.sleep(0.01)

    def update_graph2(self, index):
        if self.stop_event.is_set():
            return

        # Init things
        n = self.data.get_num()
        canvas_width = self.sort_frame.winfo_width()
        canvas_height = self.sort_frame.winfo_height()
        bar_width = canvas_width / n
        scale = 600 / n

        # Get coordinates for the rectangle
        x = index * bar_width
        y = canvas_height - self.nums[index] * scale

        # Delete the old rectangle
        self.sort_frame.delete(self.canvas_nums[index])

        # Create new rectangle
        self.canvas_nums[index] = self.sort_frame.create_rectangle(x, canvas_height, x + bar_width, y, fill='red', width=1)

        # Replace Pack
        self.sort_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.app.update_idletasks()
        time.sleep(0.03)

        # Delete the old rectangle
        self.sort_frame.delete(self.canvas_nums[index])

        # Create new rectangle
        self.canvas_nums[index] = self.sort_frame.create_rectangle(x, canvas_height, x + bar_width, y, fill='gray', width=1)

        # Replace Pack
        self.sort_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Update the GUI
        self.app.update_idletasks()
        time.sleep(0.01)

    def swap(self, i, j):
        tmp = self.nums[i]
        self.nums[i] = self.nums[j]
        self.nums[j] = tmp

    def finished(self):
        # Set button back to start
        self.stop_event.clear()
        self.menu.toggle_ss_btn()
        pass

    def bubble_sort(self):
        for i in range(len(self.nums)):
            if self.stop_event.is_set():
                break
            for j in range(len(self.nums)):
                if self.stop_event.is_set():
                    break
                if self.nums[i] < self.nums[j]:
                    self.swap(i, j)
                    self.update_graph(j, j + 1)
                    time.sleep(0.01)  # Add a small delay
                    self.app.update_idletasks()
        self.finished()

    def selection_sort(self):
        n = len(self.nums)
        for i in range(n):
            if self.stop_event.is_set():
                break
            min_index = i
            for j in range(i+1, n):
                if self.stop_event.is_set():
                    break
                if self.nums[min_index] > self.nums[j]:
                    min_index = j
            self.swap(i, min_index)
            self.update_graph(i, min_index)
            time.sleep(0.01)  # Add a small delay
            self.app.update_idletasks()
        self.finished()

    def insertion_sort(self):
        n = len(self.nums)
        for i in range(1, n):
            if self.stop_event.is_set():
                break
            val = self.nums[i]
            j = i-1
            while j >= 0 and val < self.nums[j]:
                if self.stop_event.is_set():
                    break
                self.swap(j, j+1)
                self.update_graph(j, j+1)
                time.sleep(0.01)  # Add a small delay
                self.app.update_idletasks()
                j -= 1
            self.nums[j+1] = val
        self.finished()    

    def merge(self, left, mid, right):
        subArr1 = mid - left + 1
        subArr2 = right - mid

        # Create Temp Arrays
        leftArr = [0] * subArr1
        rightArr = [0] * subArr2

        # Copy data into tmp arrays
        for i in range(subArr1):
            leftArr[i] = self.nums[left + i]
        for j in range(subArr2):
            rightArr[j] = self.nums[mid + 1 + j]

        indexOfSubArr1 = 0
        indexOfSubArr2 = 0
        indexOfMergedArr = left

        while indexOfSubArr1 < subArr1 and indexOfSubArr2 < subArr2:
            if leftArr[indexOfSubArr1] <= rightArr[indexOfSubArr2]:
                self.nums[indexOfMergedArr] = leftArr[indexOfSubArr1]
                indexOfSubArr1 += 1
            else:
                self.nums[indexOfMergedArr] = rightArr[indexOfSubArr2]
                indexOfSubArr2 += 1
            self.update_graph2(indexOfMergedArr)
            indexOfMergedArr += 1

        while indexOfSubArr1 < subArr1:
            self.nums[indexOfMergedArr] = leftArr[indexOfSubArr1]
            self.update_graph2(indexOfMergedArr)
            indexOfMergedArr += 1
            indexOfSubArr1 += 1

        while indexOfSubArr2 < subArr2:
            self.nums[indexOfMergedArr] = rightArr[indexOfSubArr2]
            self.update_graph2(indexOfMergedArr)
            indexOfMergedArr += 1
            indexOfSubArr2 += 1

    def merge_sort(self, start, end):
        if start < end:
            mid = start + (end - start) // 2
            self.merge_sort(start, mid)
            self.merge_sort(mid + 1, end)
            self.merge(start, mid, end)

    def merge_sort_thread(self):
        self.merge_sort(0, len(self.nums) - 1)
        self.finished()

    def partition(self, low, high):
        if self.stop_event.is_set():
            return
        i = low - 1
        pv = self.nums[high]

        for j in range(low, high):
            if self.stop_event.is_set():
                return
            if self.nums[j] < pv:
                i += 1
                self.swap(i, j)
                self.update_graph2(i)
                self.app.update_idletasks()
                self.update_graph2(j)
                self.app.update_idletasks()

        self.swap(i+1, high)
        self.update_graph2(i+1)
        self.app.update_idletasks()
        self.update_graph2(high)
        self.app.update_idletasks()
        return i + 1

    def quick_sort(self, low, high):
        if self.stop_event.is_set():
            return
        if low < high:
            p = self.partition(low, high)
            self.quick_sort(low, p - 1)
            self.quick_sort(p + 1, high)

    def quick_sort_thread(self):
        self.quick_sort(0, len(self.nums)-1)
        self.finished()

    def heapify(self, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and self.nums[largest] < self.nums[l]:
            largest = l
        if r < n and self.nums[largest] < self.nums[r]:
            largest = r
        if largest != i:
            self.swap(i, largest)
            self.update_graph2(i)
            self.app.update_idletasks()
            self.update_graph2(largest)
            self.app.update_idletasks()
            self.heapify(n, largest)

    def heap_sort(self):
        n = len(self.nums)

        for i in range(n//2 - 1, -1, -1):
            self.heapify(n, i)
        
        for i in range(n-1, 0, -1):
            self.swap(i, 0)
            self.update_graph2(i)
            self.app.update_idletasks()
            self.update_graph2(0)
            self.app.update_idletasks()
            self.heapify(i, 0)

    def heap_sort_thread(self):
        self.heap_sort()
        self.finished()

    def count_sort(self):
        if self.stop_event.is_set():
            return
        
        # Finding the maximum element of input_array.
        max_val = max(self.nums)
        min_val = min(self.nums)
    
        # Create a count array to store the count of individual elements
        count_arr = [1] * self.data.num
        output_arr = [0] * len(self.nums)

        print("CAJLKl", count_arr)

        # Change count_arr to store actual position of elements in output array
        for i in range(1, len(count_arr)):
            count_arr[i] += count_arr[i - 1]
            if self.stop_event.is_set():
                return
            self.update_graph2(i)   # Highlight the cumulative count operation
            self.app.update_idletasks()

        # Build the output array using count_arr
        for i in range(len(self.nums) - 1, -1, -1):
            output_arr[count_arr[self.nums[i] - min_val] - 1] = self.nums[i]
            count_arr[self.nums[i] - min_val] -= 1
            if self.stop_event.is_set():
                return
            self.update_graph(i, count_arr[self.nums[i] - min_val])  # Highlight the placement operation
            self.app.update_idletasks()

        # Copy the sorted elements into original array
        for i in range(len(self.nums)):
            self.nums[i] = output_arr[i]
            if self.stop_event.is_set():
                return
            self.update_graph2(i)  # Highlight the final sorted position
            self.app.update_idletasks()
        
        print(output_arr)
    
    def radix_sort(self):
        pass

class Menu:
    def __init__(self, gui) -> None:
        self.gui = gui

        # Toggle Button
        self.off_menu = CTkButton(master=self.gui.sort_frame, 
                            fg_color="#B27C66", 
                            border_color="#CAA8F5", 
                            border_width=5, 
                            font=('Roboto Mono Bold',30), 
                            corner_radius=15, 
                            text_color='#CAA8F5',
                            text= 'Menu',
                            border_spacing=10,
                            hover=True,
                            hover_color='#c39988',
                            command=self.toggle_menu
                        )

        # Menu
        self.on_menu = CTkFrame(master=self.gui.sort_frame, 
                            fg_color="#B27C66", 
                            border_color="#CAA8F5", 
                            border_width=5, 
                            corner_radius=20
                        )
        self.on_menu.rowconfigure(0, weight=1)
        self.on_menu.columnconfigure(0 , weight=1)

        # Close Button
        self.close_button = CTkButton(master=self.on_menu, 
                                text='X', 
                                font=('Arial', 20), 
                                text_color='#CAA8F5', 
                                fg_color='transparent', 
                                hover_color='#a96d55', 
                                corner_radius=20, 
                                command=self.toggle_menu
                            )
        self.close_button.configure(width=5)
        self.close_button.grid(row=0, column=3, padx=(20,20), pady=(10,0))

        # Algo Label and ComboBox
        self.algo_label = CTkLabel(master=self.on_menu, 
                            text=f"Sorting Algorithm:", 
                            font=('Roboto Mono Bold', 20), 
                            text_color='#CAA8F5'
                        )
        self.algo_combobox = CTkComboBox(master=self.on_menu, 
                                command=self.algo_changed,
                                font=('Roboto Mono Bold', 12),
                                width=1, 
                                values=["Selection Sort", "Bubble Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort", "Counting Sort"]
                            )
        self.algo_combobox.set("Selection Sort")
        self.algo_combobox.configure(width=150)
        self.algo_label.grid(row=0, padx=(20,0), column=0, sticky="ew", pady=(20, 10))
        self.algo_combobox.grid(row=0, column=1, sticky="ew", pady=(20, 10), columnspan=2)

        # Num Label, Entry, and Button
        self.num_label = CTkLabel(master=self.on_menu, 
                            text=f"Number of elements:", 
                            font=('Roboto Mono Bold', 20), 
                            text_color='#CAA8F5'
                        )
        self.num_entry = CTkEntry(master=self.on_menu, 
                            placeholder_text=str(self.gui.data.num),
                            font=('Roboto Mono Bold', 12),
                        )
        self.num_entry.configure( width=100)
        self.num_btn = CTkButton(master=self.on_menu, 
                            text="Set", 
                            command= lambda: self.gui.data.set_num(self.num_entry.get()),
                            font=('Roboto Mono Bold', 12),

                        )
        self.num_btn.configure(width=50)
        self.num_label.grid(row=1, padx=(20,0), column=0, sticky="ew", pady=(0,20))
        self.num_entry.grid(row=1, column=1, sticky="ns", pady=(0,20), padx=(10,0))
        self.num_btn.grid(row=1, padx=(10,20), column=2, sticky="ew", pady=(0,20))

        # Start / Stop Buttons
        self.start_button = CTkButton(master=self.gui.sort_frame, 
                                text="Start",
                                command=self.start,
                                fg_color="#B27C66", 
                                border_color="#CAA8F5", 
                                border_width=5, 
                                font=('Roboto Mono Bold',30),
                                corner_radius=15, 
                                text_color='#CAA8F5',
                                border_spacing=10,
                                hover=True,
                                hover_color='#c39988',
                            )
        self.stop_button = CTkButton(master=self.gui.sort_frame, 
                                text="Stop",
                                command=self.stop,
                                fg_color="#B27C66", 
                                border_color="#CAA8F5", 
                                border_width=5, 
                                font=('Roboto Mono Bold',30),
                                corner_radius=15, 
                                text_color='#CAA8F5',
                                border_spacing=10,
                                hover=True,
                                hover_color='#c39988',
                            )
        self.reset_button = CTkButton(master=self.gui.sort_frame, 
                                text="Reset",
                                command=self.reset,
                                fg_color="#B27C66", 
                                border_color="#CAA8F5", 
                                border_width=5, 
                                font=('Roboto Mono Bold',30),
                                corner_radius=15, 
                                text_color='#CAA8F5',
                                border_spacing=10,
                                hover=True,
                                hover_color='#c39988',
                            )
        self.start_button.configure(width=20)
        self.stop_button.configure(width=20)
        self.reset_button.configure(width=20)

        # Render First Menu
        self.off_menu.pack(padx=10, pady=10, side="left", anchor="n")

        # Render Start Button
        self.start_button.pack(padx=(0,10), pady=10, side="left", anchor="n")

    def toggle_menu(self):
        if self.on_menu.winfo_viewable():
            self.on_menu.pack_forget()
            self.off_menu.pack(padx=10, pady=10, side="left", anchor="n")
            self.off_menu.lift()
            self.reload_ss_buttons()
        else:
            self.off_menu.pack_forget()
            self.on_menu.pack(padx=10, pady=10, side="left", anchor="n")
            self.on_menu.lift()
            self.reload_ss_buttons()

    def toggle_ss_btn(self):
        if self.start_button.winfo_viewable():
            self.start_button.pack_forget()
            self.stop_button.pack(padx=(0,10), pady=10, side="left", anchor="n")
            self.stop_button.lift()
        elif self.stop_button.winfo_viewable():
            self.stop_button.pack_forget()
            self.reset_button.pack(padx=(0,10), pady=10, side="left", anchor="n")
            self.reset_button.lift()
        else:
            self.reset_button.pack_forget()
            self.start_button.pack(padx=(0,10), pady=10, side="left", anchor="n")
            self.start_button.lift()

    def algo_changed(self, event):
        algo = self.algo_combobox.get()
        self.gui.data.set_algo(algo)

    def start(self):
        print('Starting...')
        
        # Toggle Buttons
        self.start_button.pack_forget()
        self.stop_button.pack(padx=(0,10), pady=10, side="left", anchor="n")
        self.stop_button.lift()

        self.gui.start_sort()

    def stop(self):
        print('Stopping...')
        self.gui.stop_sort()

    def reset(self):
        print('Resetting...')

        # Toggle buttons
        self.reset_button.pack_forget()
        self.start_button.pack(padx=(0,10), pady=10, side="left", anchor="n")
        self.start_button.lift()

        self.gui.reset_sort()

    def reload_ss_buttons(self):
        if self.start_button.winfo_viewable():
            self.start_button.pack_forget()
            self.start_button.pack(padx=(0,10), pady=10, side="left", anchor="n")
            self.start_button.lift()
        elif self.reset_button.winfo_viewable():
            self.reset_button.pack_forget()
            self.reset_button.pack(padx=(0,10), pady=10, side="left", anchor="n")
            self.reset_button.lift()
        else:
            self.stop_button.pack_forget()
            self.stop_button.pack(padx=(0,10), pady=10, side="left", anchor="n")
            self.stop_button.lift()

if __name__ == "__main__":
    g = GUI()
