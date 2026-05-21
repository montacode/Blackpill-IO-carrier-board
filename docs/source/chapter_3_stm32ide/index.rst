==========================================
STM32CubeIDE & Code Examples
==========================================

Introduction
------------
The **BlackPill I/O Carrier** is an expansion prototyping board for the STM32F411 BlackPill module, designed to bridge the gap between low-voltage microcontrollers and 24V industrial environments. This section provides technical documentation and code examples for native development using C/HAL and the ST-Link V2 debugger.

Examples Overview
-----------------
* **Blinking LED:** Basic GPIO toggle on pin PB10.
* **Serial PWM Buzzer Control:** USB-VCP interaction and acoustic feedback on PB8.
* **Encoder Reading:** High-resolution 32-bit tracking on PA1 and PA5.
* **PWM Ramp / DAC Signal:** Linear 5-second ramp on PB9 for power or signal control.


Example 1: Blinking LED (PB10)
------------------------------
This example verifies basic GPIO functionality. It is the ideal "Hello World" to ensure the toolchain and hardware connection are working correctly.

**Project Configuration (IOC):**

* Pin **PB10**: Set to ``GPIO_Output`` (Push-Pull, Low Speed).

**Source Code:**

.. code-block:: c

    /* Simple Blink Loop in main.c */
    while (1)
    {
        HAL_GPIO_TogglePin(GPIOB, GPIO_PIN_10);
        HAL_Delay(500);
    }

Example 2: Serial PWM Buzzer Control (PB8)
------------------------------------------
Monitors the USB Virtual COM Port (VCP). If the string "Hallo" is received, the integrated piezo ringer triggers a 2.5 kHz tone sequence.

**Project Configuration (IOC):**

* **Connectivity:** USB_OTG_FS (Device_Only).
* **Middleware:** USB_DEVICE (Communication Device Class).
* **Timer:** TIM4, Channel 3 as ``PWM Generation CH3``.
* **Settings:** Prescaler = 95, ARR = 399 (2.5 kHz).

**Source Code:**

.. code-block:: c

    if (UserRxLen > 0)
    {
        memcpy(process_buffer, UserRxBufferFS, (UserRxLen < 63) ? UserRxLen : 63);
        process_buffer[UserRxLen] = '\0';
        UserRxLen = 0;

        if (strstr((char*)process_buffer, "Hallo") != NULL)
        {
            for (int i = 0; i < 10; i++)
            {
                __HAL_TIM_SET_COMPARE(&htim4, TIM_CHANNEL_3, 200); // 50% Duty Cycle
                HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_3);
                HAL_Delay(1000);
                HAL_TIM_PWM_Stop(&htim4, TIM_CHANNEL_3);
                HAL_Delay(1000);
            }
        }
    }

Example 3: 32-Bit Encoder Reading (PA1 & PA5)
---------------------------------------------
Uses the hardware quadrature encoder interface of Timer 2. Unlike 16-bit timers, the 32-bit register allows tracking of over 4 billion increments without overflow.

**Project Configuration (IOC):**

* **TIM2:** Combined Channels set to ``Encoder Mode``.
* **Counter:** ARR = 4294967295 (Max 32-bit).
* **Pins:** PA5 (CH1), PA1 (CH2).

**Source Code:**

.. code-block:: c

    /* Initialize Encoder in main.c */
    HAL_TIM_Encoder_Start(&htim2, TIM_CHANNEL_ALL);

    while (1)
    {
        uint32_t val = __HAL_TIM_GET_COUNTER(&htim2);
        int len = sprintf(msg_buffer, "Pos: %lu\r\n", val);
        CDC_Transmit_FS((uint8_t*)msg_buffer, len);
        HAL_Delay(2000);
    }

Example 4: PWM Ramp / DAC Signal (PB9)
--------------------------------------
Generates a linear ramp from 0% to 100% duty cycle over 5 seconds. This can be used for dimming or, with an external RC filter, as a 0..10V control signal.

**Project Configuration (IOC):**

* **TIM4:** Channel 4 as ``PWM Generation CH4``.
* **Settings:** Prescaler = 95, ARR = 999 (1 kHz frequency).

**Source Code:**

.. code-block:: c

    HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_4);

    while (1)
    {
        /* 5 second ramp: 500 steps * 10ms */
        for (uint16_t dc = 0; dc <= 1000; dc += 2)
        {
            __HAL_TIM_SET_COMPARE(&htim4, TIM_CHANNEL_4, dc);
            HAL_Delay(10);
        }
    }
