=================================
Arduino IDE & Code Examples
=================================

Using the **BlackPill I/O Carrier** with the Arduino IDE is an excellent choice for rapid prototyping and leveraging the vast ecosystem of Arduino libraries. This is made possible by the **STM32duino** core.

Quick Setup
-----------

1. **Install Arduino IDE:** Download the latest version from the official website.
2. **Add STM32 Board Support:**
   Add the following URL to *File > Preferences > Additional Boards Manager URLs*:
   ``https://github.com/stm32duino/BoardManagerFiles/raw/main/package_st_central_index.json``
3. **Install Package:** In *Boards Manager*, search for "STM32" and install "STM32 MCU based boards".
4. **Select Board:** * Board: "Generic STM32F4 series"
   * Part Number: "BlackPill F411CE"
   * Upload Method: "STM32CubeProgrammer (SWD)" (requires ST-Link V2).

Pin Mapping Overview
--------------------

For the **BlackPill I/O Carrier**, use these definitions in your sketches:

* **Buzzer / Status LED:** ``PB8`` or ``PA1`` (depending on assembly)
* **Digital Inputs:** ``PA0``, ``PA1``, ``PA5``
* **Analog / PWM Output:** ``PA8``, ``PB9``
* **Serial Interface (J4):** ``Serial1`` (PA9/PA10)

-----------------------------------------------------

Example 1: Blinking LED (Status Check)
--------------------------------------

**Description:**
This "Hello World" verifies the toolchain and basic GPIO control. It toggles pin **PB10** every 500ms.

.. code-block:: cpp

    /* Simple LED Blinking for BlackPill I/O Carrier */
    void setup() {
      pinMode(PB10, OUTPUT);
    }

    void loop() {
      digitalWrite(PB10, HIGH);
      delay(500);
      digitalWrite(PB10, LOW);
      delay(500);
    }

**Hardware Note:**
Ensure your LED and resistor are connected to the PB10 header. The carrier uses **0603 footprints** for these components, suitable for manual soldering.

-----------------------------------------------------

Example 2: Serial USB Control & Buzzer
--------------------------------------

**Description:**
Demonstrates interaction via USB Virtual COM Port (VCP). Sending the keyword "Hallo" (ASCII) triggers 10 beeps on the integrated buzzer (PB8).

.. code-block:: cpp

    /* USB Serial trigger for Buzzer on PB8 */
    const int buzzerPin = PB8;

    void setup() {
      Serial.begin(115200);
      pinMode(buzzerPin, OUTPUT);
    }

    void loop() {
      if (Serial.available() > 0) {
        String input = Serial.readString();
        if (input.indexOf("Hallo") >= 0) {
          for (int i = 0; i < 10; i++) {
            digitalWrite(buzzerPin, HIGH);
            delay(1000);
            digitalWrite(buzzerPin, LOW);
            delay(1000);
          }
        }
      }
    }

**Hardware Note:**
The buzzer circuit uses a piezo ringer (e.g., Murata PKLCS1212E2000-R1) driven by **PB8**.

-----------------------------------------------------

Example 3: 32-Bit Hardware Encoder Reading
------------------------------------------

**Description:**
Utilizes the native 32-bit hardware timer (TIM2) for high-resolution tracking on pins **PA1** and **PA5**. This avoids 16-bit overflows common in smaller MCUs.

.. code-block:: cpp

    /* 32-Bit Encoder on TIM2 (PA1 and PA5) */
    #include <HardwareTimer.h>

    void setup() {
      Serial.begin(115200);
      TIM_TypeDef *Instance = TIM2;
      HardwareTimer *MyTim = new HardwareTimer(Instance);

      Instance->CR1 = 0;
      Instance->SMCR = TIM_ENCODERMODE_TI12; 
      Instance->ARR = 0xFFFFFFFF; // Max 32-bit value
      Instance->CNT = 0;
      Instance->CR1 |= TIM_CR1_CEN;
    }

    void loop() {
      uint32_t count = TIM2->CNT;
      Serial.print("Encoder Position: ");
      Serial.println(count);
      delay(2000);
    }

**Hardware Note:**
The carrier provides level shifting for 24V industrial encoders. Check your **0603 RC-filter** assembly for signal debouncing.

-----------------------------------------------------

Example 4: 5-Second PWM Ramp
----------------------------

**Description:**
Generates a linear PWM ramp on pin **PB9**, increasing from 0% to 100% duty cycle over 5 seconds.

.. code-block:: cpp

    /* PWM Ramp on PB9 (0 to 5 Seconds) */
    const int pwmPin = PB9;

    void setup() {
      pinMode(pwmPin, OUTPUT);
    }

    void loop() {
      for (int i = 0; i <= 255; i++) {
        analogWrite(pwmPin, i);
        delay(19); // ~5000ms / 256 steps
      }
    }

**Hardware Note:**
PB9 is routed to the output stage. For a true analog voltage, use the **0603 footprints** on the carrier to install an RC low-pass filter.

-----------------------------------------------------

..