package com.example.usage;

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class AnotherActivity extends AppCompatActivity {

    private static final String EXTRA_SOMEBODY = "SOMEBODY";

    public static Intent prepareIntent(Context context, String somebody) {
        Intent intent = new Intent(context, AnotherActivity.class);
        intent.putExtra(EXTRA_SOMEBODY, somebody);

        return intent;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_another);

        Intent intent = getIntent();
        String somebody = intent.getStringExtra(EXTRA_SOMEBODY);
        if ("".equals(somebody)) {
            somebody = "World";
        }

        ((TextView) findViewById(R.id.greeting)).setText(String.format("Hello, %s!", somebody));
    }
}
