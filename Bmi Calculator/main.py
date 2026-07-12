"""
Advanced BMI Calculator - Main Application
GUI with data storage, history, and visualization
"""

from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from bmi_core import BMICore, DataManager
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        self.bmi_core = BMICore()
        self.data_manager = DataManager()
        
        # Colors for BMI scale
        self.colors = {
            'underweight': '#3498db',
            'normal': '#2ecc71',
            'overweight': '#f39c12',
            'obese1': '#e67e22',
            'obese2': '#e74c3c',
            'obese3': '#c0392b'
        }
        
        self.setup_ui()
        self.refresh_all()
    
    def setup_ui(self):
        """Setup the main UI with tabs"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.calculator_tab = ttk.Frame(self.notebook)
        self.history_tab = ttk.Frame(self.notebook)
        self.stats_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.calculator_tab, text="📊 Calculator")
        self.notebook.add(self.history_tab, text="📈 History")
        self.notebook.add(self.stats_tab, text="📉 Trends")
        
        self.setup_calculator_tab()
        self.setup_history_tab()
        self.setup_stats_tab()
    
    def setup_calculator_tab(self):
        """Setup the calculator tab"""
        input_frame = ttk.LabelFrame(self.calculator_tab, text="Enter Your Details", padding=20)
        input_frame.pack(pady=20, padx=20, fill='x')
        
        # Name
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky='w', pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Age
        ttk.Label(input_frame, text="Age:").grid(row=1, column=0, sticky='w', pady=5)
        self.age_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.age_var, width=30).grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Gender
        ttk.Label(input_frame, text="Gender:").grid(row=2, column=0, sticky='w', pady=5)
        self.gender_var = tk.StringVar(value="Male")
        gender_frame = ttk.Frame(input_frame)
        gender_frame.grid(row=2, column=1, pady=5, padx=(10, 0), sticky='w')
        ttk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, 
                       value="Male").pack(side='left')
        ttk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, 
                       value="Female").pack(side='left', padx=(10, 0))
        
        # Weight
        ttk.Label(input_frame, text="Weight (kg):").grid(row=3, column=0, sticky='w', pady=5)
        self.weight_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.weight_var, width=30).grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # Height
        ttk.Label(input_frame, text="Height (m):").grid(row=4, column=0, sticky='w', pady=5)
        self.height_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.height_var, width=30).grid(row=4, column=1, pady=5, padx=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="Calculate BMI", command=self.calculate_bmi,
                  width=20).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_fields,
                  width=15).pack(side='left', padx=5)
        
        self.result_frame = ttk.LabelFrame(self.calculator_tab, text="Result", padding=20)
        self.result_frame.pack(pady=10, padx=20, fill='x')
        
        self.result_text = tk.Text(self.result_frame, height=8, width=50, font=('Arial', 11))
        self.result_text.pack(fill='x')
        
        self.scale_frame = ttk.Frame(self.calculator_tab)
        self.scale_frame.pack(pady=10, padx=20, fill='x')
        self.create_bmi_scale()
    
    def create_bmi_scale(self):
        """Create visual BMI scale"""
        self.scale_canvas = tk.Canvas(self.scale_frame, height=60, bg='white')
        self.scale_canvas.pack(fill='x', padx=10)
        
        self.scale_canvas.delete("all")
        width = self.scale_canvas.winfo_width() if self.scale_canvas.winfo_width() > 100 else 700
        
        segments = [
            (0, 18.5, self.colors['underweight'], "Underweight"),
            (18.5, 25, self.colors['normal'], "Normal"),
            (25, 30, self.colors['overweight'], "Overweight"),
            (30, 35, self.colors['obese1'], "Obese I"),
            (35, 40, self.colors['obese2'], "Obese II"),
            (40, 50, self.colors['obese3'], "Obese III")
        ]
        
        for start, end, color, label in segments:
            x1 = 50 + (start / 50) * width
            x2 = 50 + (end / 50) * width
            self.scale_canvas.create_rectangle(x1, 10, x2, 50, fill=color, outline='')
            if end < 50:
                self.scale_canvas.create_text((x1 + x2)/2, 58, text=label, font=('Arial', 7), anchor='n')
        
        for bmi in [18.5, 25, 30, 35, 40]:
            x = 50 + (bmi / 50) * width
            self.scale_canvas.create_line(x, 5, x, 55, fill='black', width=1)
            self.scale_canvas.create_text(x, 62, text=str(bmi), font=('Arial', 7))
        
        
        self.bmi_marker = self.scale_canvas.create_polygon(
            50, 30,     
            40, 20,     
            40, 40,    
            fill='red', 
            outline='red'
        )
        self.bmi_text = self.scale_canvas.create_text(80, 30, text="BMI: 0", 
                                                     font=('Arial', 10, 'bold'))
    
    def setup_history_tab(self):
        """Setup the history tab"""
        columns = ('Date', 'Name', 'Age', 'Gender', 'Weight', 'Height', 'BMI', 'Category')
        self.history_tree = ttk.Treeview(self.history_tab, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=80)
        
        self.history_tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(self.history_tab, orient='vertical', 
                                 command=self.history_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        button_frame = ttk.Frame(self.history_tab)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Delete Selected", 
                  command=self.delete_selected).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear All", 
                  command=self.clear_history).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Refresh", 
                  command=self.refresh_history).pack(side='left', padx=5)
        
        self.refresh_history()
    
    def setup_stats_tab(self):
        """Setup the statistics tab"""
        self.stats_frame = ttk.Frame(self.stats_tab)
        self.stats_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        self.stats_text = tk.Text(self.stats_frame, height=8, font=('Arial', 10))
        self.stats_text.pack(fill='x', pady=(0, 10))
        
        self.graph_frame = ttk.Frame(self.stats_tab)
        self.graph_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        self.update_stats()
    
    def calculate_bmi(self):
        """Calculate BMI and display result"""
        try:
            name = self.name_var.get().strip() or "Unknown"
            age = int(self.age_var.get()) if self.age_var.get() else 0
            gender = self.gender_var.get()
            weight = float(self.weight_var.get())
            height = float(self.height_var.get())
            
            # Validate inputs
            self.bmi_core.validate_inputs(weight, height, age if age else None)
            
            bmi = self.bmi_core.calculate(weight, height)
            category, advice = self.bmi_core.get_category(bmi)
            
            # Display result
            result = f"Name: {name}\n"
            result += f"Age: {age}\n" if age else ""
            result += f"Gender: {gender}\n"
            result += f"Weight: {weight} kg\n"
            result += f"Height: {height} m\n"
            result += f"\nBMI: {bmi:.2f}\n"
            result += f"Category: {category}\n"
            result += f"Advice: {advice}"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, result)
            
            self.update_bmi_marker(bmi)
            
            self.data_manager.add_record(name, age, gender, weight, height, bmi, category)
            self.refresh_all()
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def update_bmi_marker(self, bmi):
        """Update BMI marker on scale"""
        width = self.scale_canvas.winfo_width() if self.scale_canvas.winfo_width() > 100 else 700
        x = 50 + (bmi / 50) * width
        x = max(50, min(50 + width, x))
        
       
        self.scale_canvas.coords(
            self.bmi_marker, 
            x, 30,    
            x-10, 20, 
            x-10, 40  
        )
        self.scale_canvas.itemconfig(self.bmi_text, text=f"BMI: {bmi:.1f}")
    
    def refresh_history(self):
        """Refresh history table"""
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        for record in self.data_manager.data:
            values = (
                record.get('date', ''),
                record.get('name', ''),
                record.get('age', ''),
                record.get('gender', ''),
                record.get('weight', ''),
                record.get('height', ''),
                record.get('bmi', ''),
                record.get('category', '')
            )
            self.history_tree.insert('', 'end', values=values)
    
    def delete_selected(self):
        """Delete selected records"""
        selected = self.history_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return
        
        if messagebox.askyesno("Confirm", "Delete selected record(s)?"):
            indices = [self.history_tree.index(item) for item in selected]
            for index in sorted(indices, reverse=True):
                self.data_manager.delete_record(index)
            self.refresh_all()
    
    def clear_history(self):
        """Clear all history"""
        if messagebox.askyesno("Confirm", "Delete all history?"):
            self.data_manager.clear_all()
            self.refresh_all()
    
    def clear_fields(self):
        """Clear input fields"""
        self.name_var.set("")
        self.age_var.set("")
        self.weight_var.set("")
        self.height_var.set("")
        self.result_text.delete(1.0, tk.END)
    
    def update_stats(self):
        """Update statistics display"""
        stats = self.data_manager.get_statistics()
        
        if not stats:
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, "No data available. Add records to see statistics!")
            return
        
        text = f"📊 BMI Statistics\n"
        text += "=" * 40 + "\n"
        text += f"Total Records: {stats['total']}\n"
        text += f"Average BMI: {stats['avg_bmi']:.2f}\n"
        text += f"Highest BMI: {stats['max_bmi']:.2f}\n"
        text += f"Lowest BMI: {stats['min_bmi']:.2f}\n\n"
        text += "📋 Category Distribution:\n"
        
        for category, count in stats['category_counts'].items():
            percentage = (count / stats['total']) * 100
            text += f"  {category}: {count} ({percentage:.1f}%)\n"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, text)
        self.create_graph()
    
    def create_graph(self):
        """Create BMI trend graph"""
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        if len(self.data_manager.data) < 2:
            ttk.Label(self.graph_frame, text="Need at least 2 records for trend analysis",
                     font=('Arial', 12)).pack(pady=50)
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        fig.patch.set_facecolor('#f0f0f0')
        
        # BMI trend
        dates = [datetime.strptime(r['date'], "%Y-%m-%d %H:%M:%S") for r in self.data_manager.data]
        bmis = [r['bmi'] for r in self.data_manager.data]
        
        ax1.plot(dates, bmis, 'b-', marker='o', linewidth=2, markersize=6)
        ax1.axhline(y=18.5, color='g', linestyle='--', alpha=0.5, label='Underweight/Normal')
        ax1.axhline(y=25, color='y', linestyle='--', alpha=0.5, label='Normal/Overweight')
        ax1.axhline(y=30, color='orange', linestyle='--', alpha=0.5, label='Overweight/Obese')
        ax1.set_title('BMI Trend Over Time')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('BMI')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax1.tick_params(axis='x', rotation=45)
        
        # Category distribution
        categories = ['Underweight', 'Normal', 'Overweight', 'Obese Class I', 
                     'Obese Class II', 'Obese Class III']
        counts = [sum(1 for r in self.data_manager.data if r['category'] == cat) for cat in categories]
        colors = ['#3498db', '#2ecc71', '#f39c12', '#e67e22', '#e74c3c', '#c0392b']
        
        bars = ax2.bar(categories, counts, color=colors)
        ax2.set_title('BMI Category Distribution')
        ax2.set_xlabel('Category')
        ax2.set_ylabel('Count')
        ax2.tick_params(axis='x', rotation=45)
        
        for bar, count in zip(bars, counts):
            if count > 0:
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                        str(count), ha='center', va='bottom')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def refresh_all(self):
        """Refresh all tabs"""
        self.refresh_history()
        self.update_stats()

def main():
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()