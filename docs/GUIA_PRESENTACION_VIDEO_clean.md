# Proyecto Weatheria - Guía para la Presentación en Video

**Duración Objetivo:** 10 minutos  
**Fecha:** 23 de Noviembre de 2024  
**Curso:** Telemática - Universidad EAFIT

## 🎯 Estructura de la Presentación

### Introducción (30 segundos)
**Qué decir:**
> "¡Hola! Hoy voy a demostrar Weatheria, una plataforma distribuida de análisis de datos climáticos. Este proyecto analiza 3 años de datos meteorológicos de Medellín usando MapReduce en AWS EMR, con un backend en FastAPI y un frontend en React para visualización."

**Qué mostrar:**
- Abrir el dashboard del frontend en React en `http://localhost:5173`
- Mostrar el dashboard principal con los 4 gráficos visibles
- Resaltar brevemente la naturaleza interactiva (pasar el cursor sobre un gráfico)

---

## 📊 Parte 1: Adquisición de Datos (1-1.5 minutos)

### Qué Explicar:
1. **Fuente de datos:** Open-Meteo Historical Weather API
2. **Por qué esta fuente:** Datos meteorológicos históricos gratuitos, confiables y completos
3. **Alcance de los datos:** 1,095 registros diarios (2022-2024) para Medellín, Colombia
4. **Puntos de datos recolectados:** Temperatura (máx/mín), precipitación, fecha

### Qué Decir:
> "Primero, veamos cómo adquirimos los datos. Utilizamos la API Open-Meteo Historical Weather, que proporciona acceso gratuito a datos meteorológicos históricos de todo el mundo. Nuestro script descarga 3 años de datos diarios de Medellín, incluyendo temperatura máxima, temperatura mínima y precipitación."

### Qué Mostrar:

**1. Mostrar el script de descarga:**
```bash
# Abrir el archivo en VS Code
code scripts/download_data.py
```

**Resaltar estas partes clave:**
- Línea con coordenadas: `LATITUDE = 6.25, LONGITUDE = -75.56` (Medellín)
- Rango de fechas: `START_DATE = "2022-01-01"` hasta `END_DATE = "2024-12-31"`
- Configuración del endpoint de la API
- Ubicación de salida del CSV: `data/raw/medellin_weather_2022-2024.csv`

**2. Mostrar el archivo de datos crudos:**
```bash
# Abrir el archivo CSV
code data/raw/medellin_weather_2022-2024.csv
```

**Señalar:**
> "Como pueden ver, tenemos 1,095 registros diarios con columnas para fecha, temperatura máxima, temperatura mínima y precipitación. Estos son los datos crudos que serán procesados por nuestros trabajos de MapReduce."

**3. Opcional - Mostrar salida de descarga (si hay tiempo):**
```bash
python scripts/download_data.py
```

---

## ☁️ Parte 2: Almacenamiento en AWS S3 (1-1.5 minutos)

### Qué Explicar:
1. **Por qué S3:** Almacenamiento distribuido accesible por todos los nodos del clúster EMR
2. **Estructura del bucket:** Carpetas organizadas para entrada, salida, scripts y logs
3. **Rol en el pipeline:** Repositorio central de datos entre el desarrollo local y EMR

### Qué Decir:
> "A continuación, necesitamos subir nuestros datos a AWS S3. S3 es el servicio de almacenamiento de objetos de Amazon, y es esencial para EMR porque todos los nodos del clúster necesitan acceso a los mismos datos. No podemos usar archivos locales cuando trabajamos con sistemas distribuidos."

### Qué Mostrar:

**1. Mostrar el script de configuración de S3:**
```bash
code scripts/aws/setup_s3.sh
```

**Explicar las secciones del script:**
- Creación del bucket: `aws s3 mb s3://weatheria-climate-data`
- Estructura de carpetas: `/input/`, `/output/`, `/scripts/`, `/logs/`
- Carga de datos: Subiendo CSV a `/input/`
- Carga de scripts: Subiendo archivos Python de MapReduce a `/scripts/`

