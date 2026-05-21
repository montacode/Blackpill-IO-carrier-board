=================
Hardware Overview
=================

The **BlackPill I/O Carrier** is a versatile expansion board designed for the STM32F411 "BlackPill" module. It serves as a bridge for developers to interface low-voltage microcontrollers with 24V environments during the prototyping phase.

.. image:: /images/hardware/01_BlackPillInterface/BlackPillInterface_3D.jpg
   :alt: 3D View of the BlackPill Interface Board
   :align: center
   :width: 600px

Main Features
-------------

* **I/O Evaluation:** Provides 24V-tolerant digital inputs with integrated clamping protection for safe signal testing.
* **Signal Conditioning:** Supports analog or PWM output experiments via specialized rail-to-rail OpAmp stages.
* **Prototyping Design:** Optimized footprint for easy integration into test setups or experimental control cabinets.
* **Expandability:** Dedicated headers for HC-05 Bluetooth modules or other serial tools for remote debugging and diagnostics.

Technical Description
---------------------

The carrier board facilitates power distribution and signal level shifting for development purposes. It is designed to help protect sensitive STM32 pins from voltage spikes and noise while evaluating firmware in laboratory settings.

Typical Applications
--------------------

* **Digital Readout (DRO) Prototyping:** Evaluating high-speed signal processing for linear encoders.
* **Embedded Development:** Rapid creation of custom controllers without the need for unstable breadboard setups.
* **Remote Diagnostics:** Wireless monitoring of system states during the development cycle via expansion ports.
* **Motor Control Testing:** Generating protected PWM signals to evaluate industrial-grade motor drivers.

.. note::
   For detailed electrical specifications, schematics, and pinout tables, please refer to the :doc:`pcb_details` section.

Development and Evaluation Notice
---------------------------------

This hardware is a **Development Kit** intended solely for evaluation and research by qualified personnel in controlled environments. It has not undergone formal EMC testing. The user is responsible for ensuring electromagnetic compatibility and safety when integrating this sub-assembly into any larger system. For specific setups, such as energy monitoring in a boiler room, ensure the board is housed in an enclosure that protects against moisture and temperature fluctuations.