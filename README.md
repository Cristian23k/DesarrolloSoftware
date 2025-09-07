# Actividad 1 – Introducción a DevOps y DevSecOps

**Curso:** CC3S2 Desarrollo de Software  
**Estudiante:** <Cristian Diaz>  
**Fecha:** 30/08/2025  
**Tiempo invertido:** <1h:30min>

**Entorno usado (breve y sin datos sensibles):**  
Navegador web para inspección (DevTools), sitios públicos para DNS/TLS, diagramado en draw.io/Excalidraw. Sin credenciales ni tokens.

---

<!-- Commit: Día 1 - Comparativos e imágenes base -->

## 1. DevOps vs. cascada tradicional (investigación + comparación)

**Imagen:** `imagenes/devops-vs-cascada.png` (ciclos de feedback visuales, no solo cajas).

**Síntesis:**  
DevOps acelera y reduce riesgo en la nube al **acortar ciclos de feedback**, trabajar en **lotes pequeños**, automatizar pruebas y despliegues y **alinear Dev-Ops**. Esto reduce tiempos de integración, _lead time_, y tasa de fallos, y mejora MTTR (métricas DORA) [fuente DORA]. La **config externa y port binding (12-Factor)** favorecen reproducibilidad entre entornos [fuente 12-Factor].  
**Fuentes clave:** DORA (Four Keys), 12-Factor.

**Contexto donde “cascada” aún es razonable:**

- **Sistemas con certificaciones regulatorias estrictas** (p. ej., médicos/aeronáuticos).
  - _Criterio 1 (verificable):_ cada release requiere **evidencia de conformidad** con estándar/regulación (p. ej., checklist firmado por QA externo).
  - _Criterio 2 (verificable):_ **cambios agrupados** con aprobación de organismo/cliente antes de producción.
  - _Trade-off:_ menor velocidad vs. mayor conformidad/seguridad.

> Referencias orientativas: DORA – Four Keys; 12-Factor App.

---

<!-- Commit: Día 1 - Comparativos e imágenes base -->

## 2. Ciclo tradicional de dos pasos y silos (limitaciones y anti-patrones)

**Imagen:** `imagenes/silos-equipos.png` (mostrar handoffs entre Dev, Ops, Seguridad).

**Limitaciones sin CI:**

1. **Lotes grandes** → más retrabajos y riesgos de regresión.
2. **Colas de defectos** y **costo de integración tardía** (defectos descubiertos tarde).

**Anti-patrones (y su efecto):**

- **“Throw over the wall”**: Dev “lanza” a Ops sin contexto → aumenta **MTTR** por asimetrías de información.
- **Seguridad como auditoría tardía**: hallazgos al final → regresiones repetidas y bloqueos de release.

---

<!-- Commit: Día 1 - Comparativos e imágenes base -->

## 3. Principios y beneficios de DevOps (CI/CD, automatización, colaboración; Agile)

**CI/CD (clave):** cambios pequeños, pruebas automatizadas cerca del código, _pipelines_ reproducibles, _trunk-based_ y _feature flags_ cuando aplique.  
**Agile como precursor:** _dailies_ y _retros_ alimentan qué promover o bloquear (definen políticas y prioridades).

**Indicador observable de colaboración (no financiero):**

- **“PR listo → despliegue en pruebas” (p50)**.
  - _Cómo recolectarlo (sin pagos):_ tiempos en metadatos de PR (creación/“ready for review”/merge) + tiempo de primer despliegue en ambiente de pruebas (bitácora de despliegue).
  - _Meta inicial:_ reducir p50 en un **30%** en 4 iteraciones.

---

<!-- Commit: Día 2 - DevSecOps y estrategia de despliegue -->

## 4. Evolución a DevSecOps (SAST/DAST; cambio cultural)

**Diferencias:**

- **SAST**: análisis **estático y temprano** en artefactos y dependencias; detiene fallos antes de ejecutar.
- **DAST:** **dinámico en ejecución**, valida rutas vivas y configuraciones.  
  (Colócalos en el pipeline en tu diagrama de la sección 5.)