**2. Mostrar la Consola de AWS S3 (IMPORTANTE):**
- Abrir la Consola de AWS en el navegador
- Navegar al servicio S3
- Mostrar el bucket `weatheria-climate-data`
- Hacer clic en las carpetas para mostrar:
  - `input/medellin_weather_2022-2024.csv` (los datos fuente)
  - Carpeta `scripts/` con los 3 archivos Python de MapReduce
  - Carpeta `output/` con subcarpetas para los resultados de cada trabajo
  - Carpeta `logs/` con los logs del clúster EMR

**Qué enfatizar:**
> "Esta estructura de bucket es crucial. La carpeta input contiene nuestros datos fuente, la carpeta scripts tiene nuestros trabajos de MapReduce, la carpeta output recibirá los resultados procesados, y la carpeta logs nos ayuda a depurar si algo sale mal. Todo esto es accesible para cada nodo de nuestro clúster EMR."

---

## 🚀 Parte 3: Despliegue en AWS EMR (3-3.5 minutos)

### Qué Explicar:
1. **Qué es EMR:** Servicio de clúster Hadoop administrado
2. **Configuración del clúster:** 3 instancias m5.xlarge (1 maestro, 2 nodos core)
3. **Por qué esta configuración:** Balance entre costo y rendimiento
4. **Envío de trabajos:** Cómo ejecutamos trabajos de MapReduce
5. **Monitoreo:** Cómo rastreamos el progreso de los trabajos

### Qué Decir:
> "Ahora la parte más importante: desplegar nuestros trabajos de MapReduce en AWS EMR. EMR significa Elastic MapReduce, y es el servicio Hadoop administrado de AWS. En lugar de configurar nuestro propio clúster Hadoop, AWS maneja toda la infraestructura por nosotros."

### Qué Mostrar:

**1. Mostrar el script de creación del clúster:**
```bash
code scripts/aws/create_emr_cluster.sh
```

**Resaltar parámetros clave:**
- `--name "Weatheria Climate Observatory"`
- `--release-label emr-6.10.0` (Hadoop 3.3.3, Python 3.9)
- `--instance-type m5.xlarge` (4 vCPU, 16GB RAM)
- `--instance-count 3` (1 maestro + 2 nodos core)
- `--applications Name=Hadoop`
- `--log-uri s3://weatheria-climate-data/logs/`

**Explicar:**
> "Estamos creando un clúster de 3 nodos con instancias m5.xlarge. Esto nos da suficiente poder computacional para procesar nuestros datos eficientemente mientras mantenemos los costos por debajo de $1 para toda la ejecución del procesamiento."

**2. Mostrar la Consola de AWS EMR (CRÍTICO):**
- Navegar al servicio EMR en la Consola de AWS
- Mostrar tu clúster (j-3FG55B8H77VI3) - incluso si está terminado, debe aparecer en el historial
- Hacer clic en el clúster para mostrar:
  - **Pestaña Summary:** Detalles de configuración (3 nodos, m5.xlarge, EMR 6.10.0)
  - **Pestaña Hardware:** Nodos maestro y core
  - **Pestaña Steps:** Los 3 trabajos de MapReduce que fueron ejecutados
  - **Application history:** Rastreo de aplicaciones YARN

**3. Explicar cada trabajo de MapReduce:**

**Mostrar script de envío de trabajos:**
```bash
code scripts/aws/submit_emr_jobs_mrjob.sh
```

**Recorrer los 3 trabajos:**

**Trabajo 1: Temperatura Promedio Mensual**
> "Este trabajo calcula la temperatura máxima y mínima promedio para cada mes. El mapper extrae el año-mes y las temperaturas, y el reducer calcula los promedios. Procesó los 1,095 días y produjo 36 agregados mensuales en aproximadamente 40 segundos."

**Trabajo 2: Clasificación de Temperaturas Extremas**
> "Este trabajo categoriza cada día en clases de temperatura: muy fresco, fresco, normal y muy caliente. El mapper clasifica cada día basándose en umbrales de temperatura, y el reducer cuenta cuántos días caen en cada categoría. Se completó en aproximadamente 17 segundos."

