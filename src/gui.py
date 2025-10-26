import tkinter as tk
from tkinter import messagebox
import json
from agent import generate_video_for_knowledge_point

def run_agent():
    api_key = api_key_entry.get()
    gemini_api_key = gemini_api_key_entry.get()
    knowledge_point = knowledge_point_entry.get()

    if not api_key or not gemini_api_key or not knowledge_point:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    config = {
        "api_key": api_key,
        "gemini_api_key": gemini_api_key
    }

    config_path = 'gpt_config.json'
    with open(config_path, 'w') as f:
        json.dump(config, f)

    try:
        generate_video_for_knowledge_point(knowledge_point)
        messagebox.showinfo("Success", "Video generation complete!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Code2Video")

tk.Label(root, text="OpenAI API Key:").grid(row=0, column=0, padx=10, pady=5)
api_key_entry = tk.Entry(root, width=50)
api_key_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Gemini API Key:").grid(row=1, column=0, padx=10, pady=5)
gemini_api_key_entry = tk.Entry(root, width=50)
gemini_api_key_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Knowledge Point:").grid(row=2, column=0, padx=10, pady=5)
knowledge_point_entry = tk.Entry(root, width=50)
knowledge_point_entry.grid(row=2, column=1, padx=10, pady=5)

run_button = tk.Button(root, text="Generate Video", command=run_agent)
run_button.grid(row=3, columnspan=2, pady=10)

root.mainloop()
