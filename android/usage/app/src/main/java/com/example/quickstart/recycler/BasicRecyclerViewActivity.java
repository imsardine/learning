package com.example.quickstart.recycler;

import android.content.Context;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;

import com.example.quickstart.R;
import com.example.quickstart.recycler.BasicRecyclerViewContract.PresentationModel;
import com.example.quickstart.recycler.BasicRecyclerViewContract.Presenter;

import java.util.List;

public class BasicRecyclerViewActivity extends AppCompatActivity {

    private Adapter adapter;

    private Presenter presenter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_recycler_view);

        RecyclerView recycler = (RecyclerView) findViewById(R.id.recycler);
        recycler.setAdapter(adapter = new Adapter(this));

        // Setting layout manager in XML layout files is recommended.
        // recycler.setLayoutManager(new LinearLayoutManager(this));

        presenter = new BasicRecyclerViewPresenter(new MvpView());
        presenter.init();
    }

    private class MvpView implements BasicRecyclerViewContract.View {

        @Override
        public void showData(List<PresentationModel> items) {
            adapter.setData(items);
        }

        @Override
        public void updateItem(int position) {
            adapter.notifyItemChanged(position);
        }

        @Override
        public void showTotalHits(int hits) {
            String message = String.format("Totoal HITS: %d !!", hits);
            Toast.makeText(BasicRecyclerViewActivity.this, message, Toast.LENGTH_SHORT).show();
        }

    }

    private class Adapter extends RecyclerView.Adapter<ViewHolder> {
        private LayoutInflater inflater;
        private List<PresentationModel> items;

        public Adapter(Context context) {
            inflater = LayoutInflater.from(context);
        }

        @Override
        public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
            View view = inflater.inflate(R.layout.sample_list_item, parent, false);
            return new ViewHolder(view);
        }

        @Override
        public void onBindViewHolder(ViewHolder holder, final int position) {
            PresentationModel item = items.get(position);

            String message = String.format("%s (%d)", item.name, item.hits);
            holder.text.setText(message);

            holder.itemView.setOnClickListener(new OnClickListener() {
                @Override
                public void onClick(View v) {
                    presenter.hit(position);
                }
            });
        }

        @Override
        public int getItemCount() {
            return items == null ? 0 : items.size();
        }

        public void setData(List<PresentationModel> items) {
            this.items = items;
            notifyDataSetChanged();
        }

    }

    private class ViewHolder extends RecyclerView.ViewHolder {

        public TextView text;

        public ViewHolder(View itemView) {
            super(itemView);
            text = (TextView) itemView.findViewById(R.id.text);
        }

    }

}