**Trabajo 3: Correlación Temperatura-Precipitación**
> "Este trabajo analiza la relación entre temperatura y precipitación mes a mes. Calcula coeficientes de correlación para mostrar si temperaturas más altas están asociadas con más o menos lluvia. Este trabajo tomó aproximadamente 29 segundos."

**4. Mostrar la ejecución de steps en la Consola EMR:**
- Hacer clic en la pestaña "Steps" en tu clúster
- Mostrar cada step con:
  - Nombre del step
  - Estado (COMPLETED)
  - Hora de inicio y fin
  - Duración
  - Ubicación de salida en S3

**Explicar el flujo de trabajo:**
> "Cada trabajo se ejecuta independientemente. EMR distribuye los datos entre los nodos, ejecuta las funciones map y reduce en paralelo, y escribe los resultados de vuelta a S3. El tiempo total de procesamiento fue de poco menos de 2 minutos para los tres trabajos."

**5. Mostrar la salida de los trabajos en S3:**
- Navegar de vuelta a la consola de S3
- Abrir `weatheria-climate-data/output/`
- Mostrar las tres carpetas de salida:
  - `monthly_avg/part-00000`
  - `extreme_temps/part-00000`
  - `temp_precip/part-00000`
- Hacer clic en un archivo para mostrar su contenido (formato TSV)

**6. Mostrar el script de descarga de resultados:**
```bash
code scripts/aws/download_results.sh
```

**Explicar:**
> "Después de que los trabajos se completan, descargamos los resultados de S3 a nuestra máquina local. Los resultados vienen en formato TSV (valores separados por tabulaciones), que luego convertimos a CSV para un consumo más fácil por nuestra API."

**Mostrar los archivos convertidos:**
```bash
code output/monthly_avg_fixed.csv
```
> "Aquí están los datos finales procesados listos para ser servidos por nuestra API."

**7. IMPORTANTE - Terminación del Clúster:**
```bash
code scripts/aws/terminate_emr_cluster.sh
```

**Enfatizar:**
> "Finalmente, y esto es crucial para la gestión de costos, terminamos el clúster inmediatamente después de descargar los resultados. EMR cobra por hora por nodo, así que dejar un clúster corriendo costaría alrededor de $1.50 por hora. Nuestro costo total fue de menos de $1 porque procesamos todo en menos de 30 minutos."

---

## 📡 Parte 4: API - Resultados y Consumo (1.5-2 minutos)

### Qué Explicar:
1. **Por qué FastAPI:** Moderno, rápido, documentación automática
2. **Cómo funciona:** Lee archivos CSV y sirve vía endpoints REST
3. **Configuración CORS:** Permite que el frontend acceda a la API
4. **Endpoints disponibles:** Tres endpoints principales de datos más utilidades

### Qué Decir:
> "Ahora que tenemos nuestros datos procesados, necesitamos una forma de servirlos. Construimos un backend en FastAPI que lee los archivos CSV de nuestros trabajos de MapReduce y los expone a través de endpoints REST."

### Qué Mostrar:

**1. Mostrar la estructura de la API:**
```bash
code src/api/main.py
```

**Resaltar:**
- Inicialización de FastAPI
- Configuración del middleware CORS (permite conexión del frontend)
- Importación de routers (monthly, extremes, correlation)
- Evento de startup que carga los datos CSV

**2. Mostrar un router en detalle:**
```bash
code src/api/routers/monthly.py
```

**Explicar:**
> "Este endpoint lee el archivo monthly_avg_fixed.csv, lo parsea a JSON y lo retorna. Cada registro incluye el mes, temperatura máxima promedio y temperatura mínima promedio."

**3. Iniciar la API (si no está corriendo):**
```bash
cd src/api
python main.py
```

**Mostrar el mensaje de inicio:**
> "La API se inicia en el puerto 8000 con recarga automática habilitada para desarrollo."

**4. Abrir la documentación Swagger UI:**
- Navegar a `http://localhost:8000/docs` en el navegador