**Gate mínimo de seguridad (umbrales y excepción):**

- **SAST:** **0** vulnerabilidades **críticas/altas** (CVSS ≥ 7.0) antes de promoción.
- **DAST:** **≥ 80%** de cobertura en **rutas críticas** de la API.
- **Política de excepción:** cuando algo crítico no es corregible de inmediato, **excepción de 7 días**, con **responsable** (<rol/nombre>), **mitigación** (p. ej., regla temporal en WAF) y **re-evaluación** programada.

**Evitar “teatro de seguridad”:**

- **Señal 1:** ↓ **hallazgos repetidos** en SAST/DAST a **≤ 5%**.
- **Señal 2:** **Tiempo de remediación** de críticos **≤ 48 h**.  
  (Medir comparando informes consecutivos y bitácoras de corrección.)

> Marco de apoyo: NIST **SSDF** (prácticas de desarrollo seguro).

---

<!-- Commit: Día 2 - DevSecOps y estrategia de despliegue -->

## 5. CI/CD y estrategias de despliegue (sandbox, canary, azul/verde)

**Imagen:** `imagenes/pipeline_canary.png` (pipeline con control de canary).

**Estrategia elegida (ejemplo: microservicio de autenticación):**  
**Canary** para limitar _blast radius_ y comparar contra control.

**Riesgos vs. mitigaciones:**
| Riesgo | Mitigación |
|----------------------|---------------------------------------------------------------------------------|
| Regresión funcional | **Validación de contrato** y _smoke tests_ antes de promover |
| Costo de convivencia | **Límites de tiempo** de canary (p. ej., 60 min) y auto-rollback |
| Manejo de sesiones | **Draining** + compatibilidad de esquema y _sticky sessions_ si aplica |

**KPI primario y umbral (gate técnico):**

- **Tasa de errores HTTP 5xx ≤ 0.1%** en **1 h** post-despliegue canary.
- **Ventana y decisión:** si supera umbral → **rollback**; si se mantiene → **promoción**.  
  **Métrica de producto (coexistente):** **Conversión ≥ 95%** del valor base pre-release.  
  _(Ambas métricas deben convivir: estabilidad técnica sin impacto negativo en usuario final.)_

---

<!-- Commit: Día 3 - Evidencia, diagramas y entrega final -->

## 6. Fundamentos prácticos sin comandos (evidencia mínima)

> Todas las capturas en `/imagenes/` con flechas/recuadros sobre campos clave. No exponer secretos.

### 6.1 HTTP – contrato observable

**Captura:** `imagenes/http-evidencia.png`.  
**Reportar (ejemplo real):**

- Método: **GET**
- Código: **200**
- Cabeceras: **Cache-Control: max-age=3600** (mejora rendimiento al cachear) y **X-Request-ID: <valor>** (trazabilidad).  
  **Por qué importa:** caché reduce latencia; _request id_ habilita correlación de logs.

### 6.2 DNS – nombres y TTL

**Captura:** `imagenes/dns-ttl.png`.  
**Reportar:** tipo de registro (**A** o **CNAME**) y **TTL** (p. ej., **3600 s**).  
**Interpretación:** TTL alto **retrasa rollbacks/cambios** por propagación lenta; TTL bajo acelera cambios pero puede aumentar consultas.

### 6.3 TLS – seguridad en tránsito

**Captura:** `imagenes/tls-cert.png`.  
**Reportar:** **CN/SAN**, **vigencia (desde/hasta)** y **emisora**.  
**Si falla la cadena:** errores de confianza, riesgo de **MITM** y mala UX (bloqueos/advertencias).

### 6.4 Puertos – estado de _runtime_

**Captura:** `imagenes/puertos.png`.  
**Reportar:** dos puertos en escucha (p. ej., **80/HTTP** y **443/HTTPS**) y qué servicio sugieren.  
**Utilidad:** detectar despliegue incompleto (**443** ausente) o conflicto (**puerto ocupado**).

