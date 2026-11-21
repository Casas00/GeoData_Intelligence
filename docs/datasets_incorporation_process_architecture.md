# Arquitectura del proceso de incorporación de datasets

## 1. Objetivo

La plataforma permite incorporar datasets de distintas fuentes y
estructuras a un catálogo de datos geoespaciales. Para ello, inspecciona
los datos de origen, propone cómo adaptarlos a un modelo lógico y
ejecuta la transformación y la ingesta después de que el usuario haya
revisado y aprobado las decisiones relevantes.

> **La IA analiza y propone; la plataforma valida y ejecuta; el usuario
> conserva el control de las decisiones.**

El archivo original se mantiene intacto durante todo el proceso.

## 2. Visión general del flujo

``` mermaid
flowchart TD
    A[El usuario proporciona un dataset] --> B[Inspección preliminar]
    B --> C{¿La capa tiene geometría homogénea?}
    C -- Sí / Tabular --> E[Análisis frente a modelos lógicos]
    C -- No --> D[Propuesta de separación por tipo geométrico]
    D --> F{¿El usuario aprueba?}
    F -- No --> X[Detener e informar al usuario]
    F -- Sí --> G[Generar conjuntos homogéneos]
    G --> E
    E --> H[La IA recomienda un modelo lógico]
    H --> I{¿El usuario confirma?}
    I -- No --> J[Revisar selección o solicitar aclaraciones]
    J --> E
    I -- Sí --> K[La IA propone la adaptación]
    K --> L[El usuario revisa y aprueba]
    L --> M[Transformación y validación]
    M --> N{¿El resultado es válido?}
    N -- No --> Y[Informar de errores y detener]
    N -- Sí --> O[Preparar tabla de destino]
    O --> P[Ingesta en PostgreSQL / PostGIS]
    P --> Q[Registrar metadatos y trazabilidad]
    Q --> R[Dataset incorporado al catálogo]
```

Si una fuente contiene varias capas independientes, cada capa puede
seguir el flujo por separado. Si una capa heterogénea se divide por tipo
geométrico con aprobación del usuario, cada conjunto resultante continúa
como un dataset independiente y conserva su relación de procedencia con
el original.

## 3. Etapas del proceso

### 3.1. Recepción del dataset

El usuario proporciona el archivo que desea incorporar. La plataforma
conserva el original y trabaja sobre una copia, una representación
temporal o un flujo de lectura.

### 3.2. Inspección preliminar

Antes del análisis de IA, la plataforma realiza una inspección técnica
para identificar:

-   Formato y estructura del archivo.
-   Capas disponibles, cuando el formato permita contener varias.
-   Nombres de campos y tipos de datos detectados.
-   Número de registros.
-   Sistema de referencia de coordenadas (CRS), cuando esté disponible.
-   Tipo o tipos de geometría presentes.
-   Distribución de registros por tipo geométrico.
-   Homogeneidad geométrica de cada capa.

Esta etapa describe cómo están organizados los datos, pero todavía no
intenta deducir su significado temático.

#### Tratamiento de geometrías heterogéneas

La plataforma trabaja con capas espaciales homogéneas. Si una capa
contiene distintos tipos geométricos, propone al usuario separarla en
conjuntos homogéneos.

-   **Si acepta:** se generan conjuntos independientes por tipo
    geométrico y cada uno continúa el proceso por separado.
-   **Si rechaza:** el proceso se detiene y se informa de que la
    plataforma no puede incorporar esa capa sin homogeneidad espacial.

La separación geométrica no implica una clasificación temática. Separar
puntos y polígonos no significa que la plataforma haya determinado qué
representan.

### 3.3. Análisis y selección del modelo lógico

Con la información de la inspección, la plataforma prepara el contexto
para que la IA analice el dataset frente al catálogo de modelos lógicos.

La IA puede recomendar un modelo existente, indicar que no encuentra uno
adecuado, proponer la creación de un nuevo modelo o versión, o solicitar
información adicional si no dispone de suficiente contexto.

La propuesta se presenta al usuario. El modelo lógico no se selecciona
ni se crea definitivamente sin su confirmación.

### 3.4. Propuesta de adaptación

Una vez confirmado el modelo lógico de destino, la IA analiza la
estructura de origen y propone cómo adaptar los datos. La propuesta
puede incluir:

-   Correspondencia entre campos de origen y destino.
-   Renombrado de campos.
-   Conversiones de tipos de datos.
-   Campos de destino sin correspondencia en el origen.
-   Campos de origen que no se utilizarán.
-   Tratamiento propuesto para valores nulos o ausentes.
-   Transformación del CRS, cuando sea necesaria.
-   Advertencias o dudas que requieran revisión.

Los nombres de los campos de origen no tienen por qué coincidir con los
del modelo lógico. La correspondencia se basa en su significado y en la
información disponible, no en una coincidencia literal de nombres.

La IA genera una propuesta; el usuario la revisa y la aprueba antes de
ejecutar cualquier transformación.

### 3.5. Transformación y validación

El servicio de transformación recibe el dataset original o su
representación temporal, la definición del modelo lógico de destino y la
propuesta de adaptación aprobada.

Aplica las transformaciones autorizadas y genera un dataset preparado
para la ingesta. Entre sus responsabilidades están:

-   Adaptar nombres y correspondencias de campos.
-   Convertir tipos de datos cuando la conversión esté definida y sea
    válida.
-   Aplicar las reglas aprobadas para valores nulos.
-   Reproyectar geometrías cuando el CRS de origen y destino sean
    distintos.
