/*
 * Copyright 2016, The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.example.androidthings.myproject;

import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;

import com.google.android.things.pio.Gpio;
import com.google.android.things.pio.GpioCallback;
import com.google.android.things.pio.PeripheralManagerService;

import java.io.IOException;

/**
 * Skeleton of the main Android Things activity. Implement your device's logic
 * in this class.
 *
 * Android Things peripheral APIs are accessible through the class
 * PeripheralManagerService. For example, the snippet below will open a GPIO pin and
 * set it to HIGH:
 *
 * <pre>{@code
 * PeripheralManagerService service = new PeripheralManagerService();
 * mLedGpio = service.openGpio("BCM6");
 * mLedGpio.setDirection(Gpio.DIRECTION_OUT_INITIALLY_LOW);
 * mLedGpio.setValue(true);
 * }</pre>
 *
 * For more complex peripherals, look for an existing user-space driver, or implement one if none
 * is available.
 *
 */
public class MainActivity extends Activity {
    private static final String TAG = MainActivity.class.getSimpleName();
    private static final String BUTTON_PIN = "BCM21";
    private static final String LED_PIN = "BCM6";
    private static final long BLINK_INTERVAL = 500; // ms

    private Gpio mButton;
    private Gpio mLed;
    private GpioCallback mButtonCallback;

    private Handler mHandler;
    private Runnable mBlinkRunnable;
    private boolean pressed;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.d(TAG, "onCreate");

        PeripheralManagerService service = new PeripheralManagerService();
        Log.d(TAG, "Available GPIO pins: " + service.getGpioList());

        mButtonCallback = new GpioCallback() {
            @Override
            public boolean onGpioEdge(Gpio gpio) {
                try {
                    pressed = !gpio.getValue();
                    Log.d(TAG, "Button pressed: " + pressed);
                } catch (IOException e) {
                    Log.e(TAG, "Error on Peripheral API", e);
                }

                return true; // keep callback active
            }
        };

        try {
            mButton = service.openGpio(BUTTON_PIN);
            mButton.setDirection(Gpio.DIRECTION_IN);
            mButton.setEdgeTriggerType(Gpio.EDGE_BOTH);
            mButton.registerGpioCallback(mButtonCallback);

            mLed = service.openGpio(LED_PIN);
            mLed.setDirection(Gpio.DIRECTION_OUT_INITIALLY_LOW);
        } catch (IOException e) {
            Log.e(TAG, "Error on Peripheral API", e);
        }

        mHandler = new Handler();
        mBlinkRunnable = new Runnable() {
            @Override
            public void run() {
                try {
                    if (pressed) {
                        mLed.setValue(!mLed.getValue());
                    } else {
                        mLed.setValue(false);
                    }

                    mHandler.postDelayed(mBlinkRunnable, BLINK_INTERVAL);
                } catch (IOException e) {
                    Log.e(TAG, "Error on Peripheral API", e);
                }
            }
        };

        mHandler.post(mBlinkRunnable);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Log.d(TAG, "onDestroy");

        if (mButton != null) {
            mButton.unregisterGpioCallback(mButtonCallback);
            try {
                mButton.close();
            } catch (IOException e) {
                Log.e(TAG, "Error on Peripheral API", e);
            }
        }

        if (mLed != null) {
            try {
                mLed.close();
            } catch (IOException e) {
                Log.e(TAG, "Error on Peripheral API", e);
            }
        }
    }

}
