package com.example.quickstart.recycler;

import java.io.Serializable;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

public interface BasicRecyclerViewContract {

    interface Presenter {
        String STATE_HITS = "Hits";
        List<String> STATE_KEYS = Arrays.asList(STATE_HITS);

        void init(Map<String, Serializable> state);
        void hit(int position, String id);
        Map<String, Serializable> prepareState();
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
