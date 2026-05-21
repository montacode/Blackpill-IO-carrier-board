
Python & Read Encoders
=======================

This document describes the Python main program for communicating with the AKKON Digital Read Out (DRO) controller. The program utilizes the ``DROController`` class from the ``uDROHal`` module to read device data and axis values via a serial interface.

Functional Description
----------------------

The main program executes the following steps upon startup:

1. **Initialization**: Establishes a connection via the defined COM port (e.g., ``COM5``).
2. **Device Inquiry**: One-time retrieval of hardware and firmware information using ``get_device_info()``.
3. **Information Output**: Displays the device name, hardware version, firmware version, build date, and number of axes in a formatted block.
4. **Data Acquisition Loop**: Continuously polls the current positions and velocities of all axes at 2-second intervals, outputting them with a timestamp.

Program Code
------------

.. code-block:: python

    import time
    import serial
    from dro_hal import DROController

    def main():
        # Adjust the port here according to your Device Manager
        PORT = 'COM5' 
        
        try:
            # Initialize the interface
            dro = DROController(PORT)
            print(f"Attempting to establish connection to {PORT}...")
            
            # --- 1. Query DeviceInfo at startup ---
            info = dro.get_device_info()
            
            if info:
                print("\n" + "="*45)
                print("       CONTROLLER HARDWARE INFORMATION")
                print("="*45)
                print(f" Device Name:      {info['Name']}")
                print(f" Hardware Version: V{info['HW_Ver']}")
                print(f" Firmware Version: V{info['FW_Ver']}")
                print(f" Created on:       {info['Date']}")
                print(f" Axis Count:       {info['AxisCount']}")
                print("="*45 + "\n")
                
                # Short pause to allow reading the info
                time.sleep(1)
            else:
                print("Error: Could not retrieve DeviceInfo.")
                print("Check the connection and protocol compatibility.")
                return

            # --- 2. Continuous reading of axis values ---
            print("Starting data acquisition (Press Ctrl+C to stop)...\n")
            
            while True:
                axes = dro.read_controller_info()
                
                if axes:
                    # Timestamp for the line
                    timestamp = time.strftime("%H:%M:%S")
                    
                    # Construct formatted line for all axes
                    axis_output = []
                    for i, ax in enumerate(axes):
                        # Pos: Position, Vel: Velocity
                        axis_output.append(f"A{i}: {ax['Pos']:>10} (V: {ax['Vel']:>3})")
                    
                    print(f"{timestamp} | {' | '.join(axis_output)}")
                else:
                    print(f"{time.strftime('%H:%M:%S')} | Communication disrupted...")

                # Read every 2 seconds
                time.sleep(2)

        except serial.SerialException as e:
            print(f"\nSERIAL INTERFACE ERROR: {e}")
        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
        finally:
            if 'dro' in locals():
                dro.close()
                print("Serial interface closed.")

    if __name__ == "__main__":
        main()


Program output result
---------------------
.. figure::  /images/hardware/02_DRO_App/python/ex_dro_comm_py.png
   :alt: 3D View of the BlackPill Interface Board
   
   Program result running ex_dro_comm.py

Prerequisites
-------------

* **Hardware**: A connected AKKON DRO controller.
* **Libraries**: The Python library ``pyserial`` must be installed (``pip install pyserial``).
* **Modules**: The file ``uDROHal.py`` must be located in the same directory as the main program.

Troubleshooting
---------------

* **KeyError**: Ensure that the dictionary key names (e.g., ``HW_Ver``) are identical in both ``uDROHal.py`` and the main program.
* **SerialException**: Verify in the Device Manager that the controller is actually connected to ``COM5`` and that no other program (such as a terminal or the original Delphi application) is blocking the port.
