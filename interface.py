import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

from modelos import (
    Processador, PlacaDeVideo, MemoriaRAM, Monitor, MonitorGamer,
    ComputadorOffice, ComputadorGamer, ComputadorIntermediario
)

class InventarioApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Inventário de Computadores")
        self.geometry("800x600")
        
        self.lista_computadores = []
        self.item_selecionado_index = None
        self.cpu_ultima_geracao_var = tk.BooleanVar(value=False)
        self.cpu_hyper_var = tk.BooleanVar(value=False)

        self.campos_especificos_map = {
            'ComputadorOffice': ['SSD (GB)', 'Fonte (W)', 'Monitor Marca', 'Monitor Modelo', 'Monitor Polegadas (")', 'Monitor Frequência (Hz)'],
            'ComputadorGamer': ['GPU Fabricante', 'GPU Modelo', 'GPU VRAM (GB)', 'Fonte (W)', 'Monitor Marca', 'Monitor Modelo', 'Monitor Polegadas (")', 'Monitor Frequência (Hz)'],
            'ComputadorIntermediario': ['GPU Fabricante', 'GPU Modelo', 'GPU VRAM (GB)', 'Fonte (W)', 'Monitor Marca', 'Monitor Modelo', 'Monitor Polegadas (")', 'Monitor Frequência (Hz)']
        }
        self.labels_e_entradas = {}

        self._criar_widgets()
        self._atualizar_lista()

    def _criar_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        form_frame = ttk.LabelFrame(main_frame, text="Adicionar/Editar Computador", padding="10")
        form_frame.pack(fill="x", pady=5)
        
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)
        form_frame.columnconfigure(5, weight=1)

        campos_comuns = {
            'Tipo': ttk.Combobox(form_frame, values=list(self.campos_especificos_map.keys()), state="readonly"),
            'Tag de Identificação': ttk.Entry(form_frame),
            'CPU Fabricante': ttk.Combobox(form_frame, values=['AMD', 'INTEL'], state='readonly'),
            'CPU Modelo': ttk.Combobox(form_frame, values=[], state='readonly'),
            'CPU Núcleos': ttk.Entry(form_frame),
            'CPU Última Geração': ttk.Checkbutton(form_frame, variable=self.cpu_ultima_geracao_var, text='Última Geração (E/P)'),
            'CPU Núcleos Performance': ttk.Entry(form_frame),
            'CPU Núcleos Eficiência': ttk.Entry(form_frame),
            'CPU Hyperthread': ttk.Checkbutton(form_frame, variable=self.cpu_hyper_var, text='Hyperthread/SMT (duplicar threads)'),
            'RAM (GB)': ttk.Entry(form_frame),
            'RAM (MHz)': ttk.Entry(form_frame),
        }
        campos_especificos = {
            'SSD (GB)': ttk.Entry(form_frame),
            'GPU Fabricante': ttk.Combobox(form_frame, values=['AMD', 'NVIDIA', 'INTEL'], state='readonly'),
            'GPU Modelo': ttk.Entry(form_frame),
            'GPU VRAM (GB)': ttk.Entry(form_frame),
            'Fonte (W)': ttk.Entry(form_frame),
        }

        row = 0
        ttk.Label(form_frame, text="Tipo:").grid(row=row, column=0, padx=5, pady=5, sticky="w")
        campos_comuns['Tipo'].grid(row=row, column=1, columnspan=5, padx=5, pady=5, sticky="ew")
        self.labels_e_entradas['Tipo'] = {'label': None, 'widget': campos_comuns['Tipo']}
        
        row += 1
        ttk.Label(form_frame, text="Tag de Identificação:").grid(row=row, column=0, padx=5, pady=5, sticky="w")
        campos_comuns['Tag de Identificação'].grid(row=row, column=1, columnspan=5, padx=5, pady=5, sticky="ew")
        self.labels_e_entradas['Tag de Identificação'] = {'label': None, 'widget': campos_comuns['Tag de Identificação']}
        
        row += 1
        ttk.Separator(form_frame, orient='horizontal').grid(row=row, column=0, columnspan=6, sticky='ew', pady=10)
        row += 1
        
        lbl_cpu_fab = ttk.Label(form_frame, text="CPU Fabricante:")
        lbl_cpu_fab.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        campos_comuns['CPU Fabricante'].grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        self.labels_e_entradas['CPU Fabricante'] = {'label': lbl_cpu_fab, 'widget': campos_comuns['CPU Fabricante']}

        lbl_cpu_modelo = ttk.Label(form_frame, text="CPU Modelo:")
        lbl_cpu_modelo.grid(row=row, column=2, padx=5, pady=5, sticky="w")
        campos_comuns['CPU Modelo'].grid(row=row, column=3, padx=5, pady=5, sticky="ew")
        self.labels_e_entradas['CPU Modelo'] = {'label': lbl_cpu_modelo, 'widget': campos_comuns['CPU Modelo']}

        lbl_cpu_nucleos = ttk.Label(form_frame, text="CPU Núcleos:")
        lbl_cpu_nucleos.grid(row=row, column=4, padx=5, pady=5, sticky="w")
        campos_comuns['CPU Núcleos'].grid(row=row, column=5, padx=5, pady=5, sticky="ew")
        self.labels_e_entradas['CPU Núcleos'] = {'label': lbl_cpu_nucleos, 'widget': campos_comuns['CPU Núcleos']}

        # Campos para Intel última geração (núcleos performance/eficiência)
        lbl_cpu_ultima = ttk.Label(form_frame, text="Intel - Última Geração:")
        lbl_cpu_ultima.grid(row=row+1, column=0, padx=5, pady=5, sticky="w")
        campos_comuns['CPU Última Geração'].grid(row=row+1, column=1, padx=5, pady=5, sticky="w")
        self.labels_e_entradas['CPU Última Geração'] = {'label': lbl_cpu_ultima, 'widget': campos_comuns['CPU Última Geração']}

        lbl_cpu_perf = ttk.Label(form_frame, text="Núcleos Performance:")
        lbl_cpu_perf.grid(row=row+1, column=2, padx=5, pady=5, sticky="w")
        campos_comuns['CPU Núcleos Performance'].grid(row=row+1, column=3, padx=5, pady=5, sticky="ew")
        self.labels_e_entradas['CPU Núcleos Performance'] = {'label': lbl_cpu_perf, 'widget': campos_comuns['CPU Núcleos Performance']}

        lbl_cpu_eff = ttk.Label(form_frame, text="Núcleos Eficiência:")
        lbl_cpu_eff.grid(row=row+1, column=4, padx=5, pady=5, sticky="w")
        campos_comuns['CPU Núcleos Eficiência'].grid(row=row+1, column=5, padx=5, pady=5, sticky="ew")
        self.labels_e_entradas['CPU Núcleos Eficiência'] = {'label': lbl_cpu_eff, 'widget': campos_comuns['CPU Núcleos Eficiência']}
        # adicionar opção Hyperthread/SMT logo abaixo dos campos de CPU (visível quando não-última geração)
        lbl_cpu_hyper = ttk.Label(form_frame, text="Hyperthread/SMT:")
        lbl_cpu_hyper.grid(row=row+2, column=0, padx=5, pady=5, sticky="w")
        campos_comuns['CPU Hyperthread'].grid(row=row+2, column=1, padx=5, pady=5, sticky="w")
        self.labels_e_entradas['CPU Hyperthread'] = {'label': lbl_cpu_hyper, 'widget': campos_comuns['CPU Hyperthread']}
        # avançar a linha base para os próximos campos
        row = row + 3
        lbl_ram_gb = ttk.Label(form_frame, text="RAM (GB):")
        lbl_ram_gb.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        campos_comuns['RAM (GB)'].grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        self.labels_e_entradas['RAM (GB)'] = {'label': lbl_ram_gb, 'widget': campos_comuns['RAM (GB)']}
        
        lbl_ram_mhz = ttk.Label(form_frame, text="RAM (MHz):")
        lbl_ram_mhz.grid(row=row, column=2, padx=5, pady=5, sticky="w")
        campos_comuns['RAM (MHz)'].grid(row=row, column=3, padx=5, pady=5, sticky="ew")
        self.labels_e_entradas['RAM (MHz)'] = {'label': lbl_ram_mhz, 'widget': campos_comuns['RAM (MHz)']}
        
        row += 1
        ttk.Separator(form_frame, orient='horizontal').grid(row=row, column=0, columnspan=6, sticky='ew', pady=10)
        row += 1

        lbl_ssd = ttk.Label(form_frame, text="SSD (GB):")
        lbl_ssd.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        campos_especificos['SSD (GB)'].grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        self.labels_e_entradas['SSD (GB)'] = {'label': lbl_ssd, 'widget': campos_especificos['SSD (GB)']}
        
        row += 1
        lbl_gpu_fab = ttk.Label(form_frame, text="GPU Fabricante:")
        lbl_gpu_fab.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        campos_especificos['GPU Fabricante'].grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        self.labels_e_entradas['GPU Fabricante'] = {'label': lbl_gpu_fab, 'widget': campos_especificos['GPU Fabricante']}

        lbl_gpu_modelo = ttk.Label(form_frame, text="GPU Modelo:")
        lbl_gpu_modelo.grid(row=row, column=2, padx=5, pady=5, sticky="w")
        campos_especificos['GPU Modelo'].grid(row=row, column=3, padx=5, pady=5, sticky="ew")
        self.labels_e_entradas['GPU Modelo'] = {'label': lbl_gpu_modelo, 'widget': campos_especificos['GPU Modelo']}

        lbl_gpu_vram = ttk.Label(form_frame, text="GPU VRAM (GB):")
        lbl_gpu_vram.grid(row=row, column=4, padx=5, pady=5, sticky="w")
        campos_especificos['GPU VRAM (GB)'].grid(row=row, column=5, padx=5, pady=5, sticky="ew")
        self.labels_e_entradas['GPU VRAM (GB)'] = {'label': lbl_gpu_vram, 'widget': campos_especificos['GPU VRAM (GB)']}
        row += 1
        lbl_fonte = ttk.Label(form_frame, text="Fonte (W):")
        lbl_fonte.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        campos_especificos['Fonte (W)'].grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        self.labels_e_entradas['Fonte (W)'] = {'label': lbl_fonte, 'widget': campos_especificos['Fonte (W)']}
        
        row += 1
        ttk.Separator(form_frame, orient='horizontal').grid(row=row, column=0, columnspan=6, sticky='ew', pady=10)
        row += 1

        lbl_mon_marca = ttk.Label(form_frame, text="Monitor Marca:")
        lbl_mon_marca.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        entry_mon_marca = ttk.Entry(form_frame)
        entry_mon_marca.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        self.labels_e_entradas['Monitor Marca'] = {'label': lbl_mon_marca, 'widget': entry_mon_marca}

        lbl_mon_modelo = ttk.Label(form_frame, text="Monitor Modelo:")
        lbl_mon_modelo.grid(row=row, column=2, padx=5, pady=5, sticky="w")
        entry_mon_modelo = ttk.Entry(form_frame)
        entry_mon_modelo.grid(row=row, column=3, padx=5, pady=5, sticky="ew")
        self.labels_e_entradas['Monitor Modelo'] = {'label': lbl_mon_modelo, 'widget': entry_mon_modelo}

        row += 1
        lbl_mon_pol = ttk.Label(form_frame, text="Monitor Polegadas (\"):")
        lbl_mon_pol.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        entry_mon_pol = ttk.Entry(form_frame)
        entry_mon_pol.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        self.labels_e_entradas['Monitor Polegadas (")'] = {'label': lbl_mon_pol, 'widget': entry_mon_pol}

        lbl_mon_hz = ttk.Label(form_frame, text="Monitor Frequência (Hz):")
        lbl_mon_hz.grid(row=row, column=2, padx=5, pady=5, sticky="w")
        entry_mon_hz = ttk.Entry(form_frame)
        entry_mon_hz.grid(row=row, column=3, padx=5, pady=5, sticky="ew")
        # pré-preencher frequência padrão de 60Hz
        try:
            entry_mon_hz.insert(0, '60')
        except Exception:
            pass
        self.labels_e_entradas['Monitor Frequência (Hz)'] = {'label': lbl_mon_hz, 'widget': entry_mon_hz}

        self.labels_e_entradas['Tipo']['widget'].bind("<<ComboboxSelected>>", self._atualizar_campos_especificos)
        # Bindings para atualizar campos de CPU quando fabricante ou opção de geração mudar
        self.labels_e_entradas['CPU Fabricante']['widget'].bind("<<ComboboxSelected>>", self._atualizar_campos_cpu)
        # Bind para modelo: nada necessário, mas manter referência
        # variáveis Tkinter: usar trace para reagir a mudanças
        try:
            self.cpu_ultima_geracao_var.trace_add('write', lambda *args: self._atualizar_campos_cpu())
        except Exception:
            # fallback para versões mais antigas
            self.cpu_ultima_geracao_var.trace('w', lambda *args: self._atualizar_campos_cpu())
        # também reagir a mudanças no fabricante do GPU (não obrigatório)
        
        row += 1
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=row, column=0, columnspan=6, pady=10)
        
        ttk.Button(button_frame, text="Adicionar", command=self._adicionar_computador).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Atualizar Selecionado", command=self._atualizar_computador).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Limpar Campos", command=self._limpar_campos).pack(side="left", padx=5)
        
        list_frame = ttk.LabelFrame(main_frame, text="Inventário de Computadores", padding="10")
        list_frame.pack(fill="both", expand=True, pady=5)
        
        self.lista_widget = tk.Text(list_frame, wrap="none", height=15)
        self.lista_widget.pack(side="left", fill="both", expand=True)
        
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.lista_widget.yview)
        v_scrollbar.pack(side="right", fill="y")
        self.lista_widget.config(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=self.lista_widget.xview)
        h_scrollbar.pack(fill="x", pady=2)
        self.lista_widget.config(xscrollcommand=h_scrollbar.set)
        
        self.lista_widget.tag_configure("selected", background="lightblue")
        self.lista_widget.bind('<ButtonRelease-1>', self._item_selecionado)
        
        list_button_frame = ttk.Frame(main_frame)
        list_button_frame.pack(fill="x", pady=5)

        # Removido: botão 'Remover Selecionado' e 'Carregar de Arquivo' conforme solicitado.
        ttk.Button(list_button_frame, text="Salvar em Arquivo", command=self._salvar_arquivo).pack(side="right", padx=5)

        self._atualizar_campos_especificos()

    def _get_valor(self, nome_campo, tipo=str, obrigatorio=True):
        """Função utilitária para ler e validar campos."""
        try:
            # special-case para checkbox/variáveis que não usam .get()
            if nome_campo == 'CPU Última Geração':
                return bool(self.cpu_ultima_geracao_var.get())
            if nome_campo == 'CPU Hyperthread':
                return bool(self.cpu_hyper_var.get())

            widget = self.labels_e_entradas[nome_campo]['widget']
            # Alguns widgets (Checkbutton) não possuem get(); entries/combobox têm
            try:
                valor = widget.get()
            except Exception:
                # se não conseguir, tenta ler a var associada
                valor = None
            
            if not widget.winfo_ismapped() and obrigatorio:
                # MUDANÇA AQUI
                campos_comuns = ['Tipo', 'Tag de Identificação', 'CPU Fabricante', 'CPU Modelo', 'CPU Núcleos', 'RAM (GB)', 'RAM (MHz)']
                if nome_campo in campos_comuns:
                     raise ValueError(f"Campo '{nome_campo}' é obrigatório.")
                else:
                    return None
            
            if not valor and obrigatorio:
                raise ValueError(f"Campo '{nome_campo}' é obrigatório.")
            
            if not valor and not obrigatorio:
                return None

            return tipo(valor)
        except (ValueError, TypeError):
            raise ValueError(f"Campo '{nome_campo}' deve ser do tipo {tipo.__name__}.")
        except KeyError:
            if obrigatorio:
                raise ValueError(f"Campo '{nome_campo}' não encontrado.")
            return None

    def _atualizar_campos_especificos(self, event=None):
        """Mostra/esconde os campos de entrada com base no tipo de computador selecionado."""
        tipo_selecionado = self.labels_e_entradas['Tipo']['widget'].get()
        
        for campos_lista in self.campos_especificos_map.values():
            for label_text in campos_lista:
                if label_text in self.labels_e_entradas:
                    self.labels_e_entradas[label_text]['label'].grid_remove()
                    self.labels_e_entradas[label_text]['widget'].grid_remove()

        if tipo_selecionado in self.campos_especificos_map:
            for label_text in self.campos_especificos_map[tipo_selecionado]:
                if label_text in self.labels_e_entradas:
                    self.labels_e_entradas[label_text]['label'].grid()
                    self.labels_e_entradas[label_text]['widget'].grid()

        self._atualizar_campos_cpu()

    def _atualizar_campos_cpu(self, event=None):
        """Mostra/esconde campos de CPU conforme fabricante e flag de última geração."""
        try:
            fabricante = self.labels_e_entradas['CPU Fabricante']['widget'].get()
        except Exception:
            fabricante = ''

        ultima = bool(self.cpu_ultima_geracao_var.get())

        try:
            tipo_selecionado = self.labels_e_entradas['Tipo']['widget'].get()
        except Exception:
            tipo_selecionado = ''

        models = []
        if fabricante.upper() == 'AMD':
            if tipo_selecionado == 'ComputadorOffice':
                models = ['Ryzen 3', 'Ryzen 5']
            else:
                models = ['Ryzen 3', 'Ryzen 5', 'Ryzen 7', 'Ryzen 9']
        elif fabricante.upper() == 'INTEL' and ultima:
            if tipo_selecionado == 'ComputadorOffice':
                models = ['Core Ultra 3', 'Core Ultra 5']
            else:
                models = ['Core Ultra 3', 'Core Ultra 5', 'Core Ultra 7', 'Core Ultra 9']
        elif fabricante.upper() == 'INTEL':
            if tipo_selecionado == 'ComputadorOffice':
                models = ['i3', 'i5']
            else:
                models = ['i3', 'i5', 'i7', 'i9']
        else:
            models = []
        try:
            comb = self.labels_e_entradas['CPU Modelo']['widget']
            comb['values'] = models
        except Exception:
            pass

        if fabricante.upper() == 'INTEL' and ultima:
            # esconder campo único de núcleos
            if 'CPU Núcleos' in self.labels_e_entradas:
                self.labels_e_entradas['CPU Núcleos']['label'].grid_remove()
                self.labels_e_entradas['CPU Núcleos']['widget'].grid_remove()

            # mostrar perf/eff
            for key in ('CPU Núcleos Performance', 'CPU Núcleos Eficiência', 'CPU Última Geração'):
                if key in self.labels_e_entradas:
                    self.labels_e_entradas[key]['label'].grid()
                    self.labels_e_entradas[key]['widget'].grid()
        else:
            # mostrar campo único de núcleos
            if 'CPU Núcleos' in self.labels_e_entradas:
                self.labels_e_entradas['CPU Núcleos']['label'].grid()
                self.labels_e_entradas['CPU Núcleos']['widget'].grid()

            # esconder perf/eff
            for key in ('CPU Núcleos Performance', 'CPU Núcleos Eficiência'):
                if key in self.labels_e_entradas:
                    self.labels_e_entradas[key]['label'].grid_remove()
                    self.labels_e_entradas[key]['widget'].grid_remove()
            # mostrar/ocultar checkbox de última geração (se for Intel, mostrar; caso contrário, esconder)
            if fabricante.upper() == 'INTEL':
                if 'CPU Última Geração' in self.labels_e_entradas:
                    self.labels_e_entradas['CPU Última Geração']['label'].grid()
                    self.labels_e_entradas['CPU Última Geração']['widget'].grid()
            else:
                if 'CPU Última Geração' in self.labels_e_entradas:
                    self.labels_e_entradas['CPU Última Geração']['label'].grid_remove()
                    self.labels_e_entradas['CPU Última Geração']['widget'].grid_remove()

        # Mostrar/ocultar checkbox Hyperthread: exibir quando NÃO for última geração e fabricante for AMD ou INTEL
        if fabricante.upper() in ('AMD', 'INTEL') and not ultima:
            if 'CPU Hyperthread' in self.labels_e_entradas:
                self.labels_e_entradas['CPU Hyperthread']['label'].grid()
                self.labels_e_entradas['CPU Hyperthread']['widget'].grid()
        else:
            if 'CPU Hyperthread' in self.labels_e_entradas:
                self.labels_e_entradas['CPU Hyperthread']['label'].grid_remove()
                self.labels_e_entradas['CPU Hyperthread']['widget'].grid_remove()

    def _adicionar_computador(self):
        try:
            tipo = self._get_valor('Tipo')
            
            # Construção do processador: suporta fabricante e modo Intel última geração (E/P cores)
            cpu_modelo = self._get_valor('CPU Modelo')
            cpu_fabricante = self._get_valor('CPU Fabricante')
            cpu_ultima = bool(self.cpu_ultima_geracao_var.get())
            # decidir criação do processador conforme fabricante/geração/hyperthread
            if str(cpu_fabricante).upper() == 'INTEL' and cpu_ultima:
                perf = self._get_valor('CPU Núcleos Performance', tipo=int)
                eff = self._get_valor('CPU Núcleos Eficiência', tipo=int)
                cpu = Processador(modelo=cpu_modelo, fabricante=cpu_fabricante, ultima_geracao=True, perf_cores=perf, eff_cores=eff)
            else:
                nucleos = self._get_valor('CPU Núcleos', tipo=int)
                hyper = bool(self.cpu_hyper_var.get())
                cpu = Processador(modelo=cpu_modelo, fabricante=cpu_fabricante, nucleos=nucleos, hyperthread=hyper)
            ram = MemoriaRAM(
                capacidade_gb=self._get_valor('RAM (GB)', tipo=int),
                velocidade_mhz=self._get_valor('RAM (MHz)', tipo=int)
            )
            
            novo_computador = None
            tag = self._get_valor('Tag de Identificação')
            
            if tipo == "ComputadorOffice":
                ssd = self._get_valor('SSD (GB)', tipo=int)
                # criar monitor simples para Office
                mon_marca = self._get_valor('Monitor Marca')
                mon_modelo = self._get_valor('Monitor Modelo', obrigatorio=False) or 'Standard'
                mon_polegadas = self._get_valor('Monitor Polegadas (")', tipo=float)
                # leitura da frequência (se o usuário modificou); default 60
                mon_freq = self._get_valor('Monitor Frequência (Hz)', tipo=int, obrigatorio=False) or 60
                novo_monitor = Monitor(marca=mon_marca, modelo=mon_modelo, tamanho_polegadas=mon_polegadas, frequencia_hz=mon_freq)
                novo_computador = ComputadorOffice(tag, cpu, ram, ssd, novo_monitor)
                
            # Em _adicionar_computador, SUBSTITUA o bloco "elif tipo == 'ComputadorGamer'" por este:

            elif tipo == "ComputadorGamer":
                gpu = PlacaDeVideo(
                    modelo=self._get_valor('GPU Modelo'),
                    memoria_vram=self._get_valor('GPU VRAM (GB)', tipo=int),
                    fabricante=self._get_valor('GPU Fabricante')
                )
                fonte = self._get_valor('Fonte (W)', tipo=int)
                
                monitor = MonitorGamer(
                    marca=self._get_valor('Monitor Marca'),
                    modelo=self._get_valor('Monitor Modelo'),
                    tamanho_polegadas=self._get_valor('Monitor Polegadas (")', tipo=float),
                    frequencia_hz=self._get_valor('Monitor Frequência (Hz)', tipo=int)
                )

                novo_computador = ComputadorGamer(tag, cpu, ram, gpu, fonte, monitor)
                
            elif tipo == "ComputadorIntermediario":
                gpu = PlacaDeVideo(
                    modelo=self._get_valor('GPU Modelo'),
                    memoria_vram=self._get_valor('GPU VRAM (GB)', tipo=int),
                    fabricante=self._get_valor('GPU Fabricante')
                )
                # criar monitor simples para Intermediário
                mon_marca = self._get_valor('Monitor Marca')
                mon_modelo = self._get_valor('Monitor Modelo', obrigatorio=False) or 'Standard'
                mon_polegadas = self._get_valor('Monitor Polegadas (")', tipo=float)
                mon_freq = self._get_valor('Monitor Frequência (Hz)', tipo=int, obrigatorio=False) or 60
                novo_monitor = Monitor(marca=mon_marca, modelo=mon_modelo, tamanho_polegadas=mon_polegadas, frequencia_hz=mon_freq)
                novo_computador = ComputadorIntermediario(tag, cpu, ram, gpu, novo_monitor)
            
            if novo_computador:
                if self.item_selecionado_index is None:
                    for comp in self.lista_computadores:
                        if comp.tag_identificacao.lower() == tag.lower():
                            raise ValueError(f"A tag '{tag}' já está em uso. Use uma tag única.")
                
                self.lista_computadores.append(novo_computador)
                self._atualizar_lista()
                self._limpar_campos()
                
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", f"Dado inválido: {e}")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

    def _atualizar_lista(self):
        self.lista_widget.config(state=tk.NORMAL)
        self.lista_widget.delete('1.0', tk.END)
        for i, comp in enumerate(self.lista_computadores):
            info = comp.get_info_completa()
            tag = f"item_{i}"
            self.lista_widget.tag_configure(f"header_{i}", font=("TkDefaultFont", 10, "bold"))
            self.lista_widget.insert(tk.END, f"--- Item {i+1} ---\n", (f"header_{i}", tag))
            self.lista_widget.insert(tk.END, f"{info}\n\n", (tag,))
        self.lista_widget.config(state=tk.DISABLED)
        self.item_selecionado_index = None

    def _limpar_campos(self):
        for data in self.labels_e_entradas.values():
            if data['widget']:
                widget = data['widget']
                if isinstance(widget, ttk.Entry):
                    widget.delete(0, tk.END)
                elif isinstance(widget, ttk.Combobox):
                    widget.set('')
        try:
            self.labels_e_entradas['CPU Fabricante']['widget'].set('')
        except Exception:
            pass
        try:
            if 'GPU Fabricante' in self.labels_e_entradas:
                self.labels_e_entradas['GPU Fabricante']['widget'].set('')
        except Exception:
            pass
        try:
            self.cpu_ultima_geracao_var.set(False)
        except Exception:
            pass
        try:
            self.cpu_hyper_var.set(False)
        except Exception:
            pass
        try:
            if 'CPU Núcleos Performance' in self.labels_e_entradas:
                self.labels_e_entradas['CPU Núcleos Performance']['widget'].delete(0, tk.END)
            if 'CPU Núcleos Eficiência' in self.labels_e_entradas:
                self.labels_e_entradas['CPU Núcleos Eficiência']['widget'].delete(0, tk.END)
        except Exception:
            pass

        # Garantir que a frequência do monitor volte para 60 após limpar
        try:
            if 'Monitor Frequência (Hz)' in self.labels_e_entradas:
                w = self.labels_e_entradas['Monitor Frequência (Hz)']['widget']
                try:
                    w.delete(0, tk.END)
                except Exception:
                    pass
                try:
                    w.insert(0, '60')
                except Exception:
                    pass
        except Exception:
            pass

        self.item_selecionado_index = None
        self.lista_widget.tag_remove("selected", '1.0', tk.END)
        self._atualizar_campos_especificos()

    def _item_selecionado(self, event):
        try:
            index_str = self.lista_widget.tag_names(tk.CURRENT)[-1]
            if not index_str.startswith("item_"):
                return
            self.item_selecionado_index = int(index_str.split('_')[1])
            
            self.lista_widget.tag_remove("selected", '1.0', tk.END)
            self.lista_widget.tag_add("selected", f"item_{self.item_selecionado_index}.first linestart", f"item_{self.item_selecionado_index}.last lineend")

            comp = self.lista_computadores[self.item_selecionado_index]
        except (IndexError, TypeError, ValueError):
            self.item_selecionado_index = None
            return
        
        self._limpar_campos()
        
        self.labels_e_entradas['Tipo']['widget'].set(comp.__class__.__name__)
        self.labels_e_entradas['Tag de Identificação']['widget'].insert(0, comp.tag_identificacao)
        try:
            self.labels_e_entradas['CPU Fabricante']['widget'].set(comp.processador.fabricante)
        except Exception:
            pass
        self.labels_e_entradas['CPU Modelo']['widget'].insert(0, comp.processador.modelo)

        try:
            self.cpu_ultima_geracao_var.set(bool(getattr(comp.processador, 'ultima_geracao', False)))
        except Exception:
            pass
        self._atualizar_campos_cpu()

        if getattr(comp.processador, 'fabricante', '').upper() == 'INTEL' and getattr(comp.processador, 'ultima_geracao', False):
            # preencher campos performance/eff
            try:
                self.labels_e_entradas['CPU Núcleos Performance']['widget'].insert(0, str(comp.processador.perf_cores))
                self.labels_e_entradas['CPU Núcleos Eficiência']['widget'].insert(0, str(comp.processador.eff_cores))
            except Exception:
                pass
        else:
            try:
                self.labels_e_entradas['CPU Núcleos']['widget'].insert(0, str(comp.processador.nucleos))
            except Exception:
                pass
        # definir hyperthread quando aplicável
        try:
            self.cpu_hyper_var.set(bool(getattr(comp.processador, 'hyperthread', False)))
        except Exception:
            pass
        self.labels_e_entradas['RAM (GB)']['widget'].insert(0, str(comp.memoria_ram.capacidade_gb))
        self.labels_e_entradas['RAM (MHz)']['widget'].insert(0, str(comp.memoria_ram.velocidade_mhz))
        
        if isinstance(comp, ComputadorOffice):
            self.labels_e_entradas['SSD (GB)']['widget'].insert(0, str(comp.capacidade_ssd_gb))
            try:
                self.labels_e_entradas['Monitor Marca']['widget'].insert(0, comp.monitor.marca)
                self.labels_e_entradas['Monitor Modelo']['widget'].insert(0, comp.monitor.modelo)
                self.labels_e_entradas['Monitor Polegadas (")']['widget'].insert(0, str(comp.monitor.tamanho_polegadas))
                self.labels_e_entradas['Monitor Frequência (Hz)']['widget'].insert(0, str(comp.monitor.frequencia_hz))
            except Exception:
                pass
        elif isinstance(comp, ComputadorGamer):
                try:
                    self.labels_e_entradas['GPU Fabricante']['widget'].set(comp.placa_de_video.fabricante)
                except Exception:
                    pass
                self.labels_e_entradas['GPU Modelo']['widget'].insert(0, str(comp.placa_de_video.modelo))
                self.labels_e_entradas['GPU VRAM (GB)']['widget'].insert(0, str(comp.placa_de_video.memoria_vram))
                self.labels_e_entradas['Fonte (W)']['widget'].insert(0, str(comp.potencia_fonte_w))
                
                self.labels_e_entradas['Monitor Marca']['widget'].insert(0, comp.monitor.marca)
                self.labels_e_entradas['Monitor Modelo']['widget'].insert(0, comp.monitor.modelo)
                self.labels_e_entradas['Monitor Polegadas (")']['widget'].insert(0, str(comp.monitor.tamanho_polegadas))
                self.labels_e_entradas['Monitor Frequência (Hz)']['widget'].insert(0, str(comp.monitor.frequencia_hz))
        elif isinstance(comp, ComputadorIntermediario):
            try:
                self.labels_e_entradas['GPU Fabricante']['widget'].set(comp.placa_de_video.fabricante)
            except Exception:
                pass
            self.labels_e_entradas['GPU Modelo']['widget'].insert(0, str(comp.placa_de_video.modelo))
            self.labels_e_entradas['GPU VRAM (GB)']['widget'].insert(0, str(comp.placa_de_video.memoria_vram))
            try:
                self.labels_e_entradas['Monitor Marca']['widget'].insert(0, comp.monitor.marca)
                self.labels_e_entradas['Monitor Modelo']['widget'].insert(0, comp.monitor.modelo)
                self.labels_e_entradas['Monitor Polegadas (")']['widget'].insert(0, str(comp.monitor.tamanho_polegadas))
                self.labels_e_entradas['Monitor Frequência (Hz)']['widget'].insert(0, str(comp.monitor.frequencia_hz))
            except Exception:
                pass

        self._atualizar_campos_especificos()

    def _atualizar_computador(self):
        if self.item_selecionado_index is None:
            messagebox.showwarning("Aviso", "Nenhum item selecionado para atualizar.")
            return
        
        try:
            self._adicionar_computador() 
            self.lista_computadores.pop(self.item_selecionado_index) 
            novo_item = self.lista_computadores.pop()
            self.lista_computadores.insert(self.item_selecionado_index, novo_item)
            
            self._atualizar_lista()
            self._limpar_campos()
            messagebox.showinfo("Sucesso", "Computador atualizado com sucesso!")
        except (ValueError, IndexError) as e:
            messagebox.showerror("Erro de Atualização", f"Não foi possível atualizar: {e}")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

    def _salvar_arquivo(self):
        """Salva o inventário em um arquivo JSON."""
        try:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Salvar inventário como..."
            )
            if not filepath: return
            
            lista_serializada = [comp.to_dict() for comp in self.lista_computadores]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(lista_serializada, f, indent=4)
            messagebox.showinfo("Sucesso", "Inventário salvo com sucesso!")
        except IOError as e:
            messagebox.showerror("Erro de Arquivo", f"Não foi possível salvar o arquivo: {e}")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao salvar: {e}")