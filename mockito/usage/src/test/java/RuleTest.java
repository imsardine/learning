import java.util.List;

import org.junit.Test;
import org.junit.Rule;
import static org.junit.Assert.*;

import org.mockito.Mock;
import static org.mockito.Mockito.*;
import org.mockito.junit.MockitoRule;
import org.mockito.junit.MockitoJUnit;

public class RuleTest {

    @Rule
    public MockitoRule mockitoRule = MockitoJUnit.rule(); 

    @Mock
    private List list;

    @Test
    public void test() {
        list.add("Item");
        verify(list).add("Item");
    }

}
