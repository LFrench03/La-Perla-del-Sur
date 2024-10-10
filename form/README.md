# **Formulario**
---
## **Preview** 
[![preview](capt.png)](https://qqhgi39b.forms.app/la-perla-del-sur)

---

### Diagrama de Flujo:
---

```mermaid
flowchart TD
    A[Rango de Edad]
    B{¿Cuál es tu género?}
    C[Conoce a Perla]
    D{¿Qué elegirías?}
    E{¿Estaría en tus planes futuros emigrar en algún momento?}
    F{¿Cómo seria tu proceso migratorio?}
    G{¿Intermunicipal o interprovincial?}
    H{¿Cual sería tu destino?}
    I{¿Por qué crees que decidirías emigrar?}
    J{¿Cómo les ofrecerías apoyo a la familia?}
    K{¿Buscarías a tu padre?}
    L{¿Cuál sería tu lugar de destino?}
    M{¿Hacia donde irias?}
    N{¿Te llamó la atención la imagen de la chica al principio del cuestionario? (Contexto)}


    A --> [10-16] B

    A --> [17-25] B

    A --> [26-50] B

    A --> [51-66] B

    A --> [>=68] B


    B --> [Masculino] C

    B --> [Femenino] C

    B --> [Otro] C


    C --> [Lic. Bioquimica(UH)] D

    C --> [Medicina Veterinaria(Cienfuegos)] D

    C --> [Otro] D


    D -- [¿Porqué?] E


    E --> [Si...¿Porqué?] F

    E --> [No...¿Porqué?] K


    F --> [Interno] G

    F --> [Externo] M


    G --> [Intermunicipal] L

    G --> [Interprovincial] H

    H --> [Provincia] I


    I --> J


    J --> K


    K --> [Si...¿Porqué?] N

    K --> [No...¿Porqué?] N


    N--> X[FIN]

    L--> [La capital de mi provincia natal (Cienfuegos)] I

    L--> [Otro municipio] I

```
---
