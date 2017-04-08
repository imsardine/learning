package com.example.quickstart.recycler;

import com.example.quickstart.BusinessItem;
import com.example.quickstart.recycler.BasicRecyclerViewContract.PresentationModel;
import com.example.quickstart.recycler.BasicRecyclerViewContract.Presenter;
import com.example.quickstart.recycler.BasicRecyclerViewContract.View;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class BasicRecyclerViewPresenter implements Presenter {

    private static List<BusinessItem> BUSINESS_ITEMS = Arrays.asList(
        new BusinessItem("#1", "Item 1", "..."), new BusinessItem("#2", "Item 2", "...")
    );

    private View view;

    private Map<String, Integer> itemHits = new HashMap<>(); // ID : hits

    public BasicRecyclerViewPresenter(View view) {
        this.view = view;
    }

    @Override
    public void init() {
        view.showData(transformModel());
    }

    private List<PresentationModel> transformModel() {
        List<PresentationModel> output = new ArrayList<>();

        for (BusinessItem item : BUSINESS_ITEMS) {
            PresentationModel presentation = new PresentationModel();
            presentation.id = item.getID();
            presentation.name = item.getName();
            presentation.hits = 0;

            output.add(presentation);
        }

        return output;
    }

    @Override
    public void hit(int position, String id) {
        if (!itemHits.containsKey(id)) {
            itemHits.put(id, 0);
        }

        int hits = itemHits.get(id) + 1;
        itemHits.put(id, hits);

        view.updateHits(position, hits);
        view.showTotalHits(totalHits());
    }

    private int totalHits() {
        int total = 0;

        for (int hits : itemHits.values()) {
            total += hits;
        }

        return total;
    }

}

