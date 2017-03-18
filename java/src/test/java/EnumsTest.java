package io.github.imsardine.learning.java;

import org.junit.Test;
import static org.junit.Assert.*;

public class DayOfWeekTest {

    @Test
    public void enumTypesImplicitlyExtendsEnum() {
        assertSame(Enum.class, DayOfWeek.class.getSuperclass());
    }

    @Test
    public void staticValuesMethodIsAutomaticallyGenerated() {
        // Unfortunately, it cannot be written as ` { MONDAY, TUESDAY ... }`
        DayOfWeek[] expected = { DayOfWeek.MONDAY, DayOfWeek.TUESDAY,
            DayOfWeek.WEDNESDAY, DayOfWeek.THURSDAY, DayOfWeek.FRIDAY,
            DayOfWeek.SATURDAY, DayOfWeek.SUNDAY };
        assertEquals(expected, DayOfWeek.values());
    }

    @Test
    public void enumTypeIsNullable() {
        DayOfWeek day = null;
        assertNull(day);
    }

    @Test
    public void enumValuesWithParameters() {
        for (DayOfWeek day : DayOfWeek.values()) {
            if (day == DayOfWeek.SATURDAY || day == DayOfWeek.SUNDAY) {
                assertTrue(day.weekend());
            } else {
                assertFalse(day.weekend());
            }
        }
    }

    @Test
    public void getNameOfEnumConstant() {
        assertEquals("SUNDAY", DayOfWeek.SUNDAY.name());
    }

    @Test
    public void getEnumConstantByName() {
        DayOfWeek sunday = Enum.valueOf(DayOfWeek.class, "SUNDAY");
        assertSame(DayOfWeek.SUNDAY, sunday);
    }

}

