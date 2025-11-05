import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from tkinter import messagebox

def start():
    dt = 0.05
    g = 9.8
    
    # --- Tkinter window setup ---
    window = tk.Tk()
    window.title("Javelin Throw Input")
    window.geometry("300x300")

    # --- Input fields for Height, Speed, Angle ---
    tk.Label(window, text="Height (m):", font=('Arial', 12)).pack(pady=5)
    height_entry = tk.Entry(window, font=('Arial', 12))
    height_entry.pack()

    tk.Label(window, text="Speed (m/s):", font=('Arial', 12)).pack(pady=5)
    speed_entry = tk.Entry(window, font=('Arial', 12))
    speed_entry.pack()

    tk.Label(window, text="Angle (degrees):", font=('Arial', 12)).pack(pady=5)
    angle_entry = tk.Entry(window, font=('Arial', 12))
    angle_entry.pack()

    # --- Main projectile animation function ---
    def animate_projectile(height, speed, angle):
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_xlim(0, 40 + ((speed)**2 * np.sin(2*angle))/g)
        # ax.set_ylim(0, (speed**2)* (np.sin(angle)**2)*0.5/g + height+100)
        ax.set_ylim(0, 80)
        # ax.set_aspect('equal')
        ax.set_xlabel('Horizontal Position (m)')
        ax.set_ylabel('Height (m)')
        ax.set_title(f'Javelin Throw from {height} m')
        ax.grid(True, alpha=0.3)
        
        # Ground line
        ax.axhline(y=0, color='brown', linewidth=3, label='Ground')
        
        javelin, = ax.plot([], [], 'b-', linewidth=3, label='Javelin')
        
        
        # Info text
        info_text = ax.text(0.02, 0.98, '', transform=ax.transAxes,
                           verticalalignment='top', fontsize=10,
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        def init():
            javelin.set_data([], [])
            info_text.set_text('')
            return javelin, info_text
        
        def animate(frame):
            t = frame * dt
            x = speed * np.cos(angle) * t
            y = height + speed * np.sin(angle) * t - 0.5 * g * t**2
            vx = speed * np.cos(angle)
            vy = speed * np.sin(angle) - g * t
            theta = np.arctan(vy/vx)
            x1 = x - 7.5*np.cos(theta)
            y1 = y - 7.5*np.sin(theta)
            x2 = x + 7.5*np.cos(theta)
            y2 = y + 7.5*np.sin(theta)
            
            v = g * t  # simplified velocity
            
            if y2 <= 0:
                y = 0
                v = g * np.sqrt(2 * height / g)
                info_text.set_text(f'Time: {t:.2f} s\nHeight: {y:.2f} m\nVelocity: {v:.2f} m/s\n** HIT GROUND **')
                ani.event_source.stop()
            else:
                info_text.set_text(f'Time: {t:.2f} s\nHeight: {y:.2f} m\nVelocity: {v:.2f} m/s')
            
            javelin.set_data([x1, x2], [y1, y2])
            
            return javelin, info_text
        
        ani = animation.FuncAnimation(
            fig, animate, init_func=init,
            frames=200, interval=50, blit=True, repeat=False
        )
        
        ax.legend(loc='upper right')
        ani.save("javelin.gif", writer="pillow", fps=12)
        plt.show()

    # --- Button click handler ---
    def inc():
        try:
            height = float(height_entry.get())
            speed = float(speed_entry.get())
            angle_deg = float(angle_entry.get())
            angle_rad = np.radians(angle_deg)

            if height < 0:
                messagebox.showerror("Error", "Height must be non-negative!")
                return
            if speed <= 0:
                messagebox.showerror("Error", "Speed must be greater than 0!")
                return

            animate_projectile(height, speed, angle_rad)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")

    # --- Start Simulation button ---
    button = tk.Button(window, text="Start Simulation", command=inc, 
                      bg='green', fg='white', font=('Arial', 12, 'bold'))
    button.pack(pady=15)
    window.mainloop()

start()