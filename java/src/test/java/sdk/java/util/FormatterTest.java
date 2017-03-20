package sdk.java.util;

import org.junit.Test;
import java.util.Formatter;
import static org.junit.Assert.*;

public class FormatterTest {

    @Test
    public void basicUsage() {
        Formatter formatter = new Formatter();
        int min = 15, max = 20;

        formatter.format( // returns self, instead of the formatted string
                "Generally, the average tip is %d%% to %d%% of the total meal cost.",
                min, max); // where '%%' represents a literal '%'

        String actual = formatter.toString(); // equivalent to formatter.out().toString()
        assertEquals("Generally, the average tip is 15% to 20% of the total meal cost.", actual);
    }

    @Test
    public void explictArgumentIndices() {
        Formatter formatter = new Formatter();
        formatter.format(
                "%1$s is abbreviated to %3$c%3$c%2$c%3$c.", // re-order, adjacent format specifiers
                "Pen-Pineapple-Apple-Pen", 'A', 'P'); // various data types

        String actual = formatter.toString();
        assertEquals("Pen-Pineapple-Apple-Pen is abbreviated to PPAP.", actual);
    }

    @Test
    public void mixImplicitExplicitArgumentIndices() {
        Formatter formatter = new Formatter();
        formatter.format("%4$d %d %d %1$d", 4, 3, 2, 1);

        // specifiers w/o arg index consume args in order
        String actual = formatter.toString();
        assertEquals("1 4 3 4", actual);
    }

}

