import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk

class Design:
    def __init__(self, root):
        self.root = root
        self.df = None
        self.X = None
        self.Y = None
        
    def load_data(self):
        # File dialog to select CSV
        path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not path:
            messagebox.showwarning("Warning", "No file selected!")
            return False
        
        try:
            self.df = pd.read_csv(path)
            self.df.columns = self.df.columns.str.strip()
            sns.set_style("whitegrid")
            
            # Show data preview in a new window
            self.show_data_preview()
            
            # Ask for column names
            self.select_columns()
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
            return False
    
    def show_data_preview(self):
        # Create preview window
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Data Preview")
        preview_window.geometry("600x400")
        
        # Display columns
        tk.Label(preview_window, text="Available Columns:", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(preview_window, text=str(self.df.columns.tolist()), wraplength=550).pack(pady=5)
        
        # Display first few rows
        tk.Label(preview_window, text="First Few Rows:", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Create text widget with scrollbar
        frame = tk.Frame(preview_window)
        frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(frame, wrap=tk.NONE, yscrollcommand=scrollbar.set, height=15)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        text_widget.insert(tk.END, self.df.head().to_string())
        text_widget.config(state=tk.DISABLED)
        
        tk.Button(preview_window, text="Close", command=preview_window.destroy).pack(pady=10)
    
    def select_columns(self):
        # Create column selection window
        col_window = tk.Toplevel(self.root)
        col_window.title("Select Columns")
        col_window.geometry("400x250")
        
        tk.Label(col_window, text="Select Columns for Visualization", 
                font=("Arial", 12, "bold")).pack(pady=10)
        
        # X-axis selection
        tk.Label(col_window, text="Select X-axis (LABEL) column:").pack(pady=5)
        x_var = tk.StringVar()
        x_combo = ttk.Combobox(col_window, textvariable=x_var, 
                               values=self.df.columns.tolist(), width=30)
        x_combo.pack(pady=5)
        x_combo.current(0)
        
        # Y-axis selection
        tk.Label(col_window, text="Select Y-axis (VALUE) column:").pack(pady=5)
        y_var = tk.StringVar()
        y_combo = ttk.Combobox(col_window, textvariable=y_var, 
                               values=self.df.columns.tolist(), width=30)
        y_combo.pack(pady=5)
        if len(self.df.columns) > 1:
            y_combo.current(1)
        
        def confirm_selection():
            self.X = x_var.get().strip()
            self.Y = y_var.get().strip()
            
            if not self.X or not self.Y:
                messagebox.showwarning("Warning", "Please select both columns!")
                return
            
            messagebox.showinfo("Success", 
                              f"Columns selected:\nX-axis: {self.X}\nY-axis: {self.Y}")
            col_window.destroy()
        
        tk.Button(col_window, text="Confirm", command=confirm_selection, 
                 width=20, bg="green", fg="white").pack(pady=15)
    
    def check_data_loaded(self):
        if self.df is None or self.X is None or self.Y is None:
            messagebox.showwarning("Warning", "Please load data first!")
            return False
        return True

    def pie(self):
        if not self.check_data_loaded():
            return
        labels = self.df[self.X]
        values = self.df[self.Y]

        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title("Pie Chart")
        plt.show()

    def line(self):
        if not self.check_data_loaded():
            return
        plt.figure(figsize=(10, 6))
        x_data = self.df[self.X]
        y_data = self.df[self.Y]
        sns.lineplot(x=x_data, y=y_data, marker='o')
        plt.xlabel(self.X)
        plt.ylabel(self.Y)
        plt.title("Line Chart")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def scatter(self):
        if not self.check_data_loaded():
            return
        plt.figure(figsize=(10, 6))
        x_data = self.df[self.X]
        y_data = self.df[self.Y]
        sns.scatterplot(x=x_data, y=y_data, s=100)
        plt.xlabel(self.X)
        plt.ylabel(self.Y)
        plt.title("Scatter Chart")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def histogram(self):
        if not self.check_data_loaded():
            return
        plt.figure(figsize=(10, 6))
        y_data = self.df[self.Y]
        sns.histplot(x=y_data, bins=10, kde=True, edgecolor='black')
        plt.xlabel(self.Y)
        plt.ylabel('Frequency')
        plt.title("Histogram with KDE")
        plt.tight_layout()
        plt.show()
    
    def bar(self):
        if not self.check_data_loaded():
            return
        plt.figure(figsize=(10, 6))
        x_data = self.df[self.X]
        y_data = self.df[self.Y]
        sns.barplot(x=x_data, y=y_data, palette='viridis')
        plt.xlabel(self.X)
        plt.ylabel(self.Y)
        plt.title("Bar Chart")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def box(self):
        if not self.check_data_loaded():
            return
        plt.figure(figsize=(10, 6))
        y_data = self.df[self.Y]
        sns.boxplot(y=y_data, palette='Set2')
        plt.ylabel(self.Y)
        plt.title("Box Plot")
        plt.tight_layout()
        plt.show()
    
    def violin(self):
        if not self.check_data_loaded():
            return
        plt.figure(figsize=(10, 6))
        y_data = self.df[self.Y]
        sns.violinplot(y=y_data, palette='muted')
        plt.ylabel(self.Y)
        plt.title("Violin Plot")
        plt.tight_layout()
        plt.show()
    
    def heatmap(self):
        if not self.check_data_loaded():
            return
        plt.figure(figsize=(10, 8))
        numeric_df = self.df.select_dtypes(include=['float64', 'int64'])
        if numeric_df.empty:
            messagebox.showinfo("Info", "No numeric columns found for correlation heatmap!")
            return
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', center=0, fmt='.2f')
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        plt.show()
    
    def pairplot(self):
        if not self.check_data_loaded():
            return
        numeric_df = self.df.select_dtypes(include=['float64', 'int64'])
        if numeric_df.empty:
            messagebox.showinfo("Info", "No numeric columns found for pair plot!")
            return
        sns.pairplot(numeric_df)
        plt.suptitle("Pair Plot", y=1.02)
        plt.show()
    
    def countplot(self):
        if not self.check_data_loaded():
            return
        plt.figure(figsize=(10, 6))
        x_data = self.df[self.X]
        sns.countplot(x=x_data, palette='pastel')
        plt.xlabel(self.X)
        plt.ylabel('Count')
        plt.title("Count Plot")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


# Create main window
root = tk.Tk()
root.title("Data Analytics Tool")
root.geometry("450x600")
root.configure(bg="#f0f0f0")

# Create Design object
design = Design(root)

# Header
header = tk.Label(root, text="📊 Sales Visualization Dashboard", 
                 font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
header.pack(pady=15)

# Load Data Button
load_btn = tk.Button(root, text="📁 Load CSV File", width=35, height=2,
                    command=design.load_data, bg="#4CAF50", fg="white",
                    font=("Arial", 10, "bold"))
load_btn.pack(pady=10)

# Separator
tk.Label(root, text="─" * 50, bg="#f0f0f0").pack(pady=5)

# Visualization buttons
tk.Button(root, text="1. Pie Chart", width=35, command=design.pie, bg="#e3f2fd").pack(pady=3)
tk.Button(root, text="2. Line Plot", width=35, command=design.line, bg="#e3f2fd").pack(pady=3)
tk.Button(root, text="3. Scatter Plot", width=35, command=design.scatter, bg="#e3f2fd").pack(pady=3)
tk.Button(root, text="4. Histogram", width=35, command=design.histogram, bg="#e3f2fd").pack(pady=3)
tk.Button(root, text="5. Bar Chart", width=35, command=design.bar, bg="#e3f2fd").pack(pady=3)
tk.Button(root, text="6. Box Plot", width=35, command=design.box, bg="#e3f2fd").pack(pady=3)
tk.Button(root, text="7. Violin Plot", width=35, command=design.violin, bg="#e3f2fd").pack(pady=3)
tk.Button(root, text="8. Heatmap", width=35, command=design.heatmap, bg="#e3f2fd").pack(pady=3)
tk.Button(root, text="9. Pair Plot", width=35, command=design.pairplot, bg="#e3f2fd").pack(pady=3)
tk.Button(root, text="10. Count Plot", width=35, command=design.countplot, bg="#e3f2fd").pack(pady=3)

# Separator
tk.Label(root, text="─" * 50, bg="#f0f0f0").pack(pady=5)

# Exit button
tk.Button(root, text="❌ Exit", width=35, command=root.destroy, 
         bg="#f44336", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

root.mainloop()