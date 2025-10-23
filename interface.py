import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

from modelos import Processador, PlacaDeVideo, MemoriaRAM

class InventarioApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Inventário de Componentes de PC")
        self.geometry("900x600")
        
        self.inventario = []
        self.item_selecionado_index = None

        self._criar_widgets()
        self._atualizar_lista()

    def _criar_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        form_frame = ttk.LabelFrame(main_frame, text="Adicionar/Editar Componente", padding="10")
        form_frame.pack(fill="x", pady=5)
        
        self.labels_e_entradas = {}
        self.campos_especificos_map = {
            'Processador': ['Núcleos', 'Frequência (GHz)'],
            'PlacaDeVideo': ['Memória VRAM (GB)', 'Tipo de Memória'],
            'MemoriaRAM': ['Capacidade (GB)', 'Velocidade (MHz)']
        }
        
        campos_widgets = {
            'Tipo': ttk.Combobox(form_frame, values=list(self.campos_especificos_map.keys()), state="readonly"),
            'Marca': ttk.Entry(form_frame),
            'Modelo': ttk.Entry(form_frame),
            'Preço (R$)': ttk.Entry(form_frame),
            'Núcleos': ttk.Entry(form_frame),
            'Frequência (GHz)': ttk.Entry(form_frame),
            'Memória VRAM (GB)': ttk.Entry(form_frame),
            'Tipo de Memória': ttk.Entry(form_frame),
            'Capacidade (GB)': ttk.Entry(form_frame),
            'Velocidade (MHz)': ttk.Entry(form_frame)
        }
        
        row = 0
        for label_text, widget in campos_widgets.items():
            label_widget = ttk.Label(form_frame, text=label_text + ":")
            label_widget.grid(row=row, column=0, padx=5, pady=5, sticky="w")
            widget.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
            self.labels_e_entradas[label_text] = {'label': label_widget, 'widget': widget}
            row += 1

        self.labels_e_entradas['Tipo']['widget'].bind("<<ComboboxSelected>>", self._atualizar_campos_especificos)
        
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Adicionar", command=self._adicionar_componente).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Atualizar Selecionado", command=self._atualizar_componente).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Limpar Campos", command=self._limpar_campos).pack(side="left", padx=5)
        
        list_frame = ttk.LabelFrame(main_frame, text="Inventário", padding="10")
        list_frame.pack(fill="both", expand=True, pady=5)
        
        self.lista_box = tk.Listbox(list_frame, selectmode=tk.SINGLE)
        self.lista_box.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.lista_box.yview)
        scrollbar.pack(side="right", fill="y")
        self.lista_box.config(yscrollcommand=scrollbar.set)
        
        self.lista_box.bind('<<ListboxSelect>>', self._item_selecionado)
        
        list_button_frame = ttk.Frame(main_frame)
        list_button_frame.pack(fill="x", pady=5)
        
        ttk.Button(list_button_frame, text="Remover Selecionado", command=self._remover_componente).pack(side="left", padx=5)
        ttk.Button(list_button_frame, text="Salvar em Arquivo", command=self._salvar_arquivo).pack(side="right", padx=5)
        ttk.Button(list_button_frame, text="Carregar de Arquivo", command=self._carregar_arquivo).pack(side="right", padx=5)

        self._atualizar_campos_especificos()

    def _atualizar_campos_especificos(self, event=None):
        """Mostra/esconde os campos de entrada com base no tipo de componente selecionado."""
        tipo_selecionado = self.labels_e_entradas['Tipo']['widget'].get()
        
        for campos_lista in self.campos_especificos_map.values():
            for label_text in campos_lista:
                self.labels_e_entradas[label_text]['label'].grid_remove()
                self.labels_e_entradas[label_text]['widget'].grid_remove()

        if tipo_selecionado in self.campos_especificos_map:
            for label_text in self.campos_especificos_map[tipo_selecionado]:
                self.labels_e_entradas[label_text]['label'].grid()
                self.labels_e_entradas[label_text]['widget'].grid()

    def _adicionar_componente(self):
        try:
            tipo = self.labels_e_entradas['Tipo']['widget'].get()
            if not tipo:
                raise ValueError("Selecione um tipo de componente.")
            
            marca = self.labels_e_entradas['Marca']['widget'].get()
            modelo = self.labels_e_entradas['Modelo']['widget'].get()
            preco = float(self.labels_e_entradas['Preço (R$)']['widget'].get())
            
            novo_componente = None
            if tipo == "Processador":
                nucleos = int(self.labels_e_entradas['Núcleos']['widget'].get())
                frequencia = float(self.labels_e_entradas['Frequência (GHz)']['widget'].get())
                novo_componente = Processador(marca, modelo, preco, nucleos, frequencia)
            elif tipo == "PlacaDeVideo":
                memoria_vram = int(self.labels_e_entradas['Memória VRAM (GB)']['widget'].get())
                tipo_memoria = self.labels_e_entradas['Tipo de Memória']['widget'].get()
                novo_componente = PlacaDeVideo(marca, modelo, preco, memoria_vram, tipo_memoria)
            elif tipo == "MemoriaRAM":
                capacidade = int(self.labels_e_entradas['Capacidade (GB)']['widget'].get())
                velocidade = int(self.labels_e_entradas['Velocidade (MHz)']['widget'].get())
                novo_componente = MemoriaRAM(marca, modelo, preco, capacidade, velocidade)
            
            if novo_componente:
                self.inventario.append(novo_componente)
                self._atualizar_lista()
                self._limpar_campos()
                
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", f"Dado inválido: {e}")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

    def _atualizar_lista(self):
        self.lista_box.delete(0, tk.END)
        for i, componente in enumerate(self.inventario):
            self.lista_box.insert(tk.END, f"{i+1}: [{componente.__class__.__name__}] {componente.get_info()}")

    def _limpar_campos(self):
        for data in self.labels_e_entradas.values():
            widget = data['widget']
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('')
        self.item_selecionado_index = None
        self.lista_box.selection_clear(0, tk.END)
        self._atualizar_campos_especificos()

    def _remover_componente(self):
        if self.item_selecionado_index is None:
            messagebox.showwarning("Aviso", "Nenhum item selecionado para remoção.")
            return
        
        if messagebox.askyesno("Confirmar Remoção", "Tem certeza que deseja remover o item selecionado?"):
            try:
                self.inventario.pop(self.item_selecionado_index)
                self.item_selecionado_index = None
                self._atualizar_lista()
                self._limpar_campos()
            except IndexError:
                messagebox.showerror("Erro", "O item selecionado não existe mais.")
            except Exception as e:
                messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

    def _item_selecionado(self, event=None):
        indices = self.lista_box.curselection()
        if not indices: return
            
        self.item_selecionado_index = indices[0]
        componente = self.inventario[self.item_selecionado_index]
        
        self._limpar_campos()

        self.labels_e_entradas['Tipo']['widget'].set(componente.__class__.__name__)
        self.labels_e_entradas['Marca']['widget'].insert(0, componente.marca)
        self.labels_e_entradas['Modelo']['widget'].insert(0, componente.modelo)
        self.labels_e_entradas['Preço (R$)']['widget'].insert(0, str(componente.preco))
        
        if isinstance(componente, Processador):
            self.labels_e_entradas['Núcleos']['widget'].insert(0, str(componente.nucleos))
            self.labels_e_entradas['Frequência (GHz)']['widget'].insert(0, str(componente.frequencia))
        elif isinstance(componente, PlacaDeVideo):
            self.labels_e_entradas['Memória VRAM (GB)']['widget'].insert(0, str(componente.memoria_vram))
            self.labels_e_entradas['Tipo de Memória']['widget'].insert(0, componente.tipo_memoria)
        elif isinstance(componente, MemoriaRAM):
            self.labels_e_entradas['Capacidade (GB)']['widget'].insert(0, str(componente.capacidade))
            self.labels_e_entradas['Velocidade (MHz)']['widget'].insert(0, str(componente.velocidade))

        self._atualizar_campos_especificos()

    def _atualizar_componente(self):
        if self.item_selecionado_index is None:
            messagebox.showwarning("Aviso", "Nenhum item selecionado para atualizar.")
            return
        try:
            # CORREÇÃO: Acessa os widgets corretamente
            tipo = self.labels_e_entradas['Tipo']['widget'].get()
            marca = self.labels_e_entradas['Marca']['widget'].get()
            modelo = self.labels_e_entradas['Modelo']['widget'].get()
            preco = float(self.labels_e_entradas['Preço (R$)']['widget'].get())
            
            componente_atualizado = None
            if tipo == "Processador":
                nucleos = int(self.labels_e_entradas['Núcleos']['widget'].get())
                frequencia = float(self.labels_e_entradas['Frequência (GHz)']['widget'].get())
                componente_atualizado = Processador(marca, modelo, preco, nucleos, frequencia)
            elif tipo == "PlacaDeVideo":
                memoria_vram = int(self.labels_e_entradas['Memória VRAM (GB)']['widget'].get())
                tipo_memoria = self.labels_e_entradas['Tipo de Memória']['widget'].get()
                componente_atualizado = PlacaDeVideo(marca, modelo, preco, memoria_vram, tipo_memoria)
            elif tipo == "MemoriaRAM":
                capacidade = int(self.labels_e_entradas['Capacidade (GB)']['widget'].get())
                velocidade = int(self.labels_e_entradas['Velocidade (MHz)']['widget'].get())
                componente_atualizado = MemoriaRAM(marca, modelo, preco, capacidade, velocidade)
            
            if componente_atualizado:
                self.inventario[self.item_selecionado_index] = componente_atualizado
                self._atualizar_lista()
                self._limpar_campos()
                messagebox.showinfo("Sucesso", "Componente atualizado com sucesso!")

        except (ValueError, IndexError) as e:
            messagebox.showerror("Erro de Atualização", f"Não foi possível atualizar: {e}")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

    def _salvar_arquivo(self):
        try:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Salvar inventário como..."
            )
            if not filepath: return
            with open(filepath, 'w', encoding='utf-8') as f:
                lista_serializada = [comp.to_dict() for comp in self.inventario]
                json.dump(lista_serializada, f, indent=4)
            messagebox.showinfo("Sucesso", "Inventário salvo com sucesso!")
        except IOError as e: messagebox.showerror("Erro de Arquivo", f"Não foi possível salvar o arquivo: {e}")
        except Exception as e: messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao salvar: {e}")

    def _carregar_arquivo(self):
        try:
            filepath = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Abrir arquivo de inventário..."
            )
            if not filepath: return
            with open(filepath, 'r', encoding='utf-8') as f:
                lista_de_dicts = json.load(f)

            self.inventario.clear()
            
            for data in lista_de_dicts:
                tipo = data.pop('tipo')
                if tipo == 'Processador': self.inventario.append(Processador(**data))
                elif tipo == 'PlacaDeVideo': self.inventario.append(PlacaDeVideo(**data))
                elif tipo == 'MemoriaRAM': self.inventario.append(MemoriaRAM(**data))
            
            self._atualizar_lista()
            self._limpar_campos()
            messagebox.showinfo("Sucesso", "Inventário carregado com sucesso!")
        except FileNotFoundError: messagebox.showerror("Erro", "Arquivo não encontrado.")
        except json.JSONDecodeError: messagebox.showerror("Erro", "Arquivo JSON inválido ou corrompido.")
        except (KeyError, TypeError) as e: messagebox.showerror("Erro de Formato", f"O arquivo parece estar em um formato incorreto. Detalhes: {e}")
        except Exception as e: messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao carregar: {e}")

