package com.example.quickstart.recycler;

import android.content.Context;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.TextView;

import com.example.quickstart.R;
import com.example.quickstart.recycler.BasicRecyclerViewContract.PresentationModel;

import java.util.List;

public class BasicRecyclerViewAdapter extends RecyclerView.Adapter<BasicRecyclerViewAdapter.ViewHolder> {

    public interface ItemClickListener {
        void onItemClicked(int position);
    }

    private LayoutInflater inflater;
    private List<PresentationModel> items;
    private ItemClickListener listener;

    public BasicRecyclerViewAdapter(Context context, ItemClickListener listener) {
        inflater = LayoutInflater.from(context);
        this.listener = listener;
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
    }

    @Override
    public int getItemCount() {
        return items == null ? 0 : items.size();
    }

    public void setData(List<PresentationModel> items) {
        this.items = items;
        notifyDataSetChanged();
    }

    class ViewHolder extends RecyclerView.ViewHolder implements OnClickListener {

        public TextView text;

        public ViewHolder(View itemView) {
            super(itemView);
            text = (TextView) itemView.findViewById(R.id.text);
            itemView.setOnClickListener(this);
        }

        @Override
        public void onClick(View v) {
            if (listener != null) {
                listener.onItemClicked(getAdapterPosition());
            }
        }
    }
}
