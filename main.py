<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>L.I.T.I.S. - Simulación Completa</title>
    <style>
        /* Diseño General y Tipografía Forense */
        body {
            margin: 0; padding: 0;
            background-color: #0a0e17; color: #d1d5db;
            font-family: 'Courier New', Courier, monospace;
            display: flex; justify-content: center; align-items: center;
            height: 100vh; overflow: hidden;
        }

        .screen { display: none; width: 100%; height: 100%; justify-content: center; align-items: center; flex-direction: column; }
        .active { display: flex; }

        /* Efecto Cristal Zafiro */
        .zafiro-panel {
            background: rgba(16, 32, 64, 0.4); backdrop-filter: blur(15px);
            border: 1px solid rgba(88, 166, 255, 0.25); border-radius: 12px;
            padding: 40px; width: 400px; text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6); position: relative;
        }

        h1, h2, h3 { color: #58a6ff; letter-spacing: 2px; }
        p { color: #8b949e; }

        input, textarea, select {
            width: 90%; padding: 12px; margin: 10px 0;
            background: rgba(0, 0, 0, 0.6); border: 1px solid #30363d;
            color: #c9d1d9; font-family: 'Courier New', Courier, monospace;
            border-radius: 4px; outline: none;
        }
        input:focus, textarea:focus { border-color: #58a6ff; }

        button {
            background-color: #1f6feb; color: white; border: none;
            padding: 12px; font-family: 'Courier New', Courier, monospace; font-weight: bold;
            border-radius: 4px; cursor: pointer; width: 100%; margin-top: 15px;
            transition: 0.3s;
        }
        button:hover { background-color: #58a6ff; box-shadow: 0 0 10px rgba(88, 166, 255, 0.5); }
        .btn-rojo { background-color: #d73a49; }
        .btn-rojo:hover { background-color: #ff5252; box-shadow: 0 0 10px rgba(215, 58, 73, 0.5); }

        /* Animación Biométrica */
        .escaner {
            width: 80px; height: 80px; border: 4px solid transparent;
            border-top: 4px solid #58a6ff; border-bottom: 4px solid #58a6ff;
            border-radius: 50%; display: none; animation: girar 1s linear infinite; margin: 20px auto;
        }
        @keyframes girar { 100% { transform: rotate(360deg); } }

        /* Papel Calco (Interrogatorio) */
        .lienzo-calco {
            background: rgba(255, 255, 255, 0.9); color: #000;
            width: 80%; height: 80%; border-radius: 8px; padding: 20px;
            display: flex; flex-direction: column;
        }
        .chat-box { flex-grow: 1; overflow-y: auto; border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; background: #fff; }
        .msg { margin-bottom: 10px; padding: 8px; border-radius: 4px; }
        .msg-fiscal { background: #e1f5fe; text-align: right; border-left: 4px solid #0288d1; }
        .msg-testigo { background: #f5f5f5; text-align: left; border-left: 4px solid #9e9e9e; }
        .msg-juez { background: #ffebee; text-align: center; font-weight: bold; color: #d32f2f; border: 2px solid #d32f2f; }

        /* Doctrina [?] */
        .doctrina-popup {
            display: none; background: rgba(16, 32, 64, 0.9); color: #58a6ff;
            padding: 15px; border: 1px solid #58a6ff; border-radius: 8px; margin-bottom: 10px;
        }

        /* Papel Amarillento y Tinta Roja (Dictamen) */
        .papel-amarillento {
            background: #fdf6e3; color: #d73a49; width: 60%; padding: 40px;
            border-radius: 4px; box-shadow: inset 0 0 20px rgba(0,0,0,0.1);
            font-family: 'Brush Script MT', cursive, 'Courier New'; font-size: 20px;
        }
    </style>
</head>
<body>

    <!-- FASE 1: LOGIN -->
    <div id="pantallaLogin" class="screen active">
        <div class="zafiro-panel">
            <h1>L.I.T.I.S.</h1>
            <p>Acceso Restringido</p>
            <input type="text" id="user" placeholder="Usuario">
            <input type="password" id="pass" placeholder="Contraseña">
            <button onclick="login()">INGRESAR</button>
            <div id="loaderLogin" class="escaner"></div>
            <p id="errorLogin" style="color:#ff7b72; display:none;">Credenciales inválidas.</p>
        </div>
    </div>

    <!-- FASE 2: INGESTA DE PDF -->
    <div id="pantallaUpload" class="screen">
        <div class="zafiro-panel">
            <h2>Motor RAG</h2>
            <p>Seleccione el expediente a procesar</p>
            <input type="file" id="archivoPDF" accept=".pdf">
            <button onclick="subirPDF()">PROCESAR EXPEDIENTE</button>
            <div id="loaderUpload" class="escaner"></div>
            <p id="statusUpload" style="color:#58a6ff; display:none;">Indexando datos...</p>
        </div>
    </div>

    <!-- FASE 3: CONFIGURACIÓN DEL TESTIGO -->
    <div id="pantallaConfig" class="screen">
        <div class="zafiro-panel" style="width: 500px;">
            <h2>Parámetros del Testigo</h2>
            <p>Expediente cargado: "Entradas en falso.pdf"</p>
            <label>Locuacidad</label> <input type="range" min="1" max="100" value="80">
            <label>Hostilidad</label> <input type="range" min="1" max="100" value="10">
            <label>Indignación</label> <input type="range" min="1" max="100" value="85">
            <textarea placeholder="Escribe el System Prompt (Ej: Eres Emilia Martínez...)"></textarea>
            <button onclick="iniciarJuicio()">INICIAR INTERROGATORIO</button>
        </div>
    </div>

    <!-- FASE 4: LIENZO DE INTERROGATORIO -->
    <div id="pantallaJuicio" class="screen">
        <div class="lienzo-calco">
            <div style="display: flex; justify-content: space-between;">
                <h2 style="color: #000; margin-top:0;">Acta de Audiencia</h2>
                <button style="width: auto; margin: 0;" class="btn-rojo" onclick="finalizar()">FINALIZAR SIMULACIÓN</button>
            </div>
            
            <div id="doctrinaPanel" class="doctrina-popup">
                <strong>[?] Doctrina - Pregunta Compuesta:</strong> Cada pregunta debe abordar un único punto fáctico a la vez. Es objetable incluir dos interrogantes en la misma frase.
            </div>

            <div class="chat-box" id="chatCentral">
                <div class="msg msg-juez">EL JUEZ: Tiene la palabra la fiscalía, usuario Baltazar. Puede comenzar.</div>
            </div>

            <div style="display: flex; gap: 10px;">
                <input type="text" id="inputPregunta" placeholder="Escriba o dicte su pregunta aquí..." style="background:#fff; color:#000;">
                <button onclick="enviarMensaje()" style="width: 150px;">PREGUNTAR</button>
                <button onclick="forzarObjecion()" class="btn-rojo" style="width: 150px;">¡FORZAR ERROR!</button>
            </div>
        </div>
    </div>

    <!-- FASE 5: DICTAMEN SOCRÁTICO -->
    <div id="pantallaDictamen" class="screen">
        <div class="papel-amarillento">
            <h2 style="color: #000; font-family: 'Courier New'; text-align: center;">DICTAMEN DE AUDITORÍA</h2>
            <hr style="border-color: #d73a49;">
            <p>1. Excelente técnica de incorporación de prueba. Se cumplió el traslado a la defensa.</p>
            <p>2. ¡Atención! Objeción por pregunta compuesta detectada al indagar sobre la manipulación de los posteos. Acierto al optar por reformular.</p>
            <p>3. Control de la testigo: 92%. Se extrajo la información clave gestionando correctamente su nivel de locuacidad.</p>
            <button onclick="location.reload()" style="font-family: 'Courier New';">CERRAR Y GUARDAR EN ARCHIVERO</button>
        </div>
    </div>

    <script>
        function cambiarPantalla(idOcultar, idMostrar) {
            document.getElementById(idOcultar).classList.remove('active');
            document.getElementById(idMostrar).classList.add('active');
        }

        // 1. Lógica de Login
        function login() {
            if(document.getElementById('user').value === "Baltazar" && document.getElementById('pass').value === "Litis2026") {
                document.getElementById('errorLogin').style.display = "none";
                document.getElementById('loaderLogin').style.display = "block";
                setTimeout(() => cambiarPantalla('pantallaLogin', 'pantallaUpload'), 1500);
            } else {
                document.getElementById('errorLogin').style.display = "block";
            }
        }

        // 2. Lógica de Subida de Archivo
        function subirPDF() {
            let file = document.getElementById('archivoPDF').files[0];
            if(file) {
                document.getElementById('loaderUpload').style.display = "block";
                document.getElementById('statusUpload').style.display = "block";
                setTimeout(() => cambiarPantalla('pantallaUpload', 'pantallaConfig'), 2000);
            } else {
                alert("Por favor, seleccione un expediente en PDF primero.");
            }
        }

        // 3. Pasar al juicio
        function iniciarJuicio() {
            cambiarPantalla('pantallaConfig', 'pantallaJuicio');
        }

        // 4. Lógica de Interrogatorio Dinámico
        function enviarMensaje() {
            let texto = document.getElementById('inputPregunta').value;
            if(!texto) return;
            
            let chat = document.getElementById('chatCentral');
            // Pregunta del Fiscal
            chat.innerHTML += `<div class="msg msg-fiscal"><strong>Baltazar:</strong> ${texto}</div>`;
            document.getElementById('inputPregunta').value = "";
            
            // Respuesta automática de la Testigo
            setTimeout(() => {
                chat.innerHTML += `<div class="msg msg-testigo"><strong>Emilia Martínez:</strong> Respondía exclusivamente a las directivas de la imputada. Los diseños los hacíamos porque ella me lo ordenaba.</div>`;
                chat.scrollTop = chat.scrollHeight;
            }, 1000);
        }

        // 4b. Forzar la objeción con botón de ayuda [?]
        function forzarObjecion() {
            let chat = document.getElementById('chatCentral');
            chat.innerHTML += `<div class="msg msg-fiscal"><strong>Baltazar:</strong> ¿Es cierto que Wanda borraba mensajes y le pidió grabar un video haciéndose la víctima?</div>`;
            
            setTimeout(() => {
                chat.innerHTML += `<div class="msg msg-juez">¡OBJECIÓN DE LA DEFENSA! Pregunta compuesta y sugestiva.</div>`;
                chat.scrollTop = chat.scrollHeight;
                document.getElementById('doctrinaPanel').style.display = "block";
            }, 800);
        }

        // 5. Finalizar
        function finalizar() {
            cambiarPantalla('pantallaJuicio', 'pantallaDictamen');
        }
    </script>
</body>
</html>
