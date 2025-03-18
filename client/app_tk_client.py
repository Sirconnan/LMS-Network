import tkinter as tk

class Lms_network:
    
    __nb_client = 0
    
    def __init__(self):
        self.gui = tk.Tk()
        
    
    def run_graphique(self):
        self.gui.config(bg='skyblue')
        self.gui.title("LMS Network")
        self.gui.geometry("1000x500")
        self.gui.mainloop()
        
    def start_new_client():
        Lms_network.__nb_client += 1
        
        numero_client = Lms_network.__nb_client
        instance_client = Lms_network()
        instance_client.run_graphique()
        
        
        label_def_title = tk.Label(self.gui, 
                               text="Veuillez choisir une adresse IP ou un nom de domaine du serveur cible :", 
                               bg='skyblue', 
                               font=("Arial", 14))
        label_def_title.pack(pady=20)

       
        self.label_def_input = tk.Entry(self.gui, font=("Arial", 14), width=50)
        self.label_def_input.pack(pady=10)


        submit_button = tk.Button(self.gui, text="Valider", command=self.get_input, font=("Arial", 12))
        submit_button.pack(pady=20)
        

    def get_input(self):
        user_input = self.input_start.get()
        print(f"Adresse saisie : {user_input}")  
    
instance1 = Lms_network()
tk.Button(instance1.gui, text="Crée un nouveaux client", command=Lms_network.start_new_client()).pack(pady=20)
instance1.run_graphique()