**Demostrar:**
- Hacer clic en `GET /monthly-avg` → "Try it out" → "Execute"
- Mostrar la respuesta con 36 meses de datos
- Señalar el formato JSON

**Probar otros endpoints:**
- `GET /extreme-temps` - Mostrar las 4 categorías con conteos
- `GET /temp-precipitation` - Mostrar datos de correlación
- `GET /stats` - Mostrar estadísticas generales
- `GET /health` - Mostrar verificación de salud

**Explicar el flujo de datos:**
> "Cuando el frontend necesita datos, hace una petición HTTP a estos endpoints. La API lee el archivo CSV, lo convierte a JSON y lo retorna. Esta separación entre procesamiento de datos (MapReduce) y servicio de datos (API) es un patrón común en la ingeniería de datos moderna."

**5. Mostrar un ejemplo de comando curl (opcional):**
```bash
curl http://localhost:8000/monthly-avg
```

---

## 🎨 Parte 5: Visualización con el Frontend (2-2.5 minutos)

### Qué Explicar:
1. **Stack tecnológico:** React + TypeScript + Vite para desarrollo moderno
2. **Librería de visualización:** Recharts para gráficos interactivos
3. **Integración con API:** Axios para peticiones HTTP
4. **Datos en tiempo real:** Todos los gráficos muestran datos en vivo del backend
5. **Experiencia de usuario:** Interactivo, responsivo, informativo

### Qué Decir:
> "Finalmente, exploremos el frontend. Construimos una aplicación React moderna con TypeScript que visualiza todos nuestros datos climáticos en gráficos interactivos. Todos los datos que ven aquí vienen directamente de nuestros resultados de MapReduce a través del backend FastAPI."

### Qué Mostrar:

**1. Mostrar la estructura del frontend:**
```bash
code weatheria-frontend/src/services/api.ts
```

**Explicar:**
> "Este es nuestro cliente de API. Usa Axios para hacer peticiones HTTP al backend. Noten que tenemos métodos para cada endpoint: getMonthlyAverages, getExtremeTemperatures y getTemperaturePrecipitation."

**2. Navegar al código de la página Dashboard:**
```bash
code weatheria-frontend/src/pages/Dashboard.tsx
```

**Resaltar:**
- Hooks `useEffect` que obtienen datos al montar el componente
- Variables de estado que almacenan las respuestas de la API
- Componentes de Recharts (LineChart, PieChart, BarChart, ScatterChart)

**3. Abrir el frontend en vivo:**
- Navegar a `http://localhost:5173` en el navegador
- **Ponerlo en PANTALLA COMPLETA para la demo**

**4. Tour del Dashboard (Página principal):**

**Gráfico de Tendencias de Temperatura (superior izquierda):**
> "Este gráfico de líneas muestra las temperaturas máximas y mínimas mensuales durante 3 años. Pueden ver que Medellín tiene un clima tropical muy estable con temperaturas que van de 24-29°C para máximas y 14-17°C para mínimas. Noten qué tan consistente es—esto es característico de las tierras altas ecuatoriales."

**Pasar el cursor sobre puntos de datos para mostrar interactividad.**

**Gráfico de Distribución de Temperatura (superior derecha):**
> "Este gráfico circular muestra cómo se distribuyen los días entre las categorías de temperatura. El 64% de los días son clima tropical 'normal' entre 27-30°C. Solo el 2% de los días exceden 30°C, y menos del 1% bajan de 20°C. Esto muestra la notable estabilidad climática de Medellín."

**Gráfico de Patrones de Precipitación (inferior izquierda):**
> "Este gráfico de barras muestra la precipitación mensual. Pueden ver el patrón bimodal típico de Medellín—dos temporadas lluviosas por año con períodos más secos entre ellas. Las barras más altas muestran meses con más de 300mm de lluvia."

**Gráfico de Análisis de Correlación (inferior derecha):**
> "Este gráfico de dispersión muestra la relación entre temperatura y precipitación. Cada punto representa un mes. La correlación generalmente negativa sugiere que los meses más cálidos tienden a ser más secos, lo cual se alinea con los patrones climáticos de Medellín."

