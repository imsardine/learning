package com.example.usage.fragment;

import android.os.Bundle;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;

import com.example.usage.R;

public class FragmentViaViewGroupActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_fragment_via_view_group);
    }

    @Override
    protected void onResume() {
        super.onResume();

        FragmentA fragment = FragmentA.newInstance();
        FragmentTransaction transaction = getSupportFragmentManager().beginTransaction();
        transaction.add(R.id.fragment_placeholder, fragment);
        transaction.commit();
    }
}
