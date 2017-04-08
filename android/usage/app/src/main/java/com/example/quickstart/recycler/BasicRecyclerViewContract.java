package com.example.quickstart.recycler;

import java.util.List;

public interface BasicRecyclerViewContract {

    interface Presenter {
        void init();
        void hit(int position, String id);
    }

    interface View {
        void showData(List<PresentationModel> items);
        void updateHits(int position, int hits);
        void showTotalHits(int hits);
    }

    class PresentationModel {
        String id;
        String name;
        int hits;
    }

}
