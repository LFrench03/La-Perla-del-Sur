# <h1 align=center><b>Formulario</b></h1>

---

## <h2 align=center><b>Preview:</b></h2>

[![preview](capt.png)](https://qqhgi39b.forms.app/la-perla-del-sur)

---
- [**CSV con respuestas**](data/La-Perla-del-Sur-Form.csv)

## <h2 align=center><b>Diagrama de Flujo:</b></h2>

```mermaid
%%{init:{'theme':'base', 'themeVariables':{'primaryColor': '#356bca','edgeLabelBackground': '#738a97', 'primaryTextColor': '#bbe2ec', 'lineColor': '#ffffff','primaryBorderColor': '#ffffff'}}}%%
flowchart TD

    A[Rango de Edad]--10-16 --> B{¿Cuál es tu género?}
    A --17-25 -->B
    A --26-50 -->B
    A --51-66 -->B
    A --68 o más -->B

    B --Masculino -->C[Conoce a Perla]
    B --Femenino  -->C
    B --Otro  -->C

    C --Lic. Bioquímica en la UH -->D{¿Qué elegirías?}
    C --Medicina Veterinaria en Cienfuegos -->D
    C --Otro  -->D

    D --¿Por qué? -->E{¿Estaría en tus planes futuros emigrar en algún momento?}

    E --Sí... ¿Por qué? -->F{¿Cómo sería tu proceso migratorio?}
    E --No... ¿Por qué? -->K{¿Buscarías a tu padre?}

    F --Interno -->G{¿Intermunicipal o interprovincial?}
    F --Externo -->M{¿Hacia dónde irías?}

    G --Intermunicipal -->L{¿Cuál sería tu lugar de destino?}
    G --Interprovincial -->H{¿Cuál sería tu destino?}

    H --Provincia -->I{¿Por qué crees que decidirías emigrar?}

    I  --> J{¿Cómo les ofrecerías apoyo a la familia?}
    J  --> K

    K --Sí... ¿Por qué? -->N{¿Te llamó la atención la imagen de la chica al principio del cuestionario?}
    K --No... ¿Por qué? -->N

    N  --> X[FIN]
    L --La capital de mi provincia natal -->I
    L --Otro municipio -->I
    M -- Región --> I
    style A font-size:20px,font-family:monospace, monaco
    style B font-size:20px,font-family:monospace, monaco
    style C font-size:20px,font-family:monospace, monaco
    style D font-size:20px,font-family:monospace, monaco
    style E font-size:20px,font-family:monospace, monaco
    style F font-size:20px,font-family:monospace, monaco
    style G font-size:20px,font-family:monospace, monaco
    style H font-size:20px,font-family:monospace, monaco
    style I font-size:20px,font-family:monospace, monaco
    style J font-size:20px,font-family:monospace, monaco
    style K font-size:20px,font-family:monospace, monaco
    style L font-size:20px,font-family:monospace, monaco
    style M font-size:20px,font-family:monospace, monaco
    style N font-size:20px,font-family:monospace, monaco
    style X font-size:20px,font-family:monospace, monaco
```
