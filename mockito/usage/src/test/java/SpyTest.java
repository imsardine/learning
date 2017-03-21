import java.util.List;
import java.util.ArrayList;

import org.junit.Test;
import static org.mockito.Mockito.*;
import static org.junit.Assert.*;

public class SpyTest {

    @Test
    public void normalUsage() {
        // to avoid confusion, do not keep the real instance
        List<String> list = spy(new ArrayList<String>());

        list.add("item1");
        list.add("item2");

        verify(list).add("item1");
        verify(list).add("item2");

        assertEquals(2, list.size());
        assertTrue(list.contains("item1"));
        assertFalse(list.contains("item3"));
    }

    @Test
    public void spyObjectIsNotWrapperAroundRealObject() {
        List<String> real = new ArrayList<>();
        List<String> spy = spy(real); // a COPY of the real object

        spy.add("item1");
        verify(spy).add("item1");

        assertEquals(1, spy.size());
        assertEquals(0, real.size());
    }

}

