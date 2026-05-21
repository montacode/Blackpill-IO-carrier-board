Hardware Overview
=================

The **BlackPill I/O Carrier** is a professional expansion board designed for the STM32F411 "BlackPill" module. It serves as a robust bridge between low-voltage microcontrollers and the demanding 24V environment typical of industrial automation.

.. image:: /images/hardware/01_BlackPillInterface/BlackPillInterface_3D.jpg
   :alt: 3D View of the BlackPill Interface Board
   :align: center
   :width: 600px

Main Features
-------------

* **Industrial I/O:** Provides 24V-tolerant digital inputs with integrated clamping protection for safe operation.
* **Signal Conditioning:** Analog or PWM outputs via specialized rail-to-rail OpAmp stages.
* **Compact Design:** Optimized footprint for easy integration into machine control cabinets.
* **Expandability:** Dedicated headers for HC-05 Bluetooth modules or other serial communication tools for remote diagnostics.

Technical Description
---------------------

The carrier board manages power distribution and signal level shifting. It ensures that the sensitive STM32 pins are isolated from high-voltage spikes and noise common in factory settings.

Typical Applications
--------------------

* **Digital Readout (DRO):** High-speed signal processing for linear encoders on manual machine tools.
* **Industrial Prototyping:** Rapid development of custom controllers without the need for breadboarding.
* **Diagnostics:** Wireless monitoring of machine states via the integrated expansion ports.
* **Motor Control:** Generating protected PWM signals for industrial motor drivers.

.. note::
   For detailed electrical specifications, schematics, and pinout tables, please refer to the :doc:`pcb_details` section.