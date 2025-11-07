import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

from modelos import Processador, PlacaDeVideo, MemoriaRAM, Monitor, MonitorGamer, Disco
# Carrega as subclasses que herdam da classe computador presente na pasta sub
from sub.computador_office import ComputadorOffice
from sub.computador_gamer import ComputadorGamer
from sub.computador_intermediario import ComputadorIntermediario
from sub.computador_workstation import ComputadorWorkstation

## Configuração do Formulário de cada campo
class InventarioApp(tk.Tk):
    FORM_CONFIG = [
        {'name': 'Tipo', 'type': ttk.Combobox, 'grid': {'row': 0, 'col': 0, 'colspan': 5}, 'options': {'state': 'readonly', 'values': ['ComputadorOffice', 'ComputadorGamer', 'ComputadorIntermediario', 'ComputadorWorkstation']}, 'targets': ['all']},
        {'name': 'Tag de Identificação', 'type': ttk.Entry, 'grid': {'row': 1, 'col': 0, 'colspan': 5}, 'targets': ['all']},
        {'name': 'CPU Fabricante', 'type': ttk.Combobox, 'grid': {'row': 3, 'col': 0}, 'options': {'values': ['AMD', 'INTEL'], 'state': 'readonly'}, 'targets': ['all']},
        {'name': 'CPU Família', 'type': ttk.Combobox, 'grid': {'row': 3, 'col': 2}, 'options': {'state': 'readonly'}, 'targets': ['all']},
        {'name': 'CPU Modelo', 'type': ttk.Combobox, 'grid': {'row': 3, 'col': 4}, 'options': {'state': 'readonly'}, 'targets': ['all']},
        {'name': 'CPU Núcleos', 'type': ttk.Entry, 'grid': {'row': 4, 'col': 0}, 'options': {'state': 'readonly'}, 'targets': ['all']},
        {'name': 'CPU Hyperthread', 'type': ttk.Checkbutton, 'grid': {'row': 4, 'col': 2}, 'options': {'text': 'Hyperthread/SMT', 'state': 'disabled'}, 'targets': ['all']},
        {'name': 'CPU Gráficos Integrados', 'type': ttk.Checkbutton, 'grid': {'row': 4, 'col': 4}, 'options': {'text': 'iGPU', 'state': 'disabled'}, 'targets': ['all']},
        {'name': 'CPU Última Geração', 'type': ttk.Checkbutton, 'grid': {'row': 5, 'col': 0}, 'options': {'text': 'Arquitetura P+E', 'state': 'disabled'}, 'targets': ['all']},
        {'name': 'CPU Núcleos Performance', 'type': ttk.Entry, 'grid': {'row': 5, 'col': 2}, 'options': {'state': 'readonly'}, 'targets': ['all']},
        {'name': 'CPU Núcleos Eficiência', 'type': ttk.Entry, 'grid': {'row': 5, 'col': 4}, 'options': {'state': 'readonly'}, 'targets': ['all']},
        {'name': 'Módulos RAM', 'type': ttk.Combobox, 'grid': {'row': 6, 'col': 0}, 'options': {'values': ['1', '2', '4', '8'], 'state': 'readonly'}, 'targets': ['all']},
        {'name': 'Tamanho por Módulo (GB)', 'type': ttk.Entry, 'grid': {'row': 6, 'col': 2}, 'targets': ['all']},
        {'name': 'RAM (MHz)', 'type': ttk.Entry, 'grid': {'row': 6, 'col': 4}, 'targets': ['all']},
        {'name': 'SSD Tipo', 'type': ttk.Combobox, 'grid': {'row': 8, 'col': 0}, 'options': {'values': ['SSD SATA', 'SSD NVMe'], 'state': 'readonly'}, 'targets': ['all']},
        {'name': 'SSD Capacidade (GB)', 'type': ttk.Entry, 'grid': {'row': 8, 'col': 2}, 'targets': ['all']},
        {'name': 'HD (GB)', 'type': ttk.Entry, 'grid': {'row': 8, 'col': 4}, 'targets': ['all']},
        {'name': 'GPU Fabricante', 'type': ttk.Combobox, 'grid': {'row': 9, 'col': 0}, 'options': {'values': ['AMD', 'NVIDIA', 'INTEL'], 'state': 'readonly'}, 'targets': ['ComputadorGamer', 'ComputadorIntermediario', 'ComputadorWorkstation']},
        {'name': 'GPU Modelo', 'type': ttk.Combobox, 'grid': {'row': 9, 'col': 2}, 'options': {'state': 'readonly'}, 'targets': ['ComputadorGamer', 'ComputadorIntermediario', 'ComputadorWorkstation']},
        {'name': 'GPU VRAM (GB)', 'type': ttk.Entry, 'grid': {'row': 9, 'col': 4}, 'options': {'state': 'readonly'}, 'targets': ['ComputadorGamer', 'ComputadorIntermediario', 'ComputadorWorkstation']},
        {'name': 'Monitor Marca', 'type': ttk.Entry, 'grid': {'row': 11, 'col': 0}, 'targets': ['all']},
        {'name': 'Monitor Modelo', 'type': ttk.Entry, 'grid': {'row': 11, 'col': 2}, 'targets': ['all']},
        {'name': 'Monitor Polegadas (")', 'type': ttk.Entry, 'grid': {'row': 12, 'col': 0}, 'targets': ['all']},
        {'name': 'Monitor Frequência (Hz)', 'type': ttk.Entry, 'grid': {'row': 12, 'col': 2}, 'targets': ['all']},
    ]
    ## Construtor da Interface Gráfica
    def __init__(self):
        super().__init__()
        self.title("Sistema de Inventário de Computadores")
        self.geometry("940x800")
        
        self.lista_computadores = []
        self.item_selecionado_index = None
        self.widgets = {}
        
        self.cpu_ultima_geracao_var = tk.BooleanVar(value=False)
        self.cpu_hyper_var = tk.BooleanVar(value=False)
        self.cpu_integrated_var = tk.BooleanVar(value=False)
        self.gpus_db = self._carregar_gpus()

        self.processadores_db = self._carregar_processadores()
        self._criar_widgets()
        self._atualizar_lista()
        self._update_form_visibility()
    ## Carrega a base de dados de processadores a partir do arquivo JSON
    def _carregar_processadores(self):
        try:
            with open('processadores.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror("Erro Crítico", f"Não foi possível carregar 'processadores.json': {e}")
            self.destroy()
            return []
    ## Carrega a base de dados de GPUs a partir do arquivo JSON
    def _carregar_gpus(self):
        try:
            with open('gpus.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror("Erro Crítico", f"Não foi possível carregar 'gpus.json': {e}")
            return []
    ## Cria os widgets da interface gráfica
    def _criar_widgets(self):
        main_frame = ttk.Frame(self, padding="10") # Frame principal com espaçamento interno.
        main_frame.pack(fill="both", expand=True) # Preenche todo o espaço disponível na janela principal.
        form_frame = ttk.LabelFrame(main_frame, text="Adicionar/Editar Computador", padding="10") # Frame para o formulário de entrada de dados. (Primeiro Titulo do Programa)
        form_frame.pack(fill="x", pady=5)
        #for i in [1, 3, 5]: form_frame.columnconfigure(i, weight=1) # (responsividade) Define que as colunas 1, 3 e 5 podem se expandir, ajustando o tamanho conforme a janela aumenta. 

        for config in self.FORM_CONFIG:
            name, grid_info = config['name'], config['grid']
            label = ttk.Label(form_frame, text=f"{name}:")
            label.grid(row=grid_info['row'], column=grid_info['col'], padx=5, pady=5, sticky="w")
            options = config.get('options', {}).copy()
            if name == 'CPU Última Geração': options['variable'] = self.cpu_ultima_geracao_var
            elif name == 'CPU Hyperthread': options['variable'] = self.cpu_hyper_var
            elif name == 'CPU Gráficos Integrados': options['variable'] = self.cpu_integrated_var
            widget = config['type'](form_frame, **options)
            widget.grid(row=grid_info['row'], column=grid_info['col'] + 1, columnspan=grid_info.get('colspan', 1), sticky="ew", padx=5, pady=5)
            self.widgets[name] = {'label': label, 'widget': widget, 'config': config}

        ttk.Separator(form_frame, orient='horizontal').grid(row=2, column=0, columnspan=6, sticky='ew', pady=10)
        ttk.Separator(form_frame, orient='horizontal').grid(row=7, column=0, columnspan=6, sticky='ew', pady=10)
        ttk.Separator(form_frame, orient='horizontal').grid(row=10, column=0, columnspan=6, sticky='ew', pady=10)
        
        self.widgets['Tipo']['widget'].bind("<<ComboboxSelected>>", self._update_form_visibility)
        self.widgets['CPU Fabricante']['widget'].bind("<<ComboboxSelected>>", self._update_cpu_fields)
        self.widgets['CPU Família']['widget'].bind("<<ComboboxSelected>>", self._update_cpu_fields)
        self.widgets['CPU Modelo']['widget'].bind("<<ComboboxSelected>>", self._update_cpu_fields)
        self.widgets['GPU Fabricante']['widget'].bind("<<ComboboxSelected>>", self._update_gpu_models)
        self.widgets['GPU Modelo']['widget'].bind("<<ComboboxSelected>>", self._update_gpu_vram)
        self.cpu_ultima_geracao_var.trace_add('write', lambda *args: self._update_form_visibility())
        
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=99, column=0, columnspan=6, pady=10)
        ttk.Button(button_frame, text="Adicionar", command=self._adicionar_computador).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Limpar Campos", command=self._limpar_campos).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Carregar Arquivo", command=self._carregar_arquivo).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Salvar em Arquivo", command=self._salvar_arquivo).pack(side="right", padx=5)

        list_frame = ttk.LabelFrame(main_frame, text="Inventário de Computadores", padding="10")
        list_frame.pack(fill="both", expand=True, pady=5)

        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill="x", pady=5)
        ttk.Label(search_frame, text="Buscar TAG:").pack(side="left", padx=(0,6))
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=3, fill="both")
        ttk.Button(search_frame, text="Buscar", command=self._buscar_e_carregar_por_tag).pack(side="left", padx=3)
        ttk.Button(search_frame, text="Editar", command=self._salvar_item).pack(side="left", padx=3)
        ttk.Button(search_frame, text="Excluir", command=self._excluir_por_tag).pack(side="left", padx=3)

        self.lista_widget = tk.Text(list_frame, wrap="none", height=15)
        self.lista_widget.pack(side="left", fill="x", expand=True)
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.lista_widget.yview); v_scrollbar.pack(side="right", fill="y")
        self.lista_widget.config(yscrollcommand=v_scrollbar.set)
        h_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=self.lista_widget.xview); h_scrollbar.pack(fill="x", pady=2)
        self.lista_widget.config(xscrollcommand=h_scrollbar.set)
    ## Métodos Auxiliares
    def _set_widget_state(self, widget_name, state):
        widget = self.widgets[widget_name]['widget']
        widget.config(state=state)
    ## Define o valor de um campo, respeitando seu estado atual
    def _set_field_value(self, widget_name, value, is_manual_mode=False):
        widget = self.widgets[widget_name]['widget']
        current_state = widget.cget('state') # Obtém o estado atual do widget (normal, readonly, disabled)
        if current_state == 'readonly' and not is_manual_mode: # Serve para conseguir deixar o estado normal para fazer modificações
            widget.config(state='normal')
        
        widget.delete(0, tk.END) # Apaga todo o conteúdo atual do campo
        widget.insert(0, str(value)) # Insere o novo valor no campo convertido para string ja que o campo sempre armazena texto.

        if current_state == 'readonly' and not is_manual_mode: # Retorna o estado do widget para readonly se era esse o estado original
            widget.config(state='readonly') 

    ## Atualiza os campos relacionados ao processador com base nas seleções feitas
    def _update_cpu_fields(self, event=None):
        fabricante = self.widgets['CPU Fabricante']['widget'].get()
        familia = self.widgets['CPU Família']['widget'].get()
        modelo = self.widgets['CPU Modelo']['widget'].get()

        if fabricante: # Se o fabricante estiver selecionado, atualiza as famílias disponíveis
            familias = sorted(list(set(p['familia'] for p in self.processadores_db if p['fabricante'] == fabricante)))
            self.widgets['CPU Família']['widget']['values'] = ["Outro"] + familias
        else: # Se o fabricante estiver vazio, limpa as famílias disponíveis
            self.widgets['CPU Família']['widget']['values'] = ["Outro"]
        
        if familia and familia != "Outro": # Se a família estiver selecionada, atualiza os modelos disponíveis
            tipo_selecionado = self.widgets['Tipo']['widget'].get()
            if tipo_selecionado == 'ComputadorOffice':
                modelos = sorted([p['modelo'] for p in self.processadores_db if p['familia'] == familia and p.get('integrated_gpu', False)])
            else:
                modelos = sorted([p['modelo'] for p in self.processadores_db if p['familia'] == familia])
            self.widgets['CPU Modelo']['widget']['values'] = ["Outro"] + modelos
        else: # Se a família estiver vazia ou for "Outro", limpa os modelos disponíveis
            self.widgets['CPU Modelo']['widget']['values'] = ["Outro"]

        if event: # Se o evento for disparado por uma mudança de seleção, limpa os campos dependentes
            if event.widget == self.widgets['CPU Fabricante']['widget']:
                self.widgets['CPU Família']['widget'].set('')
                self.widgets['CPU Modelo']['widget'].set('')
            if event.widget == self.widgets['CPU Família']['widget']:
                self.widgets['CPU Modelo']['widget'].set('')
        # Atualiza os campos de especificações do processador com base no modelo selecionado
        cpu_spec_fields = ['CPU Núcleos', 'CPU Núcleos Performance', 'CPU Núcleos Eficiência']
        cpu_check_fields = ['CPU Hyperthread', 'CPU Última Geração', 'CPU Gráficos Integrados']
        # Se o modelo for "Outro" ou a família for "Outro", habilita a edição manual dos campos
        if modelo == 'Outro' or familia == 'Outro':
            for field in cpu_spec_fields: self._set_widget_state(field, 'normal')
            for field in cpu_check_fields: self._set_widget_state(field, 'normal')
            if event:
                for field in cpu_spec_fields: self._set_field_value(field, '', True)
                self.cpu_hyper_var.set(False)
                self.cpu_ultima_geracao_var.set(False)
                self.cpu_integrated_var.set(False)
        else: # Se um modelo válido for selecionado, preenche os campos com os dados do processador e torna-os somente leitura
            for field in cpu_spec_fields: self._set_widget_state(field, 'readonly')
            for field in cpu_check_fields: self._set_widget_state(field, 'disabled')
            # Preenche os campos com os dados do processador selecionado
            proc_data = next((p for p in self.processadores_db if p['modelo'] == modelo), None)
            if proc_data: # Se encontrar os dados do processador, preenche os campos
                ultima = proc_data.get('ultima_geracao', False)
                self.cpu_ultima_geracao_var.set(ultima)
                self.cpu_hyper_var.set(proc_data.get('hyperthread', False))
                self.cpu_integrated_var.set(proc_data.get('integrated_gpu', False))
                if ultima:
                    perf = int(proc_data.get('perf_cores', 0) or 0)
                    eff = int(proc_data.get('eff_cores', 0) or 0)
                    total = perf + eff
                    self._set_field_value('CPU Núcleos', total)
                    self._set_field_value('CPU Núcleos Performance', perf)
                    self._set_field_value('CPU Núcleos Eficiência', eff)
                else:
                    self._set_field_value('CPU Núcleos', proc_data.get('nucleos', 'N/A'))
                    self._set_field_value('CPU Núcleos Performance', '')
                    self._set_field_value('CPU Núcleos Eficiência', '')
            else: # Se não encontrar os dados do processador, limpa os campos
                for field in cpu_spec_fields: self._set_field_value(field, '')
                self.cpu_hyper_var.set(False)
                self.cpu_ultima_geracao_var.set(False)
        self._update_form_visibility() # Atualiza a visibilidade do formulário
    #  Atualiza em tempo real os modelos de GPU com base no fabricante selecionado
    def _update_gpu_models(self, event=None):
        fab = self.widgets['GPU Fabricante']['widget'].get()
        tipo_selecionado = self.widgets['Tipo']['widget'].get()
        if not fab:
            self.widgets['GPU Modelo']['widget']['values'] = []
            try: self.widgets['GPU Modelo']['widget'].set('')
            except Exception: pass
            return
        if tipo_selecionado == 'ComputadorWorkstation':
            modelos = sorted([g['modelo'] for g in self.gpus_db if g['fabricante'] == fab and g.get('profissional', False)])
        else:
            modelos = sorted([g['modelo'] for g in self.gpus_db if g['fabricante'] == fab and not g.get('profissional', False)])
        self.widgets['GPU Modelo']['widget']['values'] = modelos
        
        if modelos:
            self.widgets['GPU Modelo']['widget'].set(modelos[0])
        else:
            self.widgets['GPU Modelo']['widget'].set('')
        self._update_gpu_vram()
    # Verifica se a GPU selecionada é uma GPU profissional
    def _is_professional_gpu(self, modelo: str, fabricante: str):
        if not modelo or modelo == 'Outro':
            return False
        for g in self.gpus_db:
            if g.get('modelo') == modelo and g.get('fabricante') == fabricante:
                return bool(g.get('profissional', False))
        return False
    # Atualiza o campo de VRAM da GPU com base no modelo e fabricante selecionados
    def _update_gpu_vram(self, event=None):
        try:
            modelo = self.widgets['GPU Modelo']['widget'].get()
            fabricante = self.widgets['GPU Fabricante']['widget'].get()
        except Exception:
            return
        if not modelo or not fabricante: # Se o modelo ou fabricante estiver vazio, limpa o campo de VRAM
            self._set_field_value('GPU VRAM (GB)', '')
        entry = next((g for g in self.gpus_db if g.get('modelo') == modelo and g.get('fabricante') == fabricante), None) # Procura a GPU no banco de dados de gpus, pega o primeiro se achar, ou retorna None se nao achar.
        if entry: # Se achar a GPU no banco de dados, atualiza o campo de VRAM
            vram = entry.get('memoria_vram', '')
            valor_vram = int(vram) if vram != '' else ''
            self._set_field_value('GPU VRAM (GB)', valor_vram)
        else: # Se nao achar a GPU no banco de dados, limpa o campo de VRAM
            if 'GPU VRAM (GB)' in self.widgets:
                self._set_field_value('GPU VRAM (GB)', '')
    ## Cria um objeto Processador a partir de um dicionário de dados
    def _create_processador_from_dict(self, data: dict):
        if not data:
            raise ValueError('Dados do processador inválidos')
        modelo = data.get('modelo')
        fabricante = data.get('fabricante')
        ultima = bool(data.get('ultima_geracao', False))
        if ultima:
            perf = data.get('perf_cores', 0)
            eff = data.get('eff_cores', 0)
            return Processador(modelo=modelo, fabricante=fabricante, ultima_geracao=True, perf_cores=perf, eff_cores=eff, integrated_gpu=data.get('integrated_gpu', False), familia=data.get('familia'))
        else:
            nucleos = data.get('nucleos')
            hyper = bool(data.get('hyperthread', False))
            return Processador(modelo=modelo, fabricante=fabricante, nucleos=nucleos, hyperthread=hyper, integrated_gpu=data.get('integrated_gpu', False), familia=data.get('familia'))
    ## Adiciona um novo computador ao inventário
    def _ler_dados_do_formulario_e_criar_obj(self):
        try:
            modelo_cpu = self._get_valor('CPU Modelo')
            familia_cpu = self._get_valor('CPU Família')
            
            if modelo_cpu == 'Outro' or familia_cpu == 'Outro': # Se for outro, ele cria manualmente o processador com base nas entradas
                is_ultima_geracao = self.cpu_ultima_geracao_var.get()
                cpu_data = {
                    "fabricante": self._get_valor('CPU Fabricante'),
                    "familia": "Custom",
                    "modelo": "Custom",
                    "ultima_geracao": is_ultima_geracao,
                    "hyperthread": self.cpu_hyper_var.get(),
                    "nucleos": self._get_valor('CPU Núcleos', int, False) if not is_ultima_geracao else 0,
                    "perf_cores": self._get_valor('CPU Núcleos Performance', int, False) if is_ultima_geracao else 0,
                    "eff_cores": self._get_valor('CPU Núcleos Eficiência', int, False) if is_ultima_geracao else 0,
                    "integrated_gpu": self.cpu_integrated_var.get(),
                }
                cpu = self._create_processador_from_dict(cpu_data)
            else:
                proc_data = next((p for p in self.processadores_db if p['modelo'] == modelo_cpu), None)
                if not proc_data: raise ValueError("Selecione um processador válido.")
                cpu = self._create_processador_from_dict(proc_data)

            mod_count = int(self._get_valor('Módulos RAM'))
            tamanho_por_mod = self._get_valor('Tamanho por Módulo (GB)', int)
            ram_total = mod_count * int(tamanho_por_mod)
            ram = MemoriaRAM(ram_total, self._get_valor('RAM (MHz)', int), mod_count)
            # Configuração do Computador
            tipo = self._get_valor('Tipo')
            tag = self._get_valor('Tag de Identificação')

            # Configuração do Disco
            ssd_tipo = self._get_valor('SSD Tipo')
            ssd_capacidade = self._get_valor('SSD Capacidade (GB)', int)
            hdd_sec = self._get_valor('HD (GB)', int, False) or 0
            disco_principal = Disco(ssd_tipo, ssd_capacidade)
            disco_sec = Disco('HD SATA', hdd_sec) if hdd_sec and int(hdd_sec) > 0 else None

            # Cria um novo computador com base no tipo selecionado
            novo_computador = None
            # Selecionando o tipo de computador a ser criado
            if tipo == "ComputadorOffice":
                monitor = Monitor(marca=self._get_valor('Monitor Marca'), modelo=self._get_valor('Monitor Modelo', obrigatorio=False) or 'Padrão', tamanho_polegadas=self._get_valor('Monitor Polegadas (")', float), frequencia_hz=self._get_valor('Monitor Frequência (Hz)', int, False) or 60)
                novo_computador = ComputadorOffice(tag, cpu, ram, disco_principal, disco_sec, monitor)
            elif tipo in ("ComputadorGamer", "ComputadorIntermediario"):
                gpu_model = self._get_valor('GPU Modelo')
                gpu_fab = self._get_valor('GPU Fabricante')
                profissional_flag = self._is_professional_gpu(gpu_model, gpu_fab)
                gpu_entry = next((g for g in self.gpus_db if g.get('modelo') == gpu_model and g.get('fabricante') == gpu_fab), None)
                if gpu_entry:
                    memoria_vram = int(gpu_entry.get('memoria_vram', 0) or 0)
                else:
                    memoria_vram = self._get_valor('GPU VRAM (GB)', int)
                gpu = PlacaDeVideo(modelo=gpu_model, memoria_vram=memoria_vram, fabricante=gpu_fab, profissional=profissional_flag)
                monitor_class = MonitorGamer if tipo == "ComputadorGamer" else Monitor
                monitor = monitor_class(marca=self._get_valor('Monitor Marca'), modelo=self._get_valor('Monitor Modelo', obrigatorio=False) or 'Padrão', tamanho_polegadas=self._get_valor('Monitor Polegadas (")', float), frequencia_hz=self._get_valor('Monitor Frequência (Hz)', int))
                if tipo == "ComputadorGamer": novo_computador = ComputadorGamer(tag, cpu, ram, disco_principal, disco_sec, gpu, monitor)
                else: novo_computador = ComputadorIntermediario(tag, cpu, ram, disco_principal, disco_sec, gpu, monitor)
            elif tipo == "ComputadorWorkstation":
                gpu_model = self._get_valor('GPU Modelo')
                gpu_fab = self._get_valor('GPU Fabricante')
                profissional_flag = self._is_professional_gpu(gpu_model, gpu_fab)
                gpu_entry = next((g for g in self.gpus_db if g.get('modelo') == gpu_model and g.get('fabricante') == gpu_fab), None)
                if gpu_entry:
                    memoria_vram = int(gpu_entry.get('memoria_vram', 0) or 0)
                else:
                    memoria_vram = self._get_valor('GPU VRAM (GB)', int)
                gpu = PlacaDeVideo(modelo=gpu_model, memoria_vram=memoria_vram, fabricante=gpu_fab, profissional=profissional_flag)
                monitor = Monitor(marca=self._get_valor('Monitor Marca'), modelo=self._get_valor('Monitor Modelo', obrigatorio=False) or 'Padrão', tamanho_polegadas=self._get_valor('Monitor Polegadas (")', float), frequencia_hz=self._get_valor('Monitor Frequência (Hz)', int))
                novo_computador = ComputadorWorkstation(tag, cpu, ram, disco_principal, disco_sec, gpu, monitor)
            

            if novo_computador:
                return novo_computador # SUCESSO! Retorna o objeto criado.
            else:
                raise ValueError("Tipo de computador inválido.") # Força cair no 'except'

        except ValueError as e: 
            messagebox.showerror("Erro de Entrada", f"Dado inválido: {e}")
            return None # FALHA: Retorna None
        except Exception as e: 
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")
            return None # FALHA: Retorna None

    def _adicionar_computador(self):
        novo_computador = self._ler_dados_do_formulario_e_criar_obj()

        if novo_computador is None:
            return

        tag = novo_computador.tag_identificacao
        if any(c.tag_identificacao.lower() == tag.lower() for c in self.lista_computadores):
            messagebox.showerror("Erro de Duplicidade", f"A tag '{tag}' já está em uso.")
            return
        self.lista_computadores.append(novo_computador)
        self._atualizar_lista()
        self._limpar_campos()
    
    ## Limpa todos os campos do formulário
    def _limpar_campos(self):
        for data in self.widgets.values():
            widget = data['widget']
            if isinstance(widget, ttk.Combobox): widget.set('')
            elif isinstance(widget, ttk.Entry):
                is_readonly = widget.cget('state') == 'readonly'
                if is_readonly: widget.config(state='normal')
                widget.delete(0, tk.END)
                if is_readonly: widget.config(state='readonly')
        self._update_cpu_fields()
        self._update_form_visibility()
        self.item_selecionado_index = None
    ## Atualiza dinamicamente a interface gráfica com base no tipo de computador selecionado e outras opções
    def _update_form_visibility(self, event=None):
        tipo_selecionado = self.widgets['Tipo']['widget'].get() # Obtém o tipo de computador selecionado
        is_ultima_geracao = self.cpu_ultima_geracao_var.get() # Verifica se a CPU é de última geração
        ram_widget = self.widgets['Módulos RAM']['widget'] # Obtém o widget de módulos de RAM
        if tipo_selecionado == 'ComputadorOffice':
            ram_widget['values'] = ['1', '2']
        elif tipo_selecionado in ('ComputadorGamer', 'ComputadorIntermediario'):
            ram_widget['values'] = ['1', '2', '4']
        elif tipo_selecionado == 'ComputadorWorkstation':
            ram_widget['values'] = ['1', '2', '4', '8']
        else:
            ram_widget['values'] = ['1', '2']
        
        if 'GPU Fabricante' in self.widgets: # Se a opção GPU Fabricante existir na interface, entao ele roda esse código
            if tipo_selecionado == 'ComputadorWorkstation':
                self.widgets['GPU Fabricante']['widget']['values'] = ['AMD', 'NVIDIA'] # Atualiza as opções de fabricante de GPU para Workstation
            else:
                self.widgets['GPU Fabricante']['widget']['values'] = ['AMD', 'NVIDIA', 'INTEL'] # Atualiza as opções de fabricante de GPU para outros tipos de computador (Gamer e Intermediário)
            fab = self.widgets['GPU Fabricante']['widget'].get() # Obtém o fabricante de GPU selecionado
            if fab: # Se ja tiver sido selecionado a fabricante, ele atualiza os modelos de GPU
                self._update_gpu_models()
        # Para cada widget, verifica se ele deve estar visível para o tipo de computador selecionado (targets).
        for name, data in self.widgets.items():
            targets = data['config']['targets'] 
            is_visible = 'all' in targets or tipo_selecionado in targets # is_visible é verdadeiro se o campo deve ser exibido
            # grid() exibe o widget, grid_remove() oculta o widget
            if is_visible: 
                data['label'].grid()
                data['widget'].grid()
            else: 
                data['label'].grid_remove()
                data['widget'].grid_remove()
        # Exibe ou oculta campos específicos com base na geração do processador, nucleos de performance e eficiencia 
        campos_ultima_geracao = ['CPU Última Geração', 'CPU Núcleos Performance', 'CPU Núcleos Eficiência']
        campos_legado = ['CPU Hyperthread']
        # Campos de CPU de última geração
        for name in campos_ultima_geracao:
            if is_ultima_geracao:
                self.widget[name]['label'].grid()
                self.widgets[name]['widget'].grid()
            else:
                self.widgets[name]['label'].grid_remove()
                self.widgets[name]['widget'].grid_remove()
        # Campos de CPU legado
        for name in campos_legado:
            if is_ultima_geracao:
                self.widgets[name]['label'].grid_remove()
                self.widgets[name]['widget'].grid_remove()
            else:
                self.widgets[name]['label'].grid()
                self.widgets[name]['widget'].grid()
        # Atualiza os modelos de CPU com base na família selecionada
        familia_atual = self.widgets['CPU Família']['widget'].get() # Obtém a família de CPU selecionada (Ex: Intel core I5, AMD Ryzen 5, etc)
        if familia_atual and familia_atual != 'Outro':
            if tipo_selecionado == 'ComputadorOffice':
                modelos = sorted([p['modelo'] for p in self.processadores_db if p['familia'] == familia_atual and p.get('integrated_gpu', False)]) # .get(chave, valor_padrao)
            else:
                modelos = sorted([p['modelo'] for p in self.processadores_db if p['familia'] == familia_atual])
            self.widgets['CPU Modelo']['widget']['values'] = ['Outro'] + modelos
    # Obtém o valor de um campo da interface e faz validações automáticas obrigatórias
    def _get_valor(self, nome_campo, tipo=str, obrigatorio=True):
        try:
            ### Caso especial para 3 checkboxes
            if nome_campo == 'CPU Última Geração': return self.cpu_ultima_geracao_var.get() #
            if nome_campo == 'CPU Hyperthread': return self.cpu_hyper_var.get() #
            if nome_campo == 'CPU Gráficos Integrados': return self.cpu_integrated_var.get() #
            widget = self.widgets[nome_campo]['widget']
            if not widget.winfo_ismapped(): return None # # Se o widget não estiver visível na interface, retorna None (campo não preenchido/oculto)
            valor = widget.get() # Obtém o valor digitado no campo especificado pelo nome_campo
            if not valor:
                if obrigatorio: raise ValueError(f"Campo '{nome_campo}' é obrigatório.")
                return None
            return tipo(valor) # Converte a variavel valor para o tipo especificado no parâmetro do método(str, int, float)
        except (ValueError, TypeError): raise ValueError(f"Campo '{nome_campo}' deve ser um número válido.") # Lança erro caso o usuário digite um valor inválido
        except KeyError: return None # Retorna None caso o nome do campo não exista na interface
    ## Atualiza a lista de computadores exibida na interface
    def _atualizar_lista(self):
        self.lista_widget.config(state=tk.NORMAL) # Ativa o widget Text para modificação
        self.lista_widget.delete('1.0', tk.END) # Apaga o conteúdo do widget lista da linha 1 até o fim.
        for i, comp in enumerate(self.lista_computadores): # Percorre todos os computadores na lista numerando com indices 0, 1, 2,...
            try: info = comp.get_info_completa() # Tenta obter a informação completa do computador
            except AttributeError: info = f"Tag: {comp.tag_identificacao}" # Caso falhe, exibe apenas a tag de identificação
            tag_id = f"item_{i}" # Cria um ID de tag único para cada item
            header = f"--- Item {i+1}: {comp.tag_identificacao} ({comp.__class__.__name__}) ---\n"
            self.lista_widget.tag_configure(f"header_{i}", font=("TkDefaultFont", 10, "bold")) # Configura a tag do cabeçalho com fonte em negrito
            self.lista_widget.insert(tk.END, header, (f"header_{i}", tag_id)) # Insere o cabeçalho do computador no widget Text 
            self.lista_widget.insert(tk.END, f"{info}\n\n", (tag_id,)) # Insere as informações do computador no widget Text
        self.lista_widget.config(state=tk.DISABLED) # Desativa o widget Text para evitar edições manuais
    ## Salva o inventário em um arquivo JSON
    def _salvar_arquivo(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json", 
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Salvar inventário como...") # Abre a caixa de diálogo para salvar o arquivo
        if not filepath: return # Se o usuário cancelar, retorna sem fazer nada (evitando possíveis erros)
        try: # Tenta salvar o inventário no arquivo selecionado
            lista_dict = [c.to_dict() for c in self.lista_computadores] # Converte cada computador em um dicionário
            with open(filepath, 'w', encoding='utf-8') as f: # Abre o arquivo para escrita (usando o utf-8 para funcionar bem em windows e linux)(caracteres especiais)
                json.dump(lista_dict, f, indent=4) # Salva a lista_dict em formato JSON
            messagebox.showinfo("Sucesso", "Inventário salvo com sucesso!")
        except Exception as e: messagebox.showerror("Erro ao Salvar", f"Ocorreu um erro ao salvar o arquivo: {e}") # Exibe uma mensagem de erro caso ocorra algum problema ao salvar o arquivo

    def _carregar_arquivo(self):
        filepath = filedialog.askopenfilename(
            defaultextension=".json", 
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")], 
            title="Carregar inventário de...") # Abre a caixa de diálogo para abrir o arquivo
        if not filepath: return # Se o usuário cancelar, retorna sem fazer nada (evitando possíveis erros)
        try: # Tenta carregar o inventário do arquivo selecionado
            with open(filepath, 'r', encoding='utf-8') as f: # Abre o arquivo para leitura (usando o utf-8 para funcionar bem em windows e linux)(caracteres especiais)
                lista_dict = json.load(f) # Carrega a lista de dicionários do arquivo JSON
            if not isinstance(lista_dict, list):
                raise ValueError("Formato de arquivo inválido: Esperado uma lista de computadores.")
            nova_lista = [] # Lista temporária para armazenar os computadores carregados
            for item_data in lista_dict: # Percorre cada dicionário na lista carregada
                tipo = item_data.get('tipo')
                tag = item_data.get('tag_identificacao')
                cpu_data = item_data.get('processador')
                ram_data = item_data.get('memoria_ram')
                disco_principal_data = item_data.get('disco_principal')
                disco_secundario_data = item_data.get('disco_secundario')
                monitor_data = item_data.get('monitor')
                gpu_data = item_data.get('placa_de_video', None)

                cpu = self._create_processador_from_dict(cpu_data)
                ram = MemoriaRAM(ram_data['capacidade_gb'], ram_data['velocidade_mhz'], ram_data['num_modulos'])
                disco_principal = Disco(disco_principal_data['tipo'], disco_principal_data['capacidade_gb'])
                disco_secundario = None
                if disco_secundario_data:
                    disco_secundario = Disco(disco_secundario_data['tipo'], disco_secundario_data['capacidade_gb'])
                if monitor_data['tipo'] == 'MonitorGamer':  
                    monitor = MonitorGamer(monitor_data['marca'], monitor_data.get('modelo', 'Padrão'), monitor_data['tamanho_polegadas'], monitor_data['frequencia_hz'])
                else:
                    monitor = Monitor(monitor_data['marca'], monitor_data.get('modelo', 'Padrão'), monitor_data['tamanho_polegadas'], monitor_data['frequencia_hz'])
                
                if tipo == 'ComputadorOffice':
                    computador = ComputadorOffice(tag, cpu, ram, disco_principal, disco_secundario, monitor)
                elif tipo in ('ComputadorGamer', 'ComputadorIntermediario'):
                    gpu = PlacaDeVideo(gpu_data['modelo'], gpu_data['memoria_vram'], gpu_data['fabricante'], gpu_data.get('profissional', False))
                    if tipo == 'ComputadorGamer':
                        computador = ComputadorGamer(tag, cpu, ram, disco_principal, disco_secundario, gpu, monitor)
                    else:
                        computador = ComputadorIntermediario(tag, cpu, ram, disco_principal, disco_secundario, gpu, monitor)
                elif tipo == 'ComputadorWorkstation':
                    gpu = PlacaDeVideo(gpu_data['modelo'], gpu_data['memoria_vram'], gpu_data['fabricante'], gpu_data.get('profissional', False))
                    computador = ComputadorWorkstation(tag, cpu, ram, disco_principal, disco_secundario, gpu, monitor)
                else:
                    raise ValueError(f"Tipo de computador desconhecido: {tipo}")
                nova_lista.append(computador) # Adiciona o computador criado à lista temporária 
                self.lista_computadores = nova_lista # Substitui a lista atual pela nova lista carregada    
                self._atualizar_lista() # Atualiza a exibição da lista na interface   
        except Exception as e:
            messagebox.showerror("Erro ao Carregar", f"Ocorreu um erro ao carregar o arquivo: {e}")
            return
    
    def _buscar_e_carregar_por_tag(self):
        tag_busca = self.search_entry.get().strip()
        if not tag_busca:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira uma TAG para buscar.")
            return

        computador, indice = self._encontrar_computador_por_tag(tag_busca)

        if computador: # Se 'computador' não for None
            self.item_selecionado_index = indice 
            self._preencher_campos_para_edicao(computador) 
        else:
            messagebox.showinfo("Não Encontrado", f"Nenhum computador encontrado com a TAG '{tag_busca}'.")
    
    def _salvar_item(self):  
        try:
            novo_computador_obj = self._ler_dados_do_formulario_e_criar_obj() 
            if novo_computador_obj is None: return
        except Exception as e:
            messagebox.showerror("Erro de Validação", f"Não foi possível salvar: {e}")
            return
        
        if self.item_selecionado_index is not None:
            self.lista_computadores[self.item_selecionado_index] = novo_computador_obj
            messagebox.showinfo("Sucesso", "Computador ATUALIZADO com sucesso!")
        else:
            self.lista_computadores.append(novo_computador_obj)
            messagebox.showinfo("Sucesso", "Computador ADICIONADO com sucesso!")
        self._atualizar_lista()
        self._limpar_campos()

    def _excluir_por_tag(self):
        tag_busca = self.search_entry.get().strip()
        if not tag_busca:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira uma TAG para excluir.")
            return
            
        computador, indice = self._encontrar_computador_por_tag(tag_busca)

        if computador: # Se 'computador' não for None
            confirm = messagebox.askyesno("Confirmação de Exclusão", f"Tem certeza que deseja excluir o computador com a TAG '{tag_busca}'?")
            if confirm:
                # 'del' é o comando Python simples para deletar um item de uma lista pelo seu índice
                del self.lista_computadores[indice] 
                self._atualizar_lista()
                messagebox.showinfo("Excluído", f"Computador com a TAG '{tag_busca}' foi excluído com sucesso.")
        else:
            # Se 'computador' for None, ele não achou
            messagebox.showinfo("Não Encontrado", f"Nenhum computador encontrado com a TAG '{tag_busca}'.")
    
    ## Método auxiliar para encontrar um item na lista pela TAG
    def _encontrar_computador_por_tag(self, tag_busca):
        for i, comp in enumerate(self.lista_computadores):
            if comp.tag_identificacao.lower() == tag_busca.lower():
                return comp, i  # encontrou, retorna o objeto e sua posição (índice)
        return None, None # nao encontrou


    def _preencher_campos_para_edicao(self, computador: Computador):
        try:
            self._limpar_campos()
            self._set_field_value('Tag de Identificação', computador.tag_identificacao)
            tipo = computador.__class__.__name__
            self.widgets['Tipo']['widget'].set(tipo)

            cpu = computador.processador
            self.widgets['CPU Fabricante']['widget'].set(cpu.fabricante)
            self.widgets['CPU Família']['widget'].set(cpu.familia)
            self._update_cpu_fields()
            self.widgets['CPU Modelo']['widget'].set(cpu.modelo)
            self._update_cpu_fields()
            if cpu.ultima_geracao:
                self.cpu_ultima_geracao_var.set(True)
                self._set_field_value('CPU Núcleos Performance', cpu.perf_cores)
                self._set_field_value('CPU Núcleos Eficiência', cpu.eff_cores)
            else:
                self.cpu_ultima_geracao_var.set(False)
                self._set_field_value('CPU Núcleos', cpu.nucleos)
            self.cpu_hyper_var.set(cpu.hyperthread)
            self.cpu_integrated_var.set(cpu.integrated_gpu)

            ram = computador.memoria_ram
            self.widgets['Módulos RAM']['widget'].set(ram.num_modulos)
            tamanho_por_mod = ram.capacidade_gb // ram.num_modulos
            self._set_field_value('Tamanho por Módulo (GB)', tamanho_por_mod)
            self._set_field_value('RAM (MHz)', ram.velocidade_mhz)

            disco_principal = computador.disco_principal
            self.widgets['SSD Tipo']['widget'].set(disco_principal.tipo)
            self._set_field_value('SSD Capacidade (GB)', disco_principal.capacidade_gb)
            if computador.disco_secundario:
                disco_sec = computador.disco_secundario
                self._set_field_value('HD (GB)', disco_sec.capacidade_gb)
            else:
                self._set_field_value('HD (GB)', '')

            monitor = computador.monitor
            self._set_field_value('Monitor Marca', monitor.marca)
            self._set_field_value('Monitor Modelo', monitor.modelo)
            self._set_field_value('Monitor Polegadas (")', monitor.tamanho_polegadas)
            self._set_field_value('Monitor Frequência (Hz)', monitor.frequencia_hz)

            if tipo in ('ComputadorGamer', 'ComputadorIntermediario', 'ComputadorWorkstation'):
                gpu = computador.placa_de_video
                self.widgets['GPU Fabricante']['widget'].set(gpu.fabricante)
                self._update_gpu_models()
                self.widgets['GPU Modelo']['widget'].set(gpu.modelo)
                self._update_gpu_vram()
                self.item_selecionado_index = self.lista_computadores.index(computador)
                self._update_form_visibility()
            
        except Exception as e:
            messagebox.showerror("Erro ao Editar", f"Ocorreu um erro ao preencher os campos para edição: {e}")

        