**5. Navegar a la página de Análisis Mensual:**
- Hacer clic en "Monthly Analysis" en la barra lateral

**Mostrar:**
- Gráfico de área con visualización de rango de temperatura
- Pasar el cursor para mostrar valores exactos de cada mes
- Explicar: "Esto da una vista detallada de las tendencias de temperatura, mostrando tanto máximas como mínimas en un rango. Pueden ver claramente las variaciones estacionales, aunque son sutiles comparadas con climas templados."

**6. Navegar a la página de Análisis Extremo:**
- Hacer clic en "Extreme Analysis" en la barra lateral

**Mostrar:**
- Gráfico de barras con conteos por categoría
- Gráfico circular con porcentajes
- Explicar: "Aquí podemos ver que los días 'frescos' (20-27°C) y 'normales' (27-30°C) dominan. Los días muy calientes son raros, lo cual es interesante para una ubicación tropical—la elevación de 1,495 metros modera la temperatura."

**7. Navegar a la página de Análisis de Precipitación:**
- Hacer clic en "Precipitation Analysis" en la barra lateral

**Mostrar:**
- Gráficos de dispersión de correlación
- Desglose mensual
- Explicar: "Esta página muestra las correlaciones temperatura-precipitación con más detalle. Los coeficientes de correlación van de -0.64 a +0.14, indicando que la relación varía por temporada."

**8. Navegar a la página About:**
- Hacer clic en "About" en la barra lateral
- Mostrar brevemente la información del proyecto

**9. Mostrar diseño responsivo (opcional si hay tiempo):**
- Redimensionar la ventana del navegador para mostrar responsividad móvil
- Explicar: "Toda la aplicación es responsiva y funciona en dispositivos móviles."

**10. Mostrar la consola del desarrollador (vistazo rápido):**
- Presionar F12
- Mostrar pestaña Network
- Refrescar la página
- Señalar las llamadas a la API: "Pueden ver las tres peticiones de API que se hacen para obtener datos cuando la página carga."

---

## 🎓 Parte 6: Conclusiones y Resumen de Arquitectura (30-45 segundos)

### Qué Decir:
> "Permítanme resumir el pipeline completo de datos que hemos construido:
>
> 1. **Recolección de Datos:** Descargamos 3 años de datos meteorológicos de la API Open-Meteo—1,095 registros diarios para Medellín.
>
> 2. **Almacenamiento en la Nube:** Subimos los datos crudos a AWS S3, que actúa como nuestro data lake distribuido accesible para todos los nodos del clúster.
>
> 3. **Procesamiento Distribuido:** Desplegamos un clúster EMR de 3 nodos en AWS y ejecutamos tres trabajos de MapReduce que analizan tendencias de temperatura, clasifican temperaturas extremas y calculan correlaciones de precipitación. Tiempo total de procesamiento: menos de 2 minutos. Costo total: menos de $1.
>
> 4. **Capa de API:** Un backend FastAPI lee los resultados procesados y los expone a través de endpoints REST con documentación automática.
>
> 5. **Visualización:** Un frontend en React obtiene datos de la API y renderiza gráficos interactivos que permiten a los usuarios explorar patrones climáticos.
>
> Esto demuestra un pipeline completo de ingeniería de datos moderna: Extraer, Transformar, Cargar y Visualizar—todo usando herramientas estándar de la industria e infraestructura en la nube."

### Qué Mostrar:
- **Opcional:** Mostrar el diagrama de arquitectura del README
- O crear un diagrama simple en pantalla/papel mostrando: Fuente de Datos → S3 → EMR → CSV → API → Frontend

---

## 📋 Aspectos Técnicos a Mencionar

### Eficiencia de Costos:
> "Todo el procesamiento costó menos de $1 en AWS, demostrando que la computación en la nube hace que el big data sea accesible incluso para proyectos académicos."

### Escalabilidad:
> "Aunque procesamos 1,095 registros, esta misma arquitectura podría escalar a millones o miles de millones de registros simplemente agregando más nodos al clúster EMR."

