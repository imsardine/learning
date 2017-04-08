package com.example.quickstart.recycler;

import java.util.List;

public interface BasicRecyclerViewContract {

    interface Presenter {
        void init();
        void hit(int position);
    }

    interface View {
        void showData(List<PresentationModel> items);
        void updateItem(int position);
        void showTotalHits(int hits);
    }

    class PresentationModel {
        String name;
        int hits;
    }

}
