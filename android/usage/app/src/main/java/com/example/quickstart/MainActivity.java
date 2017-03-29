package com.example.quickstart;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import java.util.Arrays;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);
        ListView list = (ListView) findViewById(R.id.samples_list);

        final ArrayAdapter<String> adapter = new ArrayAdapter<>(
                this, R.layout.sample_list_item, R.id.text, Arrays.asList("Item 1", "Item 2"));
        list.setAdapter(adapter);

        list.setOnItemClickListener(new OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Toast.makeText(MainActivity.this, adapter.getItem(position), Toast.LENGTH_SHORT).show();
            }
        });
    }

    public void sayHello(View view) { // corresponds to android:onClick="sayHello" in the XML layout.
        EditText input = (EditText) findViewById(R.id.somebody);
        startActivity(AnotherActivity.prepareIntent(this, input.getText().toString()));
    }

}
