<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>L.I.T.I.S. - Acceso y Archivero</title>
    <style>
        /* Tipografía clásica de máquina de escribir y fondo oscuro forense */
        body {
            margin: 0;
            padding: 0;
            background-color: #0a0e17; 
            color: #d1d5db;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }

        /* ----- PANTALLA 1: ACCESO ZAFIRO ----- */
        #pantallaLogin {
            position: absolute;
            z-index: 10;
            transition: all 1s ease-in-out;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 100%;
            background-color: #0a0e17; 
        }

        .zafiro-panel {
            background: rgba(16, 32, 64, 0.4);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(88, 166, 255, 0.25);
            border-radius: 12px;
            padding: 40px;
            width: 320px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
            position: relative;
        }

        h1 { color: #58a6ff; letter-spacing: 3px; margin-bottom: 5px; }
        p { font-size: 14px; margin-bottom: 25px; color: #8b949e; }

        input {
            width: 90%;
            padding: 12px;
            margin: 10px 0;
            background: rgba(0, 0, 0, 0.6);
            border: 1px solid #30363d;
            color: #c9d1d9;
            font-family: 'Courier New', Courier, monospace;
            border-radius: 4px;
            outline: none;
        }
        input:focus { border-color: #58a6ff; }

        button {
            background-color: #1f6feb;
            color: white;
            border: none;
            padding: 12px;
            font-family: 'Courier New', Courier, monospace;
            font-weight: bold;
            font-size: 16px;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
            margin-top: 15px;
            transition: all 0.3s ease;
        }
        button:hover { background-color: #58a6ff; }

        #mensajeError { color: #ff7b72; margin-top: 15px; display: none; font-weight: bold; }

        /* Animación Biométrica */
        .escaner-biometrico {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 100px;
            height: 100px;
            border: 4px solid transparent;
            border-top: 4px solid #58a6ff;
            border-bottom: 4px solid #58a6ff;
            border-radius: 50%;
            display: none;
            animation: girar 1s linear infinite;
            box-shadow: 0 0 20px rgba(88, 166, 255, 0.8);
        }

        @keyframes girar {
            0% { transform: translate(-50%, -50%) rotate(0deg); }
            100% { transform: translate(-50%, -50%) rotate(360deg); }
        }

        /* Efecto de apertura de puertas */
        .abrir-puertas {
            transform: scale(1.5);
            opacity: 0;
            pointer-events: none;
        }

        /* ----- PANTALLA 2: ARCHIVERO ----- */
        #pantallaArchivero {
            position: absolute;
            opacity: 0;
            z-index: 5;
            transition: opacity 1s ease-in-out;
            width: 80%;
            height: 80%;
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 30px;
            display: none;
            flex-direction: column;
        }

        .barra-superior {
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid #30363d;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }

        .buscador {
            background: #0d1117;
            border: 1px solid #30363d;
            padding: 8px;
            color: #8b949e;
            width: 300px;
            font-family: 'Courier New', Courier, monospace;
        }

        .tarjeta-expediente {
            background: #f0e6d2; /* Color crema amarillento */
            color: #000;
            padding: 20px;
            border-radius: 4px;
            width: 300px;
            border-left: 5px solid #d73a49; /* Tinta roja */
            cursor: pointer;
        }
        
        .tarjeta-expediente h3 { margin: 0 0 10px 0; font-family: sans-serif;}
        .tarjeta-expediente p { color: #333; margin: 0;}
    </style>
</head>
<body>

    <!-- PANTALLA 1: LOGIN -->
    <div id="pantallaLogin">
        <div class="zafiro-panel" id="panelCentral">
            <h1>L.I.T.I.S.</h1>
            <p>Sistema de Simulación Legal</p>
            
            <input type="text" id="usuario" placeholder="Usuario">
            <input type="password" id="clave" placeholder="Contraseña">
            
            <button onclick="iniciarSesion()">INGRESAR</button>
            <p id="mensajeError">Acceso denegado. Credenciales inválidas.</p>
        </div>
        <div class="escaner-biometrico" id="escaner"></div>
    </div>

    <!-- PANTALLA 2: ARCHIVERO -->
    <div id="pantallaArchivero">
        <div class="barra-superior">
            <h2>Archivero Principal - Usuario: Baltazar</h2>
            <input type="text" class="buscador" value="Buscar por expediente, testigo..." readonly>
        </div>
        
        <h3>Expedientes Disponibles</h3>
        <div class="tarjeta-expediente" onclick="abrirCaso()">
            <h3>Caso Nº1: Entradas en falso</h3>
            <p>Testigo: Emilia Martínez</p>
            <p>Estado: Listo para ingesta RAG</p>
        </div>
    </div>

    <script>
        function iniciarSesion() {
            var user = document.getElementById("usuario").value;
            var pass = document.getElementById("clave").value;

            if (user === "Baltazar" && pass === "Litis2026") {
                document.getElementById("mensajeError").style.display = "none";
                document.getElementById("panelCentral").style.opacity = "0";
                document.getElementById("escaner").style.display = "block";
                
                // Simula 1.5 segundos de escaneo antes de abrir
                setTimeout(function() {
                    document.getElementById("pantallaLogin").classList.add("abrir-puertas");
                    document.getElementById("pantallaArchivero").style.display = "flex";
                    setTimeout(function() {
                        document.getElementById("pantallaArchivero").style.opacity = "1";
                    }, 100);
                }, 1500);

            } else {
                document.getElementById("mensajeError").style.display = "block";
            }
        }

        function abrirCaso() {
            alert("Iniciando motor RAG... Abriendo lienzo de interrogatorio.");
            // Aquí enlazaremos con la siguiente etapa
        }
    </script>

</body>
</html>
