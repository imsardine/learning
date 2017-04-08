package com.example.quickstart.recycler;

import com.example.quickstart.BusinessItem;
import com.example.quickstart.recycler.BasicRecyclerViewContract.PresentationModel;
import com.example.quickstart.recycler.BasicRecyclerViewContract.Presenter;
import com.example.quickstart.recycler.BasicRecyclerViewContract.View;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class BasicRecyclerViewPresenter implements Presenter {

    private static List<BusinessItem> BUSINESS_ITEMS = Arrays.asList(
        new BusinessItem("Item 1", "..."), new BusinessItem("Item 2", "...")
    );

    private View view;

    private List<PresentationModel> items;

    public BasicRecyclerViewPresenter(View view) {
        this.view = view;
    }

    @Override
    public void init() {
        view.showData(items = transformModel());
    }

    private List<PresentationModel> transformModel() {
        List<PresentationModel> output = new ArrayList<>();

        for (BusinessItem item : BUSINESS_ITEMS) {
            PresentationModel presentation = new PresentationModel();
            presentation.name = item.getName();
            presentation.hits = 0;

            output.add(presentation);
        }

        return output;
    }

    @Override
    public void hit(int position) {
        PresentationModel item = items.get(position);
        item.hits += 1;

        view.updateItem(position);
        view.showTotalHits(totalHits());
    }

    private int totalHits() {
        int total = 0;

        for (PresentationModel item : items) {
            total += item.hits;
        }

        return total;
    }



}