### 6.5 12-Factor – port binding, configuración, logs

- **Port binding:** parametrizar el puerto vía **configuración externa** (variable de entorno o _settings_ del entorno) **sin tocar código**.
- **Logs:** enviar a **flujo estándar** para agregación/observabilidad; **no** rotar manualmente en archivos locales.
- **Anti-patrón:** credenciales en el repositorio → rompe reproducibilidad y seguridad.

### 6.6 Checklist de diagnóstico (intermitencia simulada)

1. **Contrato HTTP**
   - _Objetivo:_ validar método/código/cabeceras esperadas.
   - _Evidencia:_ 2xx/3xx con cabeceras correctas.
   - _Acción:_ si faltan o hay 4xx/5xx → revisar _routing_ o _backends_.
2. **DNS**
   - _Objetivo:_ consistencia de **A/CNAME** y **TTL**.
   - _Evidencia:_ respuestas coherentes entre _resolvers_.
   - _Acción:_ si hay divergencias/TTL alto → esperar ventana o ajustar plan de rollback.
3. **TLS**
   - _Objetivo:_ cert vigente, **CN/SAN** correctos, emisora confiable.
   - _Evidencia:_ candado sin advertencias.
   - _Acción:_ si caducado/host mismatch → renovar/corregir _chain_.
4. **Puertos**
   - _Objetivo:_ verificar **80/443** expuestos por el servicio correcto.
   - _Evidencia:_ puertos abiertos por el proceso esperado.
   - _Acción:_ si falta 443 → revisar configuración TLS o _listener_.
5. **Tráfico canary vs. control**
   - _Objetivo:_ comparar KPIs (5xx, p95) y conversión.
   - _Evidencia:_ canary bajo umbral.
   - _Acción:_ si falla → **rollback** inmediato.
6. **Logs de correlación (X-Request-ID)**
   - _Objetivo:_ rastrear una solicitud extremo-a-extremo.
   - _Evidencia:_ trazas coherentes entre _ingress_ y servicio.
   - _Acción:_ si faltan → habilitar/ajustar _middleware_ de trazabilidad.

---

<!-- Commit: Día 3 - Evidencia, diagramas y entrega final -->

## 7. Desafíos de DevOps y mitigaciones

**Imagen:** `imagenes/desafios_devops.png` (3 desafíos: culturales, técnicos, gobernanza).

**Riesgos y mitigaciones concretas:**

- **Cambios no observables** → _feature flags_ + _rollbacks_ probados.
- **Blast radius amplio** → **despliegue gradual/canary** + límites claros.
- **Errores humanos en operación** → revisión cruzada + automatización de _runbooks_.

**Experimento controlado (canary vs. big-bang):**

- **Métrica primaria:** tasa de **5xx** y **p95** en 60 min.
- **Control:** release big-bang de referencia previa.
- **Éxito:** canary reduce **5xx** ≥ 50% vs. big-bang a igual carga.
- **Reversión:** si KPI supera umbral, rollback automático.

---

<!-- Commit: Entrega actividad 1 -->

## 8. Arquitectura mínima para DevSecOps (HTTP/DNS/TLS + 12-Factor)

**Imagen:** `imagenes/arquitectura-minima.png`  
**Flujo:** Cliente → **DNS** → Servicio (**HTTP**) → **TLS** (terminación/validación).  
**Controles:** políticas de caché, validación de certificado, contratos de API, límites de tasa.  
**12-Factor relacionados:**

- **Config por entorno:** diffs mínimos entre ambientes, fácil auditoría.
- **Logs a stdout:** trazabilidad de eventos (correlación con X-Request-ID).

---

<!-- Commit: Entrega actividad 1 -->

## Trazabilidad (commits sugeridos)

1. `Día 1 - Comparativos e imágenes base`
2. `Día 2 - DevSecOps y estrategia de despliegue`
3. `Día 3 - Evidencia, diagramas y entrega final`
4. `Entrega actividad 1`