### Relevancia en el Mundo Real:
> "Este patrón—MapReduce en EMR con almacenamiento S3—es exactamente cómo empresas como Netflix, Airbnb y Spotify procesan petabytes de datos."

### Perspectivas Climáticas:
> "Nuestro análisis reveló que Medellín tiene una excepcional estabilidad climática con el 64% de los días en el rango 'normal'. La correlación negativa entre temperatura y precipitación durante los meses secos confirma el patrón de lluvia bimodal."

### Comparación de Rendimiento:
> "Mientras que el procesamiento simple en Python tomaría menos de un segundo para este dataset, MapReduce en EMR puede escalar a terabytes o petabytes de datos, haciéndolo ideal para ambientes de producción."

---

## 🎬 Consejos para la Presentación

### Antes de Grabar:
1. **Cerrar aplicaciones innecesarias** (ocultar desorden del escritorio)
2. **Limpiar historial/marcadores del navegador** (mantener solo pestañas de AWS, localhost)
3. **Establecer zoom del navegador al 100%** (para claridad)
4. **Probar calidad de audio y video**
5. **Tener todas las terminales/ventanas pre-posicionadas**
6. **Aumentar tamaño de fuente de terminal** para visibilidad
7. **Usar un fondo de escritorio limpio**
8. **Deshabilitar notificaciones** (asistente de concentración de Windows, notificaciones del navegador)

### Durante la Grabación:
1. **Hablar claramente y a ritmo moderado**
2. **Usar el cursor del mouse** para señalar elementos específicos de código/UI
3. **Hacer pausas breves** entre temas para permitir procesamiento
4. **Hacer zoom** en texto pequeño si es necesario
5. **Usar frases como "como pueden ver aquí"** al resaltar elementos
6. **No apresurarse** en los gráficos—dejar que los espectadores absorban las visualizaciones

### Posición de la Cámara (si muestras tu rostro):
- Ventana pequeña en la esquina (opcional)
- O solo screencast con voz en off (recomendado para demos técnicas)

### Edición (si es necesario):
- Agregar diapositiva de título al inicio con nombre del proyecto
- Agregar encabezados de sección como overlays de texto
- Acelerar operaciones lentas (descargas de archivos, inicio de clúster)
- Agregar música de fondo a bajo volumen (opcional)

---

## ⏱️ Resumen de Asignación de Tiempo

| Sección | Tiempo | Enfoque |
|---------|--------|---------|
| Introducción | 0:30 | Enganchar espectadores con demo en vivo |
| Adquisición de Datos | 1:00 | Mostrar script + datos crudos |
| Almacenamiento S3 | 1:30 | Explicar estructura de bucket + consola AWS |
| Despliegue EMR | 3:30 | **MÁS IMPORTANTE** - Mostrar clúster, trabajos, resultados |
| Consumo de API | 2:00 | Demo de Swagger UI + endpoints |
| Visualización Frontend | 2:00 | Tour del dashboard interactivo |
| Conclusión | 0:30 | Resumen de arquitectura |
| **Total** | **11:00** | *Objetivo: 10 min, Buffer: 1 min* |

---

## 🚨 Errores Comunes a Evitar

1. **No decir "ehh" o "umm" excesivamente** - hacer pausas en su lugar
2. **No omitir mostrar la consola de AWS** - esto prueba que realmente desplegaste en la nube
3. **No olvidar mostrar el contenido del bucket S3** - evidencia crítica
4. **No apresurarse en el frontend** - aquí es donde ocurre el impacto visual
5. **No olvidar mencionar el costo** - muestra que entiendes economía de la nube
6. **No mostrar errores/fallas** - tener todo funcionando antes de grabar
7. **No leer código línea por línea** - explicar conceptos, no sintaxis
8. **No pasar demasiado tiempo en la configuración** - enfocarse en resultados y arquitectura

---

## 📝 Plantilla de Guion (Copiar/Pegar para Grabar)