-   Validar la estructura y los tipos de datos resultantes.
-   Comprobar la compatibilidad del tipo geométrico con el destino.
-   Validar geometrías y coordenadas.
-   Comprobar que el resultado cumple la definición de destino.

La validación geométrica contempla, según el tipo de geometría, aspectos
como geometrías vacías, anillos de polígonos, autointersecciones y
estructura geométrica.

Las comprobaciones de coordenadas se centran en la coherencia técnica
con el CRS declarado: valores finitos, dimensionalidad, rangos y
unidades razonables. Pueden detectar valores sospechosos, pero no
demostrar por sí solas que el CRS esté correctamente declarado ni
interpretar el contexto geográfico real de cada elemento.

Los errores que impidan garantizar la compatibilidad bloquean la
ingesta. Las situaciones sospechosas que no sean concluyentes pueden
comunicarse como advertencias.

El archivo original no se modifica.

### 3.6. Preparación de la estructura de destino

Cuando el resultado transformado ha superado las validaciones, la
plataforma prepara la tabla física correspondiente en PostgreSQL o
PostGIS.

La estructura se crea de acuerdo con la definición lógica aprobada,
incluyendo campos, tipos, restricciones y, para datos vectoriales, la
columna geométrica con su tipo y CRS.

La creación de la tabla es una operación diferenciada de la
transformación y de la ingesta.

### 3.7. Ingesta

El servicio de ingesta recibe el dataset transformado y la definición de
destino. Sus responsabilidades son:

-   Realizar una comprobación defensiva final de compatibilidad.
-   Insertar los registros en la tabla de destino, preferiblemente por
    lotes.
-   Gestionar transacciones y errores.
-   Recopilar estadísticas del proceso, como registros procesados,
    insertados o rechazados.

La ingesta no vuelve a ejecutar las transformaciones. La lógica completa
de adaptación y validación corresponde al servicio de transformación; la
comprobación de ingesta actúa como última barrera de seguridad.

### 3.8. Registro y trazabilidad

La plataforma registra la información necesaria para localizar el
dataset y conocer su procedencia:

-   **Modelos lógicos y versiones:** definición de la estructura de
    destino utilizada.
-   **Datasets:** información descriptiva y localización de la tabla
    física.
-   **Fuentes:** procedencia del archivo o conjunto incorporado.
-   **Trabajos de ingesta:** estado, fechas, contadores y errores.
-   **Historial de transformaciones:** operaciones aplicadas y relación
    con el trabajo de ingesta.

Cuando un dataset se divide durante la inspección, debe conservarse la
relación entre los conjuntos resultantes y el archivo o dataset
original.

## 4. Responsabilidades de los componentes

  -----------------------------------------------------------------------
  Componente                          Responsabilidad principal
  ----------------------------------- -----------------------------------
  Inspección preliminar               Describir técnicamente el archivo,
                                      sus capas, campos, CRS y
                                      geometrías.

  IA / análisis de modelos            Recomendar un modelo lógico y
                                      proponer correspondencias y
                                      adaptaciones.

  Interfaz de usuario                 Mostrar las propuestas y permitir
                                      aprobarlas o rechazarlas.

  `transformation_service`            Ejecutar las transformaciones
                                      aprobadas y validar el resultado
                                      completo.

  `thematic_table_service`            Crear la estructura física de
                                      destino en PostgreSQL/PostGIS.

  `ingestion_service`                 Comprobar la compatibilidad final e
                                      insertar los datos.

  Servicios de metadatos              Registrar modelos, datasets,
                                      fuentes, trabajos e historial.
  -----------------------------------------------------------------------

## 5. Principios y límites del diseño

1.  **Control del usuario:** las decisiones relevantes propuestas por la
    IA requieren aprobación.
2.  **Separación de responsabilidades:** inspección, análisis,
    transformación, creación de tablas e ingesta son etapas
    diferenciadas.
3.  **Original intacto:** la plataforma no modifica el archivo
    proporcionado.
4.  **Ejecución controlada:** Python aplica las transformaciones
    mediante lógica definida y validada; la IA no ejecuta SQL ni opera
    directamente sobre la base de datos.
5.  **Compatibilidad explícita:** la estructura final debe ajustarse al
    modelo lógico aprobado.
6.  **Geometría homogénea:** cada tabla espacial de destino tiene un
    tipo geométrico definido; no se mezclan arbitrariamente puntos,
    líneas y polígonos en una misma columna.
7.  **Trazabilidad:** se conserva la relación entre los datos
    incorporados, su fuente, el modelo lógico y las operaciones
    realizadas.
8.  **Errores antes que datos inconsistentes:** si una transformación no
    puede garantizar un resultado compatible, no se continúa con la
    ingesta.

## 6. Alcance de las conversiones geométricas

En la primera versión se prioriza la validación estricta del tipo
geométrico y la transformación del CRS. No se realizan automáticamente
conversiones que puedan alterar el significado o la cardinalidad de los
datos.

Algunas conversiones simples podrían contemplarse en el futuro bajo
reglas explícitas. Por ejemplo, un `Polygon` podría representarse como
un `MultiPolygon` de un único componente. En cambio, dividir
automáticamente un `MultiPolygon` en varios registros cambiaría la
cardinalidad y requeriría una decisión explícita.

------------------------------------------------------------------------

*Documento de arquitectura funcional del proceso de incorporación de
datasets. Describe el flujo previsto y las responsabilidades de sus
componentes; no implica que todas las etapas estén ya implementadas.*
