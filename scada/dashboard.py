"""Interfaz visual del prototipo; todavía sin adquisición de telemetría."""


def crear_app():
    import customtkinter as ctk

    #===========================================
    #1. CONFIGURACION DE LA VENTANA PRINCIPAL
    #===========================================

    ctk.set_appearance_mode("dark")  # Modo oscuro

    BG = "#0B1220"  # Color de fondo
    SIDEBAR = "#101A2B"
    CARD = "#172235"
    BORDER = "#273449"
    TEXT = "#F1F5F9"
    MUTED = "#94A3B8"
    ACCENT = "#3B82F6"
    #ctk.set_default_color_theme("blue")  # Tema de color azul

    #Creamos la ventana principal
    app = ctk.CTk()
    app.title("Dashboard SCADA")
    app.geometry("1200x720")
    app.minsize(850, 550)
    app.configure(fg_color=BG)

    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)

    #==========================================
    #2. FUNCIONES PARA EL DASHBOARD
    #==========================================
    def crear_panel(parent):
        return ctk.CTkFrame(parent, fg_color=CARD, corner_radius=10)

    def texto(parent, contenido, tamaño=14, color=TEXT, negrita=False, ajuste=0):
        font = ("Arial", tamaño, "bold") if negrita else ("Arial", tamaño)
        return ctk.CTkLabel(parent, text=contenido, font=font, text_color=color, wraplength=ajuste, justify="left")

    def crear_indicador(parent,columna,nombre,unidad):

        panel = crear_panel(parent)
        panel.grid(row=0, column=columna, padx=6, pady=5, sticky="nsew")
        texto(panel, nombre, 13, MUTED).pack(anchor="w", padx=18, pady=(16, 5))
        texto(panel, "--",30, TEXT,True).pack(anchor="w",padx=18)
        texto(panel, unidad, 12, MUTED).pack(anchor="w", padx=18, pady=(0, 16))

        return panel

    #===========================================
    #3. CREACION DE LA BARRA LATERAL
    #===========================================
    sidebar = ctk.CTkFrame(app, width=210, fg_color=SIDEBAR, corner_radius=0)
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.grid_propagate(False)

    texto(sidebar, "Gemelo digital ", 20, ACCENT, True).pack(pady=(32, 5))
    texto(sidebar, "SCADA Industrial", 12, MUTED).pack(pady=(0, 35))
    texto(sidebar, "SECCIONES PREVISTAS", 13, TEXT, True).pack(anchor="w", padx = 22, pady=12)

    for opcion in ["Supervision", "Inspeccion de calidad", "Mantenimiento ML", "Historial de eventos"]:
        texto(sidebar, opcion, 12, MUTED).pack(anchor="w", padx=25, pady=13)
    texto(sidebar,"PROTOTIPO ACADEMICO",11,ACCENT).pack(side="bottom", pady=25)

    #===========================================
    #4. CONTENEDOR PRINCIPAL
    #===========================================
    main= ctk.CTkScrollableFrame(app, fg_color=BG, corner_radius=0)
    main.grid(row=0, column=1, sticky="nsew")
    main.grid_columnconfigure((0,1,2,3), weight=1)

    #===========================================
    #5. CABECERA DEL DASHBOARD
    #===========================================
    header = ctk.CTkFrame(main, fg_color="transparent")
    header.grid(row=0, column=0, columnspan=4, sticky="ew",padx=16 ,pady=(22,20))

    header.grid_columnconfigure(0, weight=1)

    titulo = texto(header, "Panel de supervision", 26, TEXT, True)
    titulo.grid(row=0, column=0, sticky="w")
    subtitulo = texto(header, "Faja transportadora | Planta virtual 01", 13, MUTED)

    subtitulo.grid(row=1, column=0, sticky="w", pady = 5)

    conexion = ctk.CTkLabel(header, text="SIN CONEXIÓN", text_color=MUTED,fg_color=CARD,corner_radius=8, width=150, height=35)
    conexion.grid(row=0, column=1, rowspan=2)

    #===========================================
    #6. CREACION DE LOS INDICADORES
    #===========================================
    indicadores = ctk.CTkFrame(main, fg_color="transparent")
    indicadores.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10)
    indicadores.grid_columnconfigure((0,1,2,3), weight=1)   

    tarjetas_kpi = [
        crear_indicador(indicadores, 0, "Velocidad", "m/s"),
        crear_indicador(indicadores, 1, "Temperatura", "°C"),
        crear_indicador(indicadores, 2, "Vibración", "mm/s"),
        crear_indicador(indicadores, 3, "Corriente", "A")
    ]
    #============================================
    #DISTRIBUCION RESPONSIVA DE LOS INDICADORES
    #===========================================
    columnas_actuales = None
    def ajustar_indicadores(event):

        nonlocal columnas_actuales
        ancho = event.width

        #deterninamos el número de columnas según el ancho de la ventana

        if ancho >= 780:
            columnas = 4
        elif ancho >= 440:
            columnas = 2
        else:
            columnas = 1
       #evitamos reorganizar si el número de columnas no ha cambiado
        if columnas == columnas_actuales:
            return
        columnas_actuales = columnas

       #retiramos las tarjetas de la grilla y las reorganizamos según el número de columnas
        for tarjeta in tarjetas_kpi:
            tarjeta.grid_forget()
        #configuramos el peso de las columnas para que se expandan proporcionalmente
        for col in range(4):
            indicadores.grid_columnconfigure(col, weight=1 if col < columnas else 0)
        #Reubicamos las tarjetas en la grilla según el número de columnas
        for i, tarjeta in enumerate(tarjetas_kpi):
            fila = i // columnas
            columna = i % columnas
            tarjeta.grid(row=fila, column=columna, padx=6, pady=6, sticky="nsew")

    indicadores.bind("<Configure>", ajustar_indicadores)
      

    #===========================================
    #7. VISUALIZACION DE LA FAJA TRANSPORTADORA
    #===========================================
    main.grid_columnconfigure(0, weight=2)
    main.grid_columnconfigure(1, weight=1)
    main.grid_columnconfigure(2, weight=0)
    main.grid_columnconfigure(3, weight=0)

    central = ctk.CTkFrame(main, fg_color="transparent")
    central.grid(row=2, column=0, columnspan=4, sticky="ew", padx=10, pady=10)
    central.grid_columnconfigure(0, weight=2)
    central.grid_columnconfigure(1, weight=1)

    faja= crear_panel(central)
    faja.grid(row=0, column=0,  sticky="nsew", padx=6, pady=6)
    texto(faja, "VISUALIZACION DE LA FAJA", 16, TEXT, True).pack(anchor="w", padx=20, pady=(20, 8))  
    texto(faja,"ENTRADA     →     TRANSPORTE     →     SALIDA",13,MUTED).pack(pady=(15, 10))

    cinta = ctk.CTkFrame(faja, height=70,fg_color="#334155", corner_radius=12)
    cinta.pack(fill="x", padx=25, pady=10) 
    cinta.pack_propagate(False)

    texto(cinta, "▰   ▰   ▰   ▰   ▰   ▰   ▰", 25, "#64748B").pack(expand=True)
    texto(faja, "Vista esquemática | Movimiento no conectado", 12, MUTED).pack(pady=(5, 20))

    #===========================================
    #8. VISUALIZACION DE LA SEÑAL DEL SENSOR DE PRESENCIA
    #===========================================

    sensor = crear_panel(central)
    sensor.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
    texto(sensor, "SEÑAL DEL SENSOR DE PRESENCIA", 14, TEXT, True).pack(pady=(22, 20))
    estado_sensor = texto(sensor, "SIN DATOS", 20, MUTED,True)
    estado_sensor.pack(pady=10)
    valor_sensor = texto(sensor, "SIN DATOS", 42, TEXT,True)
    valor_sensor.pack(pady=10) 
    texto(sensor,"Señal de presencia: 1 = Objeto detectado | 0 = No hay objeto", 12, MUTED, ajuste=230).pack(pady=(0, 20))


    # ==========================================
    # RESPONSIVE: FAJA Y SENSOR
    # ==========================================

    modo_central = None

    def ajustar_paneles(event):

        nonlocal modo_central

        ancho = event.width

        if ancho >= 690:
            nuevo_modo = "horizontal"
        else:
            nuevo_modo = "vertical"

        # No reorganizar si el modo no cambia
        if nuevo_modo == modo_central:
            return

        modo_central = nuevo_modo

        # Retirar las posiciones anteriores
        faja.grid_forget()
        sensor.grid_forget()

        if nuevo_modo == "horizontal":

            central.grid_columnconfigure(0, weight=2)
            central.grid_columnconfigure(1, weight=1)

            faja.grid(row=0, column=0,sticky="nsew", padx=6, pady=6
            )

            sensor.grid(row=0, column=1,sticky="nsew", padx=6, pady=6
            )

        else:

            central.grid_columnconfigure(0, weight=1)
            central.grid_columnconfigure(1, weight=0)

            faja.grid(row=0, column=0,sticky="ew", padx=6, pady=6
            )

            sensor.grid(row=1, column=0,sticky="ew", padx=6, pady=6
            )


    central.bind("<Configure>", ajustar_paneles)

    #===========================================
    #9. REGISTRO DE EVENTOS
    #===========================================
    inferior = ctk.CTkFrame(main,fg_color="transparent")

    inferior.grid(row=3,column=0,columnspan=4,sticky="ew", padx=10,pady=10)
    eventos = crear_panel(inferior)
    eventos.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
    texto(eventos, "REGISTRO DE EVENTOS", 15, TEXT, True).pack(anchor="w", padx=20, pady=(20, 12))  

    registro = ctk.CTkTextbox(eventos, height=145, fg_color="#101a2b", text_color=MUTED, border_width=0)
    registro.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    registro.insert("end","Sistema preparado.\n""Esperando conexión con CoppeliaSim...\n")
    registro.configure(state ="disabled")

    #===========================================
    #10. MANTENIMIENTO INTELIGENTE
    #===========================================
    ml= crear_panel(inferior)
    ml.grid(row=0, column=1,  sticky="nsew", padx=6, pady=6)
    texto(ml, "MANTENIMIENTO INTELIGENTE", 15, TEXT, True).pack(anchor="w", padx=20, pady=(20, 15))
    texto(ml, "Predicción de fallas y mantenimiento preventivo mediante algoritmos de aprendizaje automático.", 13, MUTED, ajuste=300).pack(anchor="w", padx=20, pady=8)
    texto( ml, "Diagnóstico: No disponible",13, MUTED, ajuste=300).pack(anchor="w", padx=20, pady=8)
    texto(ml, "Estado: Pendiente de entrenamiento",12, ACCENT).pack(anchor="w", padx=20, pady=(8, 20))


    # ==========================================
    # RESPONSIVE: PANELES INFERIORES
    # ==========================================

    modo_inferior = None

    def ajustar_inferior(event):

        nonlocal modo_inferior

        ancho = event.width

        if ancho >= 690:
            nuevo_modo = "horizontal"
        else:
            nuevo_modo = "vertical"

        # Evitar reorganizaciones innecesarias
        if nuevo_modo == modo_inferior:
            return

        modo_inferior = nuevo_modo

        # Retirar posiciones anteriores
        eventos.grid_forget()
        ml.grid_forget()

        if nuevo_modo == "horizontal":

            inferior.grid_columnconfigure(0, weight=1)
            inferior.grid_columnconfigure(1, weight=1)

            eventos.grid(row=0,column=0,sticky="nsew",padx=6,pady=6)

            ml.grid(row=0,column=1,sticky="nsew",padx=6,pady=6)

        else:

            inferior.grid_columnconfigure(0, weight=1)
            inferior.grid_columnconfigure(1, weight=0)

            eventos.grid(row=0,column=0,sticky="ew",padx=6,pady=6)

            ml.grid(row=1,column=0,sticky="ew",padx=6,pady=6)


    inferior.bind("<Configure>", ajustar_inferior)

    #===========================================
    #11. INICIAMOS EL DASHBOARD
    #===========================================
    return app


def main() -> int:
    app = crear_app()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