```
[00:00-00:30] INTRODUCCIÓN
"¡Hola! Hoy voy a demostrar Weatheria, una plataforma distribuida de análisis 
de datos climáticos que procesa 3 años de datos meteorológicos usando MapReduce en AWS EMR."
[Mostrar dashboard del frontend]

[00:30-01:30] ADQUISICIÓN DE DATOS
"Primero, veamos cómo recolectamos datos. Usamos la API Open-Meteo Historical Weather 
para descargar 1,095 registros diarios para Medellín, Colombia, cubriendo 2022 a 2024."
[Mostrar script de descarga + CSV crudo]

[01:30-03:00] ALMACENAMIENTO EN AWS S3
"A continuación, subimos nuestros datos a AWS S3. S3 es esencial porque todos los nodos 
de nuestro clúster EMR necesitan acceso a los mismos datos. Aquí está la estructura de nuestro bucket..."
[Mostrar consola S3 con carpetas]

[03:00-06:30] DESPLIEGUE EN AWS EMR
"Ahora el núcleo del proyecto: AWS EMR. Creamos un clúster de 3 nodos con instancias 
m5.xlarge y enviamos tres trabajos de MapReduce..."
[Mostrar consola EMR, explicar cada trabajo, mostrar resultados en S3]

[06:30-08:30] CAPA DE API
"Después del procesamiento, servimos los resultados a través de un backend FastAPI. 
Aquí está la documentación Swagger mostrando todos nuestros endpoints..."
[Demostrar llamadas a API en Swagger UI]

[08:30-10:30] VISUALIZACIÓN DEL FRONTEND
"Finalmente, nuestro frontend en React visualiza los datos. Todos estos gráficos están 
obteniendo datos reales de nuestros resultados de MapReduce. Déjenme guiarlos..."
[Tour del dashboard, mostrar interactividad, explicar perspectivas]

[10:30-11:00] CONCLUSIÓN
"En resumen, hemos construido un pipeline completo de datos: recolección de datos, 
almacenamiento en la nube, procesamiento distribuido en EMR, servicio de API y visualización 
interactiva. Costo total: menos de $1. Esto demuestra ingeniería de datos moderna a escala."
[Mostrar arquitectura o vista final del dashboard]
```

---

## ✅ Lista de Verificación Final Antes de Grabar

- [ ] El backend API está corriendo (`python src/api/main.py`)
- [ ] El frontend está corriendo (`npm run dev` en weatheria-frontend/)
- [ ] La Consola de AWS está abierta mostrando EMR + S3
- [ ] Todos los scripts están listos para abrir en VS Code
- [ ] Las pestañas del navegador están organizadas (AWS, localhost:8000, localhost:5173)
- [ ] El escritorio está limpio
- [ ] Las notificaciones están deshabilitadas
- [ ] La herramienta de grabación de audio/video está lista
- [ ] Has practicado el flujo al menos una vez
- [ ] Tienes agua cerca (¡mantente hidratado!)

---

## 🎯 Criterios de Éxito

Tu video debe demostrar claramente:
1. ✅ Recolección real de datos de API externa
2. ✅ Despliegue real en AWS (clúster EMR + bucket S3 visible en consola)
3. ✅ Ejecución de trabajos MapReduce y resultados
4. ✅ API funcional con endpoints documentados
5. ✅ Frontend interactivo con datos reales
6. ✅ Comprensión de conceptos de sistemas distribuidos
7. ✅ Conciencia de costos y gestión de recursos

---

## 💡 Puntos Extra

Si tienes tiempo extra o quieres impresionar:
- Mostrar la **UI del ResourceManager YARN** del clúster EMR
- Demostrar **descarga de un CSV** desde la API
- Mostrar **seguridad de tipos de TypeScript** en el código del frontend
- Mencionar **factor de replicación** en HDFS/S3
- Discutir **escalabilidad horizontal** (¿qué pasaría si tuviéramos 1 millón de registros?)
- Mostrar **commits de git** probando desarrollo iterativo
- Mencionar **mejoras futuras** (procesamiento en tiempo real, más ciudades, predicciones con ML)

---

¡Buena suerte con tu presentación! 🚀

**Recuerda:** La confianza viene de la preparación. Practica tu flujo, conoce tus puntos clave y entregarás una excelente demostración.
