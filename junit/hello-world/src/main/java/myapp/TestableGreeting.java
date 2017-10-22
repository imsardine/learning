package myapp;

import java.io.PrintStream;
import java.util.Calendar;

public class TestableGreeting {

    private PrintStream out;

    private Timer timer;

    TestableGreeting(PrintStream out, Timer timer) {
        this.out = out; // this.out = System.out;
        this.timer = timer; // this.timer = new LocalTimer();
    }

    public static void main(String[] args) {
		new TestableGreeting(System.out, new LocalTimer()).run();
    }

    public void run() {
       Calendar cal = Calendar.getInstance();
       cal.setTimeInMillis(timer.currentTimeMillis());
       int hour = cal.get(Calendar.HOUR_OF_DAY);

       if (hour >= 6 && hour < 12) {
           out.println("Good morning!");
       } else if (hour >= 12 && hour < 17) {
           out.println("Good afternoon!");
       } else if (hour >= 17 && hour <= 22) {
           out.println("Good evening!");
       } else {
           out.println("Zzz...");
       }
    }

}

