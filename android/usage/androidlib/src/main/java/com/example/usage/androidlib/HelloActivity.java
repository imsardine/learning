package com.example.usage.androidlib;

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

import com.example.usage.Greeting;

public class HelloActivity extends AppCompatActivity {

    private static final String EXTRA_SOMEBODY = "SOMEBODY";

    public static Intent prepareIntent(Context context, String somebody) {
        Intent intent = new Intent(context, HelloActivity.class);
        intent.putExtra(EXTRA_SOMEBODY, somebody);

        return intent;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_hello);

        Intent intent = getIntent();
        String somebody = intent.getStringExtra(EXTRA_SOMEBODY);

        ((TextView) findViewById(R.id.greeting)).setText(new LibGreeting().hello(somebody));
    }

}


