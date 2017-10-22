package myapp;

import java.util.Calendar;

public class Greeting {

    public static void main(String[] args) {
        int hour = Calendar.getInstance().get(Calendar.HOUR_OF_DAY);

        if (hour >= 6 && hour < 12) {
            System.out.println("Good morning!");
        } else if (hour >= 12 && hour < 17) {
            System.out.println("Good afternoon!");
        } else if (hour >= 17 && hour <= 22) {
            System.out.println("Good evening!");
        } else {
            System.out.println("Zzz...");
        }
    }

}
