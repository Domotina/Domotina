# Domotina
## Estado
[![Build Status](https://travis-ci.org/Domotina/domotina.svg?branch=dev)](https://travis-ci.org/Domotina/domotina)
[![Codacy Badge](https://www.codacy.com/project/badge/1e19fe0af18b4c4981ce27578a6944e0)](https://www.codacy.com/public/kaosterra/domotina)
## Introducción
Durante los últimos años, el avance de la tecnología en dispositivos móviles, sensores inalámbricos, avances en sistemas de domótica y sistemas embebidos han hecho posible la automatización de soluciones de monitoreo remoto y automatización de viviendas inteligentes. Particularmente, en este último campo, el uso de internet y dispositivos móviles abren todo un nuevo campo de acción para automatización de tareas domésticas, control remoto de viviendas, manejo proactivo de alarmas, control de activos e interacción con electrodomésticos en tiempo real.

La empresa **SmartHome (SH)**, ha decidido incursionar en la construcción de viviendas inteligentes, que brinden tecnologías de punta en control remoto de viviendas a sus clientes, manteniendo costos razonables que permitan masificar su utilización. SH desea contratar a su grupo para el desarrollo de una aplicación que le permita ofrecer a sus clientes un valor agregado mas allá de la construcción tradicional.

El sistema a desarrollar debe poder controlar una casa u oficina ofreciendo acceso remoto e información de control a los diferentes propietarios. Esto quiere decir que un sistema central recopila la información de todos los sensores de todas las viviendas y/o oficinas bajo su cargo. Estos datos son recibidos y procesados de tal forma que cada propietario, luego de identificarse en el sistema, tenga acceso al sistema de administración y consulta de su vivienda u oficina.

Desde el punto de vista de los usuarios de la central (operadores de la constructora, administración del proyecto o compañías de seguridad), se requiere poder administrar las viviendas u oficinas bajo su control, lo cual incluye la gestión de la información de los inmuebles y de los usuarios autorizados en cada uno de ellos. El sistema central debe estar disponible en todo momento y debe garantizar que sólo los usuarios asignados a una vivienda pueden tener acceso a dicha información.

Una urbanización o conjunto de oficinas puede crecer paulatinamente hasta tener cientos de viviendas bajo su control, por lo que el sistema a desarrollar debe estar en capacidad de escalar adecuadamente. Adicionalmente, algunas operaciones críticas deben ser atendidas de manera inmediata. Por ejemplo, si un sensor de humo o una alarma de intrusos se prende en algún sitio, se debe informar en menos de **1 segundo** a los propietarios y a las autoridades sobre dicho incidente.

Los propietarios de una vivienda pueden consultar la información del sistema desde dispositivos móviles o clientes web para consultar de manera intuitiva y ágil el estado de su vivienda. Por ejemplo, un usuario debe poder ver un mapa de su vivienda u oficina, en la que se indique qué luces están prendidas, en qué estado se encuentran sus electrodomésticos, en qué estados están las puertas y ventanas de su casa y en qué partes de la vivienda hay movimiento.

Adicionalmente, cada electrodoméstico dentro de una casa, puede ser marcado con un tag *RFID*, de tal forma que se sepa en todo momento donde se encuentra cada activo registrado a una vivienda. Así por ejemplo, un televisor puede tener un tag *RFID* que indica la posición en la vivienda donde está ubicado. Un usuario puede definir alarmas para indicar qué partes de la vivienda están autorizadas para un activo y en qué horarios está permitido su uso en esa parte de la vivienda. Por ejemplo, una alarma podría enviarse para indicar que un televisor, el equipo de sonido y la cámara fotográfica, abandonaron el apartamento en un horario no permitido.

El propietario de una vivienda debe poder tener reportes de actividades de su vivienda. Estos reportes permitirán consultar todos los eventos sucedidos en un periodo de tiempo en su vivienda. De igual forma, los administradores del sistema deben poder generar reportes de forma instantánea a partir de la información disponible en el sistema (p.ej. usuarios y viviendas registradas en el sistema, actividades registradas sobre los electrodomésticos de las viviendas de una urbanización, número de alertas generadas por el sistema durante un periodo de determinado de tiempo, etc.).
##Equipo de trabajo
|Nombre|Rol|
|:-:|:-:|
|Raúl Gómez|Team Member|
|David Jiménez|Team Member|
|Luis Florez|Team Member|
|Cindy Hernández|Team Lead|
|Luis Mendivelso|Architecture Owner|
|Andrés Esguerra|ProductOwner|
