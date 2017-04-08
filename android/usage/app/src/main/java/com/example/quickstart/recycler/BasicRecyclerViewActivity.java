package com.example.quickstart.recycler;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.widget.Toast;

import com.example.quickstart.R;
import com.example.quickstart.recycler.BasicRecyclerViewContract.PresentationModel;
import com.example.quickstart.recycler.BasicRecyclerViewContract.Presenter;

import java.util.List;

public class BasicRecyclerViewActivity extends AppCompatActivity implements BasicRecyclerViewAdapter.ItemClickListener {

    private BasicRecyclerViewAdapter adapter;

    private Presenter presenter;

    private List<PresentationModel> items;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_recycler_view);

        RecyclerView recycler = (RecyclerView) findViewById(R.id.recycler);
        recycler.setAdapter(adapter = new BasicRecyclerViewAdapter(this, this));

        // Setting layout manager in XML layout files is recommended.
        // recycler.setLayoutManager(new LinearLayoutManager(this));

        presenter = new BasicRecyclerViewPresenter(new MvpView());
        presenter.init();
    }

    @Override
    public void onItemClicked(int position, String id) {
        presenter.hit(position, id);
    }

    private class MvpView implements BasicRecyclerViewContract.View {

        @Override
        public void showData(List<PresentationModel> items) {
            adapter.setData(BasicRecyclerViewActivity.this.items = items);
        }

        @Override
        public void updateHits(int position, int hits) {
            items.get(position).hits = hits;
            // or adapter.updateHits(position, hits), so the view don't have to manipulate data.
            adapter.notifyItemChanged(position);
        }

        @Override
        public void showTotalHits(int hits) {
            String message = String.format("Totoal HITS: %d !!", hits);
            Toast.makeText(BasicRecyclerViewActivity.this, message, Toast.LENGTH_SHORT).show();
        }

    }

}
