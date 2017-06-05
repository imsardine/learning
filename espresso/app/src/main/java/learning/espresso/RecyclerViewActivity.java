package learning.espresso;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.RecyclerView.Adapter;
import android.support.v7.widget.RecyclerView.ViewHolder;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

public class RecyclerViewActivity extends AppCompatActivity {
    private TextView selectedItem;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_recycler_view);

        selectedItem = (TextView) findViewById(R.id.selected_item);
        RecyclerView recyclerView = (RecyclerView) findViewById(R.id.recycler);
        recyclerView.setAdapter(new CustomAdapter());
    }

    class CustomAdapter extends Adapter<CustomViewHolder> {
        private LayoutInflater inflater;
        private List<String> dataItems;

        CustomAdapter() {
            inflater = LayoutInflater.from(RecyclerViewActivity.this);
            dataItems = new ArrayList<>();
            for (int i = 0; i <= 50; i++) {
                dataItems.add("Item " + (i + 1));
            }
        }

        @Override
        public CustomViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
            View itemView = inflater.inflate(R.layout.list_item_layout, parent, false);
            return new CustomViewHolder(itemView);
        }

        @Override
        public void onBindViewHolder(CustomViewHolder holder, int position) {
            holder.textView.setText(dataItems.get(position));
        }

        @Override
        public int getItemCount() {
            return dataItems.size();
        }
    }

    class CustomViewHolder extends ViewHolder {
        TextView textView;

        CustomViewHolder(final View itemView) {
            super(itemView);
            textView = (TextView) itemView.findViewById(R.id.item_text);
            textView.setOnClickListener(new OnClickListener() {
                @Override
                public void onClick(View v) {
                    selectedItem.setText(textView.getText());
                }
            });
        }

    }

}
