=======================
Project Digital Indexer
=======================

The **Digital Indexer** is a precision measurement system designed for machine tool research and prototyping. This project demonstrates how to bridge industrial hardware signals with modern mobile interfaces to create a digital readout (DRO) for lathe applications.


.. figure:: /images/hardware/02_DRO_App/Android/01_DRO_APP_LandscapeYellow.jpg
   :alt: 3D View of the BlackPill Interface Board
   :align: center
   :width: 600px
   
   Digital read out of encoder 1, display on Android phone 
   
The PlackPill DRO can handle three encoder inputs.
   
Project Overview
================

The core objective of this project is to track the angular position of a lathe's main spindle in real-time. By utilizing the 32-bit hardware timers of the STM32F411, the system ensures high-resolution data acquisition, which is then transmitted wirelessly to a mobile device.

**Key Workflow:**

1.  **Sensing:** A high-resolution encoder tracks the spindle rotation.
2.  **Processing:** The BlackPill, mounted on the **I/O Carrier**, decodes the signals and calculates the precise angle.
3.  **Transmission:** Data is sent via Bluetooth (HC-05) to a remote device.
4.  **Visualization:** An Android application receives, normalizes, and displays the angle in a user-friendly format.

Documentation Structure
=======================

This documentation is divided into five specialized sections to cover every aspect of the system:

.. toctree::
   :maxdepth: 3

   hardware_setup
   firmware_logic
   android_app
   lathe_integration
   operation_manual
   ex_dro_comm
   
   

.. list-table:: System Components Quick-View
   :widths: 25 75
   :header-rows: 1

   * - Component
     - Description
   * - **BlackPill Hardware**
     - The F411 MCU and the custom I/O Carrier with 24V-tolerant inputs.
   * - **Firmware**
     - C-based HAL implementation for 32-bit encoder tracking and UART comms.
   * - **Android App**
     - Mobile interface for normalization (scaling) and visual readout.
   * - **Lathe Integration**
     - Mechanical mounting of the encoder and sensor alignment on the spindle.
   * - **Operation**
     - Calibration procedures and daily usage instructions.

Development Disclaimer
======================

This setup is an **Evaluation Project**. The hardware is designed as a development sub-assembly for laboratory use. All code and documentation avoid the use of umlauts to ensure maximum compatibility across different development environments.

