package com.example.di;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

import java.text.SimpleDateFormat;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView greeting = (TextView) findViewById(R.id.greeting);
        greeting.setText("Hello, World! (" + today() + ")");
    }

    private String today() {
        Time time = Injection.provideTime();
        return new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(time.today());
    }

}